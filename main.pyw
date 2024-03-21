''' CSV EDITOR | MAIN

TASK:
    - Usar dataclass o Enum para declarar los widgets

WARNINGS:
    - ...

________________________________________________________________________________________________ '''

__version__ = '2024.03.19'
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
from func_data import WG

''' GLOBAL VARIABLES '''
# from _data.main_GUI_ui import Ui_MainWindow


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
        uiFileName = r"main_GUI.ui"
        uiFile = os.path.join(self.dataPath, uiFileName)
        self.ui = uic.loadUi(uiFile, self)

        '''
        Formato .py con la GUI
        Al iniciar la GUI con la variable self.ui es necesario llamar luego todos los widgets con self.ui.statusBar (por ejemplo)
        Creo que es mas comodo hacer todo el proceso asi desde el principio y no seguir el metodo func_data WG.
        '''
        ## GUI .PY
        # from _data.main_GUI_ui import Ui_MainWindow
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
    
        ## GUI
        WG.ICO_INFO = QIcon(os.path.join(self.dataPath, "info.ico"))
        self.statusbar.showMessage(f"version: {__version__}  |  login: {SYS.OS_GET_LOGIN()}  |  author: pablogonzalezpila@gmail.com")
        
        ## CONNECTIONS
        WG.BTN_LOAD: QPushButton = self.btn_load
        WG.BTN_SAVE: QPushButton = self.btn_save
        WG.TX_FILENAME: QLineEdit = self.tx_filename
        WG.TBL_DATA: QTableWidget = self.tbl_data
        WG.BTN_FIELDS: QPushButton = self.btn_fields
        WG.BTN_ADD: QPushButton = self.btn_add
        WG.BTN_DUPLICATE: QPushButton = self.btn_duplicate
        WG.BTN_DEL: QPushButton = self.btn_del
        # 
        WG.BTN_LOAD.clicked.connect(self.LOAD)
        WG.BTN_SAVE.clicked.connect(self.SAVE)
        WG.BTN_FIELDS.clicked.connect(self.FIELDS)
        WG.BTN_ADD.clicked.connect(self.ROW_ADD)
        WG.BTN_DUPLICATE.clicked.connect(self.ROW_DUPLICATE)
        WG.BTN_DEL.clicked.connect(self.ROW_DEL)
    
    def LOAD(self):
        '''
        '''
        filePath = QFileDialog.getOpenFileName(self, filter="*.csv;;All Files(*)")
        self.reportPath = SYS.PATH_BASENAME.GET(filePath[0], SYS.PATH_BASENAME.PATH)
        fileName = os.path.basename(filePath[0].split(".")[0])
        WG.TX_FILENAME.setText(fileName)
        if fileName == None or fileName == "":
            return
        df = pd.read_csv(filePath[0])
        QT.TBL_POP_PANDAS_DF(WG.TBL_DATA, df)
    
    def FIELDS(self):
        '''
        '''
        tbl_data = QT.TBL_GET_PANDAS_DF(WG.TBL_DATA)
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
        QT.TBL_POP_PANDAS_DF(WG.TBL_DATA, new_tbl_data)

    def ROW_ADD(self):
        '''
        '''
        WG.TBL_DATA.setRowCount(WG.TBL_DATA.rowCount()+1)

    def ROW_DUPLICATE(self):
        '''
        '''
        currentRow = WG.TBL_DATA.currentRow()
        if not currentRow < 0:
            WG.TBL_DATA.insertRow(currentRow+1)
            for col in range(WG.TBL_DATA.columnCount()):
                value = QT.CELL_RD(WG.TBL_DATA, currentRow, col)
                QT.CELL_WR(WG.TBL_DATA, currentRow+1, col, value)

    def ROW_DEL(self):
        '''
        '''
        currentRow = WG.TBL_DATA.currentRow()
        if currentRow < 0:
            QT.INFOBOX("ATTENTIONS", "PLEASE, SELECT A VALID ROW", WG.ICO_INFO)
            return
        WG.TBL_DATA.removeRow(currentRow)

    def SAVE(self):
        '''
        '''
        fileName = WG.TX_FILENAME.text()
        if fileName == None or fileName == "":
            QT.INFOBOX("ATTENTION", "THE FILE NAME IS EMPTY", WG.ICO_INFO)
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
            tbl_data = QT.TBL_GET_PANDAS_DF(WG.TBL_DATA)
            tbl_data.to_csv(os.path.join(self.reportPath, fileName),header=True, index=False)


''' INIT SCRIPT 
________________________________________________________________________________________________ '''

if __name__ == "__main__":
    ## APPLICATION
    APP = QApplication(sys.argv)
    
    ## DARK MODE
    if SYS.OS_GET_SYSTEM() == "Windows":
        import qdarktheme
        qdarktheme.enable_hi_dpi()
        qdarktheme.setup_theme(theme="dark", corner_shape="rounded")

    ## GUI
    WINDOW = MAIN_WINDOW()
    WINDOW.show()
    
    ## EXIT
    sys.exit(APP.exec())