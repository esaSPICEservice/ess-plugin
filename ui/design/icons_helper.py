from PyQt5.QtGui import *
from . import icons_rc

def add_icon_button(button, icon_name):
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_name))
    button.setIcon(icon)

def add_icon_label(label, icon_name):
    pixmap = QPixmap(icon_name)
    label.setPixmap(pixmap)