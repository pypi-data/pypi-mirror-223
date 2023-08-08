from urllib.parse import quote

from dbbackup.db.base import BaseCommandDBConnector
from dbbackup.db.exceptions import DumpError


class PgDumpBinaryConnector(BaseCommandDBConnector):
    extension = 'psql.bin'
    dump_cmd = 'pg_dump'
    restore_cmd = 'pg_restore'

    def _create_dump(self):
        cmd = f'{self.dump_cmd} '
        cmd += self.create_postgres_uri()
        cmd += ' --format=custom'
        for table in self.exclude:
            cmd += f' --exclude-table-data={table}'
        cmd = f'{self.dump_prefix} {cmd} {self.dump_suffix}'
        return self.run_command(cmd, env=self.dump_env)[0]

    def _restore_dump(self, dump):
        dbname = self.create_postgres_uri(
            dbname='postgres' if '--create' in self.restore_suffix else None
        )
        cmd = f'{self.restore_cmd} {dbname}'
        cmd = f'{self.restore_prefix} {cmd} {self.restore_suffix}'
        return self.run_command(cmd, stdin=dump, env=self.restore_env)

    def create_postgres_uri(self, dbname=None):
        host = self.settings.get('HOST')

        if not host:
            raise DumpError('A host name is required')

        if not dbname:
            dbname = self.settings.get('NAME') or ''

        user = quote(self.settings.get('USER') or '')
        password = self.settings.get('PASSWORD') or ''
        password = f':{quote(password)}' if password else ''
        if not user:
            password = ''
        else:
            host = '@' + host

        port = (
            ':{}'.format(self.settings.get('PORT')) if self.settings.get('PORT') else ''
        )
        return f'--dbname=postgresql://{user}{password}{host}{port}/{dbname}'
