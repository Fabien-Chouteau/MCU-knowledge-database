import json
import os
import fnmatch
import re

database_dir = os.path.dirname(os.path.abspath(__file__))
database_file = os.path.join(database_dir, 'mcu_knowledge_database.json')

class MCUDatabase:

    def __init__(self, filename=None):
        if filename is None:
            filename = database_file

        self.database = []
        with open(filename, 'r') as file:
            self.database = json.load(file)

        self._vendors_cache = None
        self._cores_cache = None
        self._families_cache = None

    def _clear_caches(self):
        self._vendors_cache = None
        self._cores_cache = None
        self._families_cache = None

    def list(self):
        return self.database

    def vendors(self):

        if self._vendors_cache is None:
            vendors = set()

            for mcu in self.database:
                vendors.add(mcu['vendor'])

            self._vendors_cache = sorted(list(vendors))

        return self._vendors_cache

    def cores(self):

        if self._cores_cache is None:
            cores = set()

            for mcu in self.database:
                cores.add(mcu['cpu_core'])

            self._cores_cache = sorted(list(cores))

        return self._cores_cache

    def families(self, vendor=None):

        if self._families_cache is None or vendor is not None:
            families = set()

            for mcu in self.database:
                if vendor is None or mcu['vendor'] == vendor:
                    families.add(mcu['family'])

            self._families_cache = sorted(list(families))

        return self._families_cache

    def filter_by_vendor(self, vendor):
        p = re.compile(vendor)
        self._clear_caches()
        self.database = [i for i in self.database if p.match(i['vendor'])]

    def filter_by_core(self, core):
        p = re.compile(core)
        self._clear_caches()
        self.database = [i for i in self.database if p.match(i['cpu_core'])]

    def filter_by_family(self, family):
        p = re.compile(family)
        self._clear_caches()
        self.database = [i for i in self.database if p.match(i['family'])]

    def filter_by_existing_svd(self, search_dirs):
        svd_cache = set()

        def search_svd(svdfile):
            for dir in search_dirs:
                for root, dirnames, filenames in os.walk(dir):
                    for filename in fnmatch.filter(filenames, svdfile):
                        svd_cache.add(svdfile)
                        return os.path.join(root, filename)
            return None

        def svd_exists(svdfile):
            return svdfile in svd_cache or search_svd(svdfile) is not None

        self._clear_caches()
        self.database = [i for i in self.database if svd_exists(i['svd_file'])]

    def svd_of_vendor(self, vendor):
        svdfiles = set()
        for mcu in self.database:
            if mcu['vendor'] == vendor:
                svdfiles.add(mcu['svd_file'])

        return list(svdfiles)

    def dump(self):
        return json.dumps(self.database, indent=4)
