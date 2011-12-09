from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import join

class PostgreSQL(BaseEngine):
    categories = ["database"]
    version = "postgresql-9.1.1"
    source_url = "http://wwwmaster.postgresql.org/redir/198/h/source/v%s/" % version.split("-")[1]

    def start(self): return self.default_start(self.postgre_starter)
    def stop(self): return self.default_stop(self.postgre_stopper)
    def restart(self): return self.default_restart(self.postgre_restarter)
    def install(self, force = False): return self.default_install(self.postgre_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __postgre_installer(self):
        command('''wget "%s%s.tar.gz"''' % (self.source_url, self.version))
        command('''tar -xzf "%s.tar.gz"''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --without-readline 
                   --prefix="%s" && make && make install)''' %  (self.version, self.app_path))
        command('''(cd %s && mkdir data && mkdir logs)''' % self.app_path)
        command('''rm -rf %s && rm %s.tar.gz''' % (self.version, self.version))
        return True

    def __postgre_starter(self):
        command('''%s/bin/pg_ctl start -D %s -l %s''' % (self.app_path, join(self.app_path, "data"), join(self.app_path, "logs/PostgresLog")))
    def __postgre_stopper(self):
        command('''%s/bin/pg_ctl stop -D %s''' % (self.app_path, join(self.app_path, "data")))  
    def __postgre_restarter(self):
        command('''%s/bin/pg_ctl restart -D %s -l %s''' % (self.app_path, join(self.app_path, "data"), join(self.app_path, "logs/PostgresLog")))
