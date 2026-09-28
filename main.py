import argparse

from src.nodes import *
from src.defs import *
from src.XLS_Reader import *
from src.Visitor_HTML import HTMLVisitor
from pathlib import Path

# from Visitor_LATEX import LATEXVisitor

class PathBuilder:
    """
    Baut alle benötigten Pfade. 
    Muss in main.py stehen.
    """

    def __init__(self, pARCHIVE_BASE_relPath: str, pARCHIV_SUB_relDIR: str) -> None:

        # Ordner von main.py bzw. main.exe
        self.WORK_absDIR = Path(__file__).resolve().parent
        # Archiv, eins über workdir
        self.ARCHIVE_BASE_absDIR: Path = (self.WORK_absDIR / pARCHIVE_BASE_relPath).resolve()  # ARCHIVE_BASE_DIR z.Bsp. "../"  
        # Zielordner für das Archiv
        self.ARCH_SUB_absDIR: Path = (self.ARCHIVE_BASE_absDIR / pARCHIV_SUB_relDIR).resolve()   # z.Bsp. "Archiv/ArchivA/"

        # Pfad zur Excel-Datei, wird im XLS_Reader genutzt
        self.XLS_Input_absDIR: Path = self.ARCHIVE_BASE_absDIR

        # html-Ausgabeordner
        self.HTML_Output_absDir: Path = self.ARCH_SUB_absDIR / "html"  # z.Bsp. "Archiv/ArchivA/html/"
        self.HTML_Output_relPath: Path = Path(pARCHIV_SUB_relDIR)  / "html" 

        print("WORK_absDIR:", self.WORK_absDIR)
        print("ARCHIVE_BASE_absDIR:", self.ARCHIVE_BASE_absDIR)
        print("ARCH_SUB_absDIR:", self.ARCH_SUB_absDIR)
        print("XLS_Input_absDIR:", self.XLS_Input_absDIR)
        print("HTML_Output_absDir:", self.HTML_Output_absDir)
        print("HTML_Output_relPath:", self.HTML_Output_relPath)

if __name__ == "__main__":

    # print("\033c", end="")    # clear console

    # Argumente parsen; default-Werte aus defs.py 
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputPath", type=str, default=ARCHIVE_BASE_relPath)
    parser.add_argument("--outputPath", type=str, default=ARCHIV_SUB_relDIR)
    parser.add_argument("--XLS_InputFileName", type=str, default=XLS_InputFileName)
    args = parser.parse_args()
    print("InputPath:", args.inputPath)
    print("OutputPath:", args.outputPath)
    print("Database:", args.XLS_InputFileName)

    read_config("../src/config.json")  # config.json einlesen,     

    # Pfade erzeugen
    PathInfo = PathBuilder(args.inputPath, args.outputPath)

    # alle mögliche Informationen
    GenericInfo: cGenInfo = cGenInfo(
        "Archiv",
        pWORK_absDIR=PathInfo.WORK_absDIR,
        pARCH_SUB_absDIR=PathInfo.ARCH_SUB_absDIR,
        pXLS_Input_absDIR=PathInfo.XLS_Input_absDIR,        
        pHTML_Output_absDir=PathInfo.HTML_Output_absDir,        
        pHTML_Output_relPath=PathInfo.HTML_Output_relPath,
        pXLS_InputFileName=args.XLS_InputFileName,        
        pHTML_OutputFileName=HTML_OutputFileName,        
    )

    # Figurenliste aus Excel lesen
    complete_dance_list: cDanceDict = cDanceDict()
    GruppenNamen: List[str] = []  # für alle Tänze gleich!
    complete_dance_list.DanDi_raw, GruppenNamen = XLS_Reader(
        GenericInfo.XLS_Input_absDIR / GenericInfo.XLS_InputFileName,
        XLS_Dance_SheetList,
    )

    # Info-Dict zu allen Kursen:
    #   Dict[GroupName -> KursInfo]
    CoursesSpecificInfo: Dict[str, cKursInfo] = {}

    # Gruppendaten aller Gruppen setzen
    lastGroup = len(GruppenNamen)
    for iGruppenNummer in range(lastGroup):
        GroupName: str = GruppenNamen[iGruppenNummer]
        KursInformation: cKursInfo = cKursInfo(
            pInfo="Dies sind sonstige Informationen zum Tanzkurs der "
            + GroupName
            + ".",
            pGroupName=GroupName,
            pKursTitel="Archiv - " + GroupName,
            pKursFilter="",
        )
        CoursesSpecificInfo[GroupName] = KursInformation

    TSV_Tanz: cTSV_TANZ = cTSV_TANZ(
        GenericInfo, CoursesSpecificInfo, complete_dance_list
    )

    html_visitor: HTMLVisitor = HTMLVisitor()

    TSV_Tanz.accept(html_visitor)

    print("Done.\n")
