
from PyQt5.QtWidgets import QDialog
from ui.common import get_settings, get_runtime, get_catalog_handler
from ui.design.catalogs import Ui_catalogWidget


from settings.handler import last_repo_key, last_kernel_key, last_start_date

class  CatalogsDialog(QDialog):

    id = 'catalogs_dialog_window_id'

    def __init__(self, main_window):
        QDialog.__init__(self, main_window)
        self.settings = get_settings()
        self.run_time = get_runtime()
        self.handler = get_catalog_handler()
        self.mission = self.run_time.get('mission')
        self.init_ui()

    def init_ui(self):
        self.setObjectName(CatalogsDialog.id)
        self.catalog_widget = Ui_catalogWidget()
        self.catalog_widget.setupUi(self)
        self.catalog_widget.reloadButton.clicked.connect(self.reload)
        self.catalog_widget.removeButton.clicked.connect(self.remove)
        self.catalog_widget.refreshButton.clicked.connect(self.refresh_catalogs)
        self.current_catalogs = self.catalog_widget.current_catalogs
        self.session_catalogs = self.catalog_widget.session_catalogs


    def remove(self):
        selected = self.current_catalogs.selectedItems()
        for item in selected:
            catalog_name = item.text()
            self.handler.remove_catalog(catalog_name)

        self.refresh_catalogs()

    def reload(self):
        selected = self.session_catalogs.selectedItems()
        for item in selected:
            catalog_name = item.text()
            self.handler.add_catalog(catalog_name)
        self.refresh_catalogs()

    def refresh_catalogs(self):
        self.current_catalogs.clear()
        self.session_catalogs.clear()

        current = self.handler.get_catalogs()
        session = self.handler.get_session_catalogs()

        for catalog in current:
            self.current_catalogs.addItem(catalog)
        for catalog in session:
            if catalog not in current:
                self.session_catalogs.addItem(catalog)  


    def show_and_focus(self):
        self.hide()
        self.refresh_catalogs()
        self.show()
