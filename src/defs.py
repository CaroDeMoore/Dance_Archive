from typing import Dict
import json
from pathlib import Path
from typing import Any

DEBUG: int = 0

#     Dateinamen und Pfade
# -----------------------------------------------------------------------------
"""
    Archiv-Ordner
        - Figuren und Folgen - Die WebSeite.html
        - main.py        
        - videothek (Ordner)
        - html (Ordner, hier wird die HTML-Seite ausgegeben)
        - styles.css

    Pfadangaben sind relativ zum main.py
    Alle Angaben sind hier noch Strings, die in main.PathReader() aufgelöst werden.
    StyleSheet liegt neben main.py

"""
# Archiv: dieser Ordner in Tanzen enthält:
#       - Datenbank, Unterarchiven, Source
ARCHIVE_BASE_relPath: str = "../"   # Bezug Archiv\Source\ nach Archv\

# !!!!! ab jetzt sind Bezüge relativ zu ARCHIVE_BASE_DIR !!!!!

# XLS Eingabe-Datei
XLS_InputFileName: str = "Figuren und Folgen - Die Datenbank.xlsm"

# Name des Sub-Archiv in Archiv/
ARCHIV_SUB_relDIR: str = "ArchivA/"  

# HTML-Ausgabedatei
HTML_OutputFileName: str = "Figuren und Folgen - Die WebSeite.html"
HTML_Output_relative_Path: str = ARCHIVE_BASE_relPath + ARCHIV_SUB_relDIR + "/html" 

HTML_StylesheetName: str = "styles.css" 

# Pfad von den Tanzseiten zur Videothek (benutzt in cLink)
VIDEO_Folder: str = "../../videothek"  

# XLS-Tabellenblätter
XLS_Dance_SheetList: Dict[str, str] = {
    "CC": "Cha Cha Cha",
    "JI": "Jive",
    "RB": "Rumba",
    "SB": "Samba",
    "DF": "Discofox",
    "QS": "Quickstep",
    "SF": "Slowfox",
    "SW": "Langsamer Walzer",
    "AS": "American Smooth",
    "TG": "Tango",
    "VW": "Wiener Walzer",
    "SS": "Salsa",
    "LAT": "Latein",
    "STD": "Standard",
    "ALL": "Alle Tänze",
}

# Spalten defs
colAdmin: int = 0
colLineCom: int = 1
#       Spalte, ab der die Gruppen stehen
colFirstGroup: int = 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#    Anzahl der Gruppen

NUM_OF_GROUPs: int = 10

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

START_ZEILE = 0
colFigur: int = colFirstGroup + NUM_OF_GROUPs
colFigCom: int = colFigur + 1
colLink: int = colFigCom + 1
colLinkCom: int = colLink + 1

CellIsEmpty = ""
Line_Comment = "com"
Line_Def = "def"
Line_Link = "link"
Line_End = "end"
Line_Start = "start"
Hide_Tag = "filter"

# STYLES
STY_NAVIGATION_BUTTON = 0
STY_NAVIGATION_ITEM = 1
STY_MAINPAGE = 2

H1 = "h1"
H2 = "h2"
H3 = "h3"

def read_config(configFile: str) -> None:
    config_file = Path(__file__).parent / configFile

    with config_file.open("r", encoding="utf-8") as file:        
        config =json.load(file)   

    # Werte aus config.json übergeben

    # Gruppen
    global NUM_OF_GROUPs
    NUM_OF_GROUPs = config["groups"]["NUM_OF_GROUPs"]

    # Spalten-Nummern
    global colAdmin
    colAdmin = config["columns"]["admin"]
    global colLineCom
    colLineCom = config["columns"]["line_comment"]
    global colFirstGroup
    colFirstGroup = config["columns"]["first_group"]
    global colFigur
    colFigur = config["columns"]["figure"]
    global colFigCom
    colFigCom = config["columns"]["figure_comment"]
    global colLink      
    colLink = config["columns"]["link"]
    global colLinkCom
    colLinkCom = config["columns"]["link_comment"]

    # Sheet-Namen für die Tänze
    global XLS_Dance_SheetList
    XLS_Dance_SheetList = config["xls"]["dance_sheets"]

    # Werte für die Line-Kommandos 
    global CellIsEmpty
    CellIsEmpty = config["line_commands"]["CellIsEmpty"]
    global Line_Comment
    Line_Comment = config["line_commands"]["Line_Comment"]
    global Line_Def
    Line_Def = config["line_commands"]["Line_Def"]
    global Line_Link
    Line_Link = config["line_commands"]["Line_Link"]
    global Line_End
    Line_End = config["line_commands"]["Line_End"]
    global Line_Start
    Line_Start = config["line_commands"]["Line_Start"]
    global Hide_Tag
    Hide_Tag = config["line_commands"]["Hide_Tag"]
    
    # Pfade
    global ARCHIVE_BASE_relPath
    ARCHIVE_BASE_relPath = config["path"]["archive"]
    global ARCHIV_SUB_relDIR
    ARCHIV_SUB_relDIR = config["path"]["archive_sub"]
    global HTML_Output_relative_Path
    HTML_Output_relative_Path = config["path"]["html"]
    global VIDEO_Folder
    VIDEO_Folder = config["path"]["video"]

    # Dateien
    global XLS_InputFileName
    XLS_InputFileName = config["file"]["xls_input"]
    global HTML_OutputFileName
    HTML_OutputFileName = config["file"]["html_output"]
    global HTML_StylesheetName
    HTML_StylesheetName = config["file"]["stylesheet"]

