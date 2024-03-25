'''
CSV EDITOR

TASK:
    - pyuic6 -o _data/main_GUI_ui.py _data/main_GUI.ui
    - pyside6-uic -o _data/PySide_GUI.py _data/main_GUI.ui
    - pyarmor gen CSV_EDITOR.py _data

WARNINGS:
    - PyQt6 changed to PySide6, watch out for possible BUG(s) and Crashes 

________________________________________________________________________________________________ '''

__version__ = '2024.03.25'
__author__ = 'PABLO GONZALEZ PILA <pablogonzalezpila@gmail.com>'
__appName__ = 'CSV EDITOR'

''' SYSTEM LIBRARIES '''
import os, sys
import pandas as pd
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PySide6.QtWidgets import QPushButton, QTableWidget, QLineEdit
from PySide6.QtGui import QIcon, QFont

''' CUSTOM MAIN LIBRARIES '''
import pydeveloptools.func_system as SYS
import pydeveloptools.func_pyside6 as QT

''' APP EXTENSIONS '''
from _data.PySide_GUI import Ui_MainWindow


''' MAIN CLASS
________________________________________________________________________________________________ '''

class MAIN_WINDOW(QMainWindow):
    '''
    '''
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
        self.reportPath = self.sysPath
        # self.reportPath = os.path.join(self.sysPath, 'REPORTS')
        # if not os.path.exists(self.reportPath): 
        #     os.mkdir(self.reportPath)

        ## GUI .UI
        # uiFileName = r"main_GUI.ui"
        # uiFile = os.path.join(self.dataPath, uiFileName)
        # self.ui = uic.loadUi(uiFile, self)
        ## GUI .PY FILE
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## GUI / WIDGETS
        self.setWindowTitle("CSV Editor (by PABLO PILA)")
        self.setWindowIcon(QIcon(os.path.join(self.dataPath,'csv.ico')))
        self.ui.statusbar.showMessage(f"version: {__version__} | pablogonzalezpila@gmail.com")
        self.ui.btn_load.setIcon(QIcon(os.path.join(self.dataPath, "load.ico")))
        self.ui.btn_save.setIcon(QIcon(os.path.join(self.dataPath, "save.ico")))
        self.ICO_INFO = QIcon(os.path.join(self.dataPath, "info.ico"))
        TBL_HEADER = self.ui.tbl_data.horizontalHeader()
        HEADER_FONT = QFont()
        HEADER_FONT.setFamily("Arial Black")
        HEADER_FONT.setPointSize(14)
        # HEADER_FONT.setPixelSize(30)
        # HEADER_FONT.setBold(True)
        TBL_HEADER.setFont(HEADER_FONT)
        ## CONNECTIONS
        self.ui.btn_load.clicked.connect(self.LOAD)
        self.ui.btn_save.clicked.connect(self.SAVE)
        self.ui.btn_fields.clicked.connect(self.FIELDS)
        self.ui.btn_add.clicked.connect(self.ROW_ADD)
        self.ui.btn_duplicate.clicked.connect(self.ROW_DUPLICATE)
        self.ui.btn_del.clicked.connect(self.ROW_DEL)
    
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
            QT.INFOBOX("ATTENTION", "PLEASE, SELECT A VALID ROW", self.ICO_INFO)
            return
        self.ui.tbl_data.removeRow(currentRow)

    def LOAD(self):
        '''
        '''
        filePath = QFileDialog.getOpenFileName(self, filter="*.csv;;All Files(*)")
        self.reportPath = SYS.PATH_BASENAME.GET(filePath[0], SYS.PATH_BASENAME.PATH)
        fileName = os.path.basename(filePath[0].split(".")[0])
        self.ui.tx_filename.setText(fileName)
        if fileName == None or fileName == "":
            return
        try:
            df = pd.read_csv(filePath[0])
            QT.TBL_POP_PANDAS_DF(self.ui.tbl_data, df)
        except Exception as e:
            QT.INFOBOX("ERROR !!", e, self.ICO_INFO)

    def SAVE(self):
        '''
        '''
        fileName = self.ui.tx_filename.text()
        if fileName == None or fileName == str():
            QT.INFOBOX("ATTENTION", "THE FILE NAME IS EMPTY", self.ICO_INFO)
            return

        ## PyQt6
        # fileName, _ = QFileDialog.getSaveFileName(
        #     None,
        #     caption="Save As", 
        #     directory=os.path.join(self.reportPath, fileName), 
        #     filter="CSV Files (*.csv);;All Files (*)",
        #     )
        
        ## PySide6
        fileName, _ = QFileDialog.getSaveFileName(
            parent= None,
            caption= "Save As", 
            dir= os.path.join(self.reportPath, fileName), 
            filter= "CSV Files (*.csv);;All Files (*)",
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

    # from PySide6.QtWidgets import QStyleFactory
    # APP.setStyle(QStyleFactory.create("Fusion"))

    # from qt_material import apply_stylesheet
    # THEMES = [
    #     'dark_amber.xml',
    #     'dark_blue.xml',
    #     'dark_cyan.xml',
    #     'dark_lightgreen.xml',
    #     'dark_pink.xml',
    #     'dark_purple.xml',
    #     'dark_red.xml',
    #     'dark_teal.xml',
    #     'dark_yellow.xml',
    #     'light_amber.xml',
    #     'light_blue.xml',
    #     'light_cyan.xml',
    #     'light_cyan_500.xml',
    #     'light_lightgreen.xml',
    #     'light_pink.xml',
    #     'light_purple.xml',
    #     'light_red.xml',
    #     'light_teal.xml',
    #     'light_yellow.xml'
    # ]
    # apply_stylesheet(APP, theme=THEMES[9])

    ## GUI
    WINDOW = MAIN_WINDOW()
    WINDOW.show()
    
    ## EXIT
    sys.exit(APP.exec())