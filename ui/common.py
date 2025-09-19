from PyQt5.QtWidgets import qApp, QMenuBar, QAction, QMenu, QApplication
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
import datetime
from settings.handler import PersistenceSettings, RuntimeSettings
from catalog.handler import CatalogHandler

WINDOW_TYPES = [
    'Qt.Widget', 
'Qt.Window',  
'Qt.Dialog', 
'Qt.Sheet', 
'Qt.Drawer', 
'Qt.Popup', 
'Qt.Tool', 
'Qt.ToolTip', 
'Qt.SplashScreen', 
'Qt.Desktop', 
'Qt.SubWindow', 
'Qt.ForeignWindow', 
'Qt.CoverWindow'
]

class ActionSpec:
    def __init__(self, id, tooltip, shortcut, cmd):
        self.id = id
        self.tooltip = tooltip
        self.shortcut = shortcut
        self.cmd = cmd

class MenuSpec:
    def __init__(self, id, actions):
        self.id = id
        self.actions = actions

def widget_desc(widget):
    return widget.objectName()

def get_main_window():
    widgets = qApp.topLevelWidgets()
    for index, widget in enumerate(widgets):
        name = widget.objectName()
        if name == 'mainWindow':
            return widget
    return qApp

def get_api():
    # Find the scripting API object with its name in QT
    widgets = qApp.topLevelWidgets()
    for widget in widgets:
        n = widget.objectName()
        if n == 'mainWindow':
            mainWindow = widget
    for child in mainWindow.children():
        n = child.objectName()
        if n == 'scriptingApi':
            return child
    return None

def remove_menu(main_window, search_menu_id: str):
    main_menu = main_window.findChildren(QMenuBar)[0]
    menu = main_menu.findChild(QMenu, search_menu_id)
    if menu:
        menu.clear()
        menu.deleteLater()


def add_menu(main_window, menu_spec: MenuSpec):
    main_menu = main_window.findChildren(QMenuBar)[0]
    
    new_menu_id = menu_spec.id
    new_menu = main_menu.findChild(QMenu, new_menu_id)
    if not new_menu:
        new_menu = main_menu.addMenu(new_menu_id)
        new_menu.setObjectName(new_menu_id)
    else:
        new_menu.clear()

    for action_spec in menu_spec.actions:
        action = QAction(QIcon(), action_spec.id, main_window)
        action.setShortcut(action_spec.shortcut)
        action.setStatusTip(action_spec.tooltip)
        action.triggered.connect(action_spec.cmd)
        new_menu.addAction(action)

def widgets_recursive(d, widget = None, doPrint =False ):
    if not widget:
        for widget in QApplication.topLevelWidgets():
            get_widget(widget, d, 0, doPrint)
    else:
        get_widget(widget, d, 0, doPrint)
                
def get_widget(w,d, depth = 0, doPrint=False):
    '''
        Recursively searches through all widgets down the tree and prints if desired.
    :param w: the widget to search from
    :param d: the dictionary to add it to
    :param depth: current depth we are at
    :param doPrint: if we need to print
    :return:
    '''
    n = w.objectName()
    n = n if n else to_str(w)
    if doPrint: print("\t"*depth, n)
    newD = {}
    for widget in w.children():
        get_widget(widget, newD, depth +1 )
    d[n] = newD

def get_widget_from_name(name):
    for widget in QApplication.allWidgets():
        try:
            if name in widget.objectName() :
                return widget
        except:
            pass
    return None

def to_str(object):
    if isinstance(object, QAction):
        return ' QAction > '+ object.text()
    return str(object) 

def get_settings():
    main_window = get_main_window()
    if not hasattr(main_window, 'persistence_settings'):
        set_settings_handler()
    return main_window.persistence_settings

def get_runtime():
    main_window = get_main_window()
    if not hasattr(main_window, 'runtime_settings'):
        set_settings_handler()
    return main_window.runtime_settings

def get_catalog_handler():
    main_window = get_main_window()
    if not hasattr(main_window, 'catalog_handler'):
        set_settings_handler()
    return main_window.catalog_handler


def set_rt_settings(rt_settings):
    rt = get_runtime()
    rt.update(rt_settings)


def set_settings_handler():
    main_window = get_main_window()
    main_window.__setattr__('persistence_settings', PersistenceSettings())
    main_window.__setattr__('runtime_settings', RuntimeSettings())
    main_window.__setattr__('catalog_handler', CatalogHandler())


EPOCH_2000 = datetime.datetime(2000, 1, 1, 12, 0, tzinfo=datetime.timezone.utc).timestamp()

def cosmo_time_to_utc(cosmo_time):
    delta = (32.5 + 37) # TDB to UTC delta
    date_utc = datetime.datetime.fromtimestamp(EPOCH_2000 + cosmo_time - delta, tz=datetime.timezone.utc)
    return date_utc.isoformat()

def show_url_in_browser(url_str):
    QDesktopServices.openUrl(QUrl(url_str, QUrl.TolerantMode))
