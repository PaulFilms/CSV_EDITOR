''' 
# CSV EDITOR | DATA

`TASK:`
\n
`WARNINGS:`
\n
'''
__update__ = '2023.11.15'
__author__ = 'PABLO GONZALEZ PILA <pablogonzalezpila@gmail.com>'

''' SYSTEM LIBRARIES '''
from dataclasses import dataclass, asdict, fields
from PyQt6.QtWidgets import QPushButton, QTableWidget

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
    BTN_OPEN: QPushButton
    BTN_SAVE: QPushButton
    TBL_DATA: QTableWidget
    BTN_FIELDS: QPushButton
    BTN_ADD: QPushButton