from PyQt5.QtWidgets import qApp, QMenuBar, QAction, QMenu, QDialog, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon

import time
from dataclasses import dataclass

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

@dataclass
class ActionSpec:
    """Class for describing an action."""
    id: str
    tooltip: str
    shortcut: str
    cmd: any


@dataclass
class MenuSpec:
    """Class for describing a menu."""
    id: str
    actions: list[ActionSpec]

def widget_desc(widget):
    return f'{widget.objectName()} {widget.isWindow()} {widget.width()} {widget.height()} {WINDOW_TYPES[widget.windowType()]}'

def get_main_window():
    widgets = qApp.topLevelWidgets()
    for index, widget in enumerate(widgets):
        name = widget.objectName()
        # print(f'{index:03d}=> {widget_desc(widget)}')
        if name == 'mainWindow':
            return widget
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
        return f' QAction > {object.text()}'
    return str(object) 

