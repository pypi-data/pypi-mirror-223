import hashlib
import inspect
import tempfile

import requests
from dbbackup import settings as dbbackup_settings
from dbbackup.utils import filename_to_datestring
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.db.migrations.loader import MigrationLoader


class BackupStorage(Storage):
    def __init__(
        self,
        base_url=None,
        repository=None,
        environment=None,
        enable_restore=False,
        enable_backup=False,
        chunk_size=50 * 1000 * 1000,
    ):
        if not base_url:
            base_url = 'https://devops.local.datamaker.io'
        if not repository:
            repository = dbbackup_settings.HOSTNAME.split('@')[0]
        if not environment:
            environment = dbbackup_settings.HOSTNAME.split('@')[1]

        self.base_url = base_url
        self.repository = repository
        self.environment = environment
        self.enable_restore = enable_restore
        self.enable_backup = enable_backup
        self.chunk_size = chunk_size
        self.schema = self.get_schema()

    def _open(self, name, mode='rb'):
        assert self.enable_restore, 'Restore is disabled'

        backup_id = name.split('_')[0]
        url = f'{self.base_url}/api/backups/{backup_id}/'
        params = {
            'repository': self.repository,
            'schema': self.schema,
        }
        if self.environment == 'production':
            params['environment'] = self.environment
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        response = requests.get(data['file'], stream=True)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in response.iter_content(8192):
                temp_file.write(chunk)

        return File(open(temp_file.name, mode), name=name)  # noqa: SIM115

    def _save(self, name, content):
        assert self.enable_backup, 'Backup is disabled'

        size = content.size
        hash_md5 = hashlib.md5()

        url = f'{self.base_url}/api/backups/upload/'
        offset = 0
        for chunk in content.chunks(self.chunk_size):
            hash_md5.update(chunk)
            response = requests.put(
                url,
                data={'filename': name},
                files={'file': chunk},
                headers={
                    'Content-Range': f'bytes {offset}-{offset + len(chunk) - 1}/{size}'
                },
            )
            response.raise_for_status()
            data = response.json()
            offset = data['offset']
            url = data['url']

        response = requests.post(url, data={'md5': hash_md5.hexdigest()})
        response.raise_for_status()
        data = response.json()

        category, database_name = self.get_content_type(name)
        if category == 'database':
            options = {'database': database_name, 'schema': self.schema}
        else:
            options = {}

        url = f'{self.base_url}/api/backups/'
        response = requests.post(
            url,
            json={
                'repository': self.repository,
                'environment': self.environment,
                'category': category,
                'chunked_upload': data['id'],
                'options': options,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data['name']

    def exists(self, name):
        assert self.enable_backup, 'Backup is disabled'
        return False

    def listdir(self, path):
        url = f'{self.base_url}/api/backups/'
        response = requests.get(
            url,
            params={
                'repository': self.repository,
                'environment': self.environment,
                'schema': self.schema,
            },
        )
        response.raise_for_status()
        data = response.json()
        return [], [item['name'] for item in data]

    def delete(self, name):
        assert self.enable_backup, 'Backup is disabled'
        backup_id = name.split('_')[0]
        url = f'{self.base_url}/api/backups/{backup_id}/'
        response = requests.delete(
            url, params={'repository': self.repository, 'environment': self.environment}
        )
        response.raise_for_status()

    @staticmethod
    def get_schema():
        loader = MigrationLoader(None, ignore_no_migrations=True)
        sources = [
            inspect.getsource(migration.__class__)
            for migration in loader.disk_migrations.values()
        ]
        sources.sort()
        return hashlib.md5(''.join(sources).encode('utf-8')).hexdigest()

    @staticmethod
    def get_content_type(name):
        name = name.split('.')[0].removesuffix(
            '-'.join([dbbackup_settings.HOSTNAME, filename_to_datestring(name)])
        )

        if name:
            name = name.removesuffix('-')
            if name in settings.DATABASES:
                return 'database', name
            else:
                raise ValueError('Unknown backup category')
        else:
            return 'media', None
