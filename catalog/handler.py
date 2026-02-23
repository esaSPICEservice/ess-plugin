import cosmoscripting



class CatalogHandler:
    cosmo = cosmoscripting.Cosmo()
    catalogs = []
    session_catalogs = []

    def __init__(self):
       self.sensor_reload_cb = None

    def set_sensor_reload_cb(self, callback):
        if self.sensor_reload_cb is None:
            self.sensor_reload_cb = callback


    def get_catalogs(self):
        return self.catalogs
    
    def get_session_catalogs(self):
        return self.session_catalogs
    
    def add_catalog(self, catalog):
        self.catalogs.append(catalog)
        self.session_catalogs.append(catalog)
        self.cosmo.loadCatalogFile(catalog)
        print('[CH] Loaded catalog: ' + catalog + ' State: ' + ','.join(self.catalogs))

    def remove_catalog(self, catalog):
        index = self.catalogs.index(catalog) if catalog in self.catalogs else -1
        if index > -1:
            undo_required = len(self.catalogs) - index
            to_be_reloaded = self.catalogs[index+1:]
            self.catalogs = self.catalogs[:index]
            for i in range(undo_required):
                self.cosmo.unloadLastCatalog()
            for cat in to_be_reloaded:
                self.cosmo.loadCatalogFile(cat)
                self.catalogs.append(cat)
                if 'sensors.json' in cat and self.sensor_reload_cb:
                    print('[CH] SENSOR ' + cat + ' NEEDS as sensor reprocessing')
                    self.sensor_reload_cb()
            print('[CH] Loaded removed: ' + catalog + ' State: ' + ','.join(self.catalogs))

    def clean_catalogs(self):
        for i in range(len(self.catalogs)):
            self.cosmo.unloadLastCatalog()
        self.catalogs = []
        print('[CH] Cleaned catalog')
