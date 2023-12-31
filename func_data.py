''' 
# CSV EDITOR | DATA

`TASK:`
\n
`WARNINGS:`
\n
'''
__update__ = '2023.11.20'
__author__ = 'PABLO GONZALEZ PILA <pablogonzalezpila@gmail.com>'

''' SYSTEM LIBRARIES '''
from dataclasses import dataclass, asdict, fields
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QTableWidget, QLineEdit

''' CUSTOM MAIN LIBRARIES '''

''' APP EXTENSIONS '''

''' GLOBAL VARIABLES '''

''' MAIN
---------------------------------------------------- '''

@dataclass
class WG:
    '''
    All widgets used in the app
    '''
    ## DEVICES
    BTN_LOAD: QPushButton
    BTN_SAVE: QPushButton
    TX_FILENAME: QLineEdit
    TBL_DATA: QTableWidget
    BTN_FIELDS: QPushButton
    BTN_ADD: QPushButton
    BTN_DUPLICATE: QPushButton
    BTN_DEL: QPushButton
    ## ICONS
    ICO_APP: QIcon
    ICO_INFO: QIcon