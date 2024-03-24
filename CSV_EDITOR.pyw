''' CSV EDITOR | MAIN

TASK:
    - Usar dataclass o Enum para declarar los widgets
    - pyuic6 -o _data/main_GUI_ui.py _data/main_GUI.ui
    - Quitar del archivo .ui los iconos para añadirlos por codigo, y revisar los translates

WARNINGS:
    - Al compilar, el ejecutable no carga los iconos

________________________________________________________________________________________________ '''

__version__ = '2024.03.24'
__author__ = 'PABLO GONZALEZ PILA <pablogonzalezpila@gmail.com>'
__appName__ = 'CSV EDITOR'

''' SYSTEM LIBRARIES '''
import os, sys
import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QPushButton, QTableWidget, QLineEdit
from PyQt6.QtGui import QIcon

''' CUSTOM MAIN LIBRARIES '''
import pydeveloptools.func_system as SYS
import pydeveloptools.func_pyqt6 as QT

''' APP EXTENSIONS '''
from _data.main_GUI_ui import Ui_MainWindow


''' MAIN CLASS
________________________________________________________________________________________________ '''

class MAIN_WINDOW(QMainWindow):
    def __init__(self) -> None:
        # super(MAIN_WINDOW, self).__init__()
        super().__init__()
        
        ## FOLDERS
        self.sysPath = os.getcwd()
        try:
            self.basePath = sys._MEIPASS
        except Exception:
            self.basePath = os.path.abspath(".")
        self.dataPath = os.path.join(self.basePath, "_data")
        # REPORTS
        self.reportPath = os.path.join(self.sysPath, 'REPORTS')
        if not os.path.exists(self.reportPath): 
            os.mkdir(self.reportPath)

        ## GUI .UI
        # uiFileName = r"main_GUI.ui"
        # uiFile = os.path.join(self.dataPath, uiFileName)
        # self.ui = uic.loadUi(uiFile, self)

        ## GUI .PY FILE
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## GUI / WIDGETS
        self.ICO_INFO = QIcon(os.path.join(self.dataPath, "info.ico"))
        self.ui.statusbar.showMessage(f"version: {__version__}  |  login: {SYS.OS_GET_LOGIN()}  |  author: pablogonzalezpila@gmail.com")
        self.ui.btn_load.setIcon(QIcon(os.path.join(self.dataPath, "load.ico")))
        self.ui.btn_save.setIcon(QIcon(os.path.join(self.dataPath, "save.ico")))
        ## CONNECTIONS
        self.ui.btn_load.clicked.connect(self.LOAD)
        self.ui.btn_save.clicked.connect(self.SAVE)
        self.ui.btn_fields.clicked.connect(self.FIELDS)
        self.ui.btn_add.clicked.connect(self.ROW_ADD)
        self.ui.btn_duplicate.clicked.connect(self.ROW_DUPLICATE)
        self.ui.btn_del.clicked.connect(self.ROW_DEL)
    
    def LOAD(self):
        '''
        '''
        filePath = QFileDialog.getOpenFileName(self, filter="*.csv;;All Files(*)")
        self.reportPath = SYS.PATH_BASENAME.GET(filePath[0], SYS.PATH_BASENAME.PATH)
        fileName = os.path.basename(filePath[0].split(".")[0])
        self.ui.tx_filename.setText(fileName)
        if fileName == None or fileName == "":
            return
        df = pd.read_csv(filePath[0])
        QT.TBL_POP_PANDAS_DF(self.ui.tbl_data, df)
    
    def FIELDS(self):
        '''
        '''
        tbl_data = QT.TBL_GET_PANDAS_DF(self.ui.tbl_data)
        fields = tbl_data.columns.values.tolist()
        FORM = QT.QLIST_FORM(
            LIST=fields, 
            Window_Title="TABLE FIELDS"
            )
        FORM.setWindowIcon(QIcon(os.path.join(self.dataPath, "csv.ico")))
        FORM.exec()
        new_tbl_data = pd.DataFrame()
        for field in FORM.value:
            if field in tbl_data.columns:
                new_tbl_data[field] = tbl_data[field]
            if field not in fields:
                new_tbl_data[field] = None
        QT.TBL_POP_PANDAS_DF(self.ui.tbl_data, new_tbl_data)

    def ROW_ADD(self):
        '''
        '''
        self.ui.tbl_data.setRowCount(self.ui.tbl_data.rowCount()+1)

    def ROW_DUPLICATE(self):
        '''
        '''
        currentRow = self.ui.tbl_data.currentRow()
        if not currentRow < 0:
            self.ui.tbl_data.insertRow(currentRow+1)
            for col in range(self.ui.tbl_data.columnCount()):
                value = QT.CELL_RD(self.ui.tbl_data, currentRow, col)
                QT.CELL_WR(self.ui.tbl_data, currentRow+1, col, value)

    def ROW_DEL(self):
        '''
        '''
        currentRow = self.ui.tbl_data.currentRow()
        if currentRow < 0:
            QT.INFOBOX("ATTENTIONS", "PLEASE, SELECT A VALID ROW", self.ICO_INFO)
            return
        self.ui.tbl_data.removeRow(currentRow)

    def SAVE(self):
        '''
        '''
        fileName = self.ui.tx_filename.text()
        if fileName == None or fileName == "":
            QT.INFOBOX("ATTENTION", "THE FILE NAME IS EMPTY", self.ICO_INFO)
            return
        
        # fileName = f"{fileName}.csv"
        # if not QT.YESNOBOX("SAVE TABLE", f"DO YOU WANT TO SAVE THE CURRENT TABLE LIKE <{fileName}> ?", WG.ICO_INFO):
        #     return

        fileName, _ = QFileDialog.getSaveFileName(
            None,
            caption="Save As", 
            directory=os.path.join(self.reportPath, fileName), 
            filter="CSV Files (*.csv);;All Files (*)",
            )
        if fileName:
            # print(fileName)
            tbl_data = QT.TBL_GET_PANDAS_DF(self.ui.tbl_data)
            tbl_data.to_csv(os.path.join(self.reportPath, fileName),header=True, index=False)


''' INIT SCRIPT 
________________________________________________________________________________________________ '''

if __name__ == "__main__":
    ## APPLICATION
    APP = QApplication(sys.argv)
    
    ## DARK MODE
    # if SYS.OS_GET_SYSTEM() == "Windows":
    import qdarktheme
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme(theme="dark", corner_shape="rounded")

    ## GUI
    WINDOW = MAIN_WINDOW()
    WINDOW.show()
    
    ## EXIT
    sys.exit(APP.exec())