''' 
# CSV EDITOR | MAIN

\n
`TASK:`
\n
`WARNINGS:`
'''
__version__ = '2023.11.15'
__author__ = 'PABLO GONZALEZ PILA <pablogonzalezpila@gmail.com>'
__appName__ = 'CSV EDITOR'

''' SYSTEM LIBRARIES '''
import os, sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QPushButton, QTableWidget

''' CUSTOM MAIN LIBRARIES '''
import pydeveloptools.func_pyqt6 as QT

''' APP EXTENSIONS '''
from func_data import WG

''' GLOBAL VARIABLES '''
uiFileName = r"main_GUI.ui"

''' MAIN CLASS
    ---------- '''

class MAIN_WINDOW(QMainWindow):
    def __init__(self) -> None:
        super(MAIN_WINDOW, self).__init__()
        
        ## FOLDERS
        # self.sysPath = os.getcwd()
        try:
            self.basePath = sys._MEIPASS
        except Exception:
            self.basePath = os.path.abspath(".")
        self.dataPath = os.path.join(self.basePath, "_data")

        ## GUI .UI
        uiFile = os.path.join(self.dataPath, uiFileName)
        self.ui = uic.loadUi(uiFile, self)

        ## GUI .PY
        pass
        
        ## CONNECTIONS
        WG.BTN_SAVE: QPushButton = self.btn_save
        WG.TBL_DATA: QTableWidget = self.tbl_data
        WG.BTN_FIELDS: QPushButton = self.btn_fields
        WG.BTN_ADD: QPushButton = self.btn_add
        # 
        WG.BTN_SAVE.clicked.connect(self.SAVE)
        WG.BTN_FIELDS.clicked.connect(self.FIELDS)
        WG.BTN_ADD.clicked.connect(self.ROW_ADD)
    
    def LOAD(self):
        '''
        '''
    
    def FIELDS(self):
        '''
        '''
        tbl_data = QT.TBL_GET_PANDAS_DF(WG.TBL_DATA)
        fields = tbl_data.columns.values.tolist()
        FORM = QT.QLIST(LIST=fields, Window_Title="TABLE FIELDS")
        # FORM.setWindowIcon(QIcon(os.path.join(self.icoPath, "scope.ico")))
        FORM.exec()
        for field in FORM.value:
            if field not in fields:
                tbl_data[field] = None
        QT.TBL_POP_PANDAS_DF(WG.TBL_DATA, tbl_data)

    def ROW_ADD(self):
        '''
        '''
        WG.TBL_DATA.setRowCount(WG.TBL_DATA.rowCount()+1)

    def SAVE(self):
        '''
        '''
        tbl_data = QT.TBL_GET_PANDAS_DF(WG.TBL_DATA)
        print(tbl_data)
        print("SAVE")


''' INIT SCRIPT 
    ----------- '''

if __name__ == "__main__":
    ## APPLICATION
    APP = QApplication(sys.argv)
    
    ## DARK MODE
    import qdarktheme
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme(theme="dark", corner_shape="rounded")

    ## GUI
    WINDOW = MAIN_WINDOW()
    WINDOW.show()
    
    ## EXIT
    sys.exit(APP.exec())