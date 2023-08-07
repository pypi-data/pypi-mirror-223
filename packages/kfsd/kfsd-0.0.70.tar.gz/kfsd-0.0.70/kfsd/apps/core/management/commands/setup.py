from django.core.management.base import BaseCommand

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.core.utils.system import System

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Dev setup"

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--working_dir",
            type=str,
            help="Working Dir",
        )
        parser.add_argument(
            "-u",
            "--utils",
            type=bool,
            help="Is Utils Pkg",
        )
        parser.add_argument(
            "-mm",
            "--makemigration",
            type=bool,
            default=True,
            help="Make Migrations",
        )
        parser.add_argument(
            "-m",
            "--migrate",
            type=bool,
            default=True,
            help="Make Migrations",
        )

    def genPyEnv(self, workingDir, isUtilsPkg):
        system = System()
        FileUtils.rm_file("db.sqlite3")
        migrationsDir = ""
        if not isUtilsPkg:
            migrationsDir = FileUtils.construct_path(
                workingDir, "kubefacets/apps/backend/migrations"
            )
            kfsdMigrationsDir = FileUtils.construct_path(
                workingDir,
                "py_env/lib/python3.10/site-packages/kfsd/apps/models/migrations",
            )
            FileUtils.rm_dir(kfsdMigrationsDir)
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(kfsdMigrationsDir)
        else:
            migrationsDir = FileUtils.construct_path(
                workingDir, "kfsd/apps/models/migrations"
            )
            FileUtils.rm_dir(migrationsDir)

        cmds = [
            "mkdir {}".format(migrationsDir),
            "touch {}/__init__.py".format(migrationsDir),
        ]

        system.cmdsExec(cmds, False)

    def makeMigrations(self):
        system = System()
        cmds = ["python manage.py makemigrations"]
        system.cmdsExec(cmds, False)

    def migrate(self):
        system = System()
        cmds = ["python manage.py migrate"]
        system.cmdsExec(cmds, False)

    def devSetup(self, workingDir, isUtilsPkg, isMakeMigrations, isMigrate):
        self.genPyEnv(workingDir, isUtilsPkg)
        if isMakeMigrations:
            self.makeMigrations()
        if isMigrate:
            self.migrate()

    def handle(self, *args, **options):
        logger.info("Dev Setup...")
        workingDir = DictUtils.get(options, "working_dir")
        isUtilsPkg = DictUtils.get(options, "utils", False)
        isMakeMigrations = DictUtils.get(options, "makemigration")
        isMigrate = DictUtils.get(options, "migrate")
        logger.info(
            "Recd working_dir: {}, is_utils_pkg: {}, is_make_migrations: {}, is_migrate: {}".format(
                workingDir, isUtilsPkg, isMakeMigrations, isMigrate
            )
        )
        self.devSetup(workingDir, isUtilsPkg, isMakeMigrations, isMigrate)
