"""
nodes.py
    definiert die Datenstruktur (Body, Header, Title, Nav, …).
    → rein strukturell, keine Formatierungslogik.
"""

from abc import ABC, abstractmethod

# from pydoc import text
from tkinter import messagebox
from urllib.parse import quote
from tkinter import messagebox

# from importlib.resources import path
from typing import List
from enum import Enum

from src.Visitor_Base import cVisitor
from src.defs import *
from src.style_mapping import cRoles
from pathlib import Path
import re


# alles außer Zahlen und Buchstaben wird durch _ ersetzt
def cleanFromSpecialChars(inp: str) -> str:
    inp = re.sub(r"[^\w]+", "_", inp, flags=re.UNICODE)
    return inp.strip("_")


# Basisklasse für die Visitor-Klassen
class Node(ABC):
    def __init__(self):
        self.role: str = self.__class__.__name__ + "_default_role"  # default_role

    @abstractmethod
    def accept(self, visitor: cVisitor) -> str: ...  # ...: siehe Ellipsis

    def set_role(self, pRole: str):
        self.role = pRole


class cLinkType(str, Enum):
    FILE = "file"
    URL = "url"
    NIX = "nix"


class cLink(Node):
    def __init__(self, pLink: str | None = None, pComment: str = ""):
        super().__init__()

        self.linkComment = pComment

        if pLink is None:
            self.LinkType = cLinkType.NIX
            self.link = ""
        elif pLink.startswith(("http://", "https://")):
            self.link = pLink
            self.LinkType = cLinkType.URL
        else:  # Datei-Link
            path = (
                Path(VIDEO_Folder) / pLink
            )  # Achtung: Video-Ordner ist in pLink nicht enthalten, die Zelle enthält nur den Namen
            self.LinkType = cLinkType.FILE

            if path.is_absolute():
                self.link = path.resolve()
                text: str = (
                    f"Warning: Absolute path '{self.link}' found. \n\n Videos dürfen nur im Ordner videothek liegen!"
                )
                messagebox.showinfo("Absoluter Pfad", text)
            else:
                # relative Pfade werden relativ zum xls interpretiert
                self.link = quote(path.as_posix())  # mache aus \ einen /

    def printen(self) -> str:
        outStr = ""
        outStr = str(self.link) + " , "
        outStr += self.linkComment
        outStr = outStr
        return outStr

    def set_role(self, pRole: str):
        self.role = pRole

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_link(self)


class cLinkListe(Node):
    def __init__(self):
        super().__init__()
        self.Links: List[cLink] = []

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_LinkList(self)


class cLessonDate:
    def __init__(self, pLessonDate: str, pGroupTime: str):
        super().__init__()
        self.lessonDate: str = pLessonDate
        self.groupTime: str = pGroupTime

    def printen(self) -> str:
        outStr: str = ""
        outStr = self.lessonDate + " , " + self.groupTime
        return outStr


class cGroupLessonDates:
    def __init__(self):
        super().__init__()
        self.Dates: Dict[str, str] = {}  # Dict[GroupKey -> LessonDate]

    def Add(self, pGroup: str, pLessonDate: str):
        self.Dates[pGroup] = pLessonDate

    def printen(self) -> str:
        outStr: str = ""
        for pGroup in self.Dates:
            outStr += f"{pGroup}: {self.Dates[pGroup]} "

        return outStr


class cDance(Node):
    def __init__(self, pDance: str):
        super().__init__()
        self.dance = pDance

    def getDance(self, pDanceIndex: str) -> str:
        if pDanceIndex not in XLS_Dance_SheetList.keys():
            return "Dance not found"
        else:
            return XLS_Dance_SheetList[pDanceIndex]

    def printen(self) -> str:
        outStr = ""
        outStr = self.dance
        return outStr

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_dance(self)


# Überschrift für jede Figur
class cFigureHeadline(Node):
    def __init__(
        self, pFigureTitle: str, pLessonDate: str, pXLS_Line: int, pDance: str
    ):
        super().__init__()
        self.figureTitle = pFigureTitle
        self.lessonDate = pLessonDate
        self.XLS_Line = pXLS_Line
        self.Dance = pDance

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_figure_headline(self)


class cFigure(Node):
    filter_group: str
    filter_lessonDate: str

    def __init__(
        self,
        pTanz: cDance,
        pFigureName: str,
        pFigureComment: str,
        pLink: cLink,
        pGroupLessonDates: cGroupLessonDates,
        pXlsLine: int,
        css: str = "",
    ):
        super().__init__()
        self.dance: cDance = pTanz
        self.figureName = pFigureName
        self.figureComment = pFigureComment
        self.linkListe: cLinkListe = cLinkListe()
        self.linkListe.Links.append(pLink)
        self.linkListe.set_role(cRoles.FIGURE_LINK_LIST_TABLE)
        self.figureLessonDates: cGroupLessonDates = pGroupLessonDates
        self.outStr = ""
        # Info, in welcher gefilterten Liste sich die Figur befindet
        self.filter_group = ""
        self.filter_lessonDate = ""
        self.XLS_Line = pXlsLine
        self.headline: cFigureHeadline = cFigureHeadline("", "", 0, "")
        super().__init__()  # setzt role auf Klassenname

    def set_role(self, pRole: str):
        self.role = pRole

    def copy(self) -> "cFigure":
        new_figure = cFigure(
            self.dance,
            self.figureName,
            self.figureComment,
            cLink("", ""),  # xxx184
            cGroupLessonDates(),
            self.XLS_Line,
        )
        new_figure.linkListe = self.linkListe
        new_figure.figureLessonDates = self.figureLessonDates
        new_figure.set_role(self.role)
        new_figure.dance = self.dance
        new_figure.figureComment = self.figureComment
        new_figure.figureName = self.figureName
        new_figure.XLS_Line = self.XLS_Line
        return new_figure

    def setHeadLine(self, gr: str):
        """
        Setzt die headline für die Figur mit dem Lesson-Date der übergebenen Gruppe.
        """
        if gr != "":  # leer für Gruppe All
            lessonDate: str = self.figureLessonDates.Dates[gr]
        else:
            lessonDate = ""

        self.headline = cFigureHeadline(
            self.figureName,
            lessonDate,
            self.XLS_Line,
            self.dance.dance,
        )

    def getLessonDate(self, pGroupKey: str) -> str:
        return self.figureLessonDates.Dates[pGroupKey]

    def set_assigned_Filter(self, pGroupKey: str, pLessonDate: str):
        """
        Filtereinstellungen für die Figur speichern
        Wird aufgerufen, wenn die Figur in eine gefilterte Liste aufgenommen wird
        """
        self.filter_group = pGroupKey
        self.filter_lessonDate = pLessonDate

    def addLink(self, pLink: cLink):
        self.linkListe.Links.append(pLink)

    def setGroup(self, key: str, pLessonDate: str):

        self.figureLessonDates.Dates[key] = pLessonDate

    def checkGroupe(self, key: str) -> bool:
        if self.figureLessonDates.Dates[key] != CellIsEmpty:
            return True
        else:
            return False

    def printen(self) -> str:
        self.outStr: str = ""
        self.outStr = self.dance.printen() + ",   " + self.figureName + ",   "

        self.outStr += self.figureLessonDates.printen()

        for li in self.linkListe.Links:
            self.outStr += li.printen()

        self.outStr += "\n"
        return self.outStr

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_figure(self)


class cDokumentHeader(Node):
    def __init__(self, h1: str):
        super().__init__()
        self.h1 = h1
        self.css: str = cDokumentHeader.__name__ + "_css"

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_header(self)


class cKursInfo(Node):
    def __init__(
        self,
        pInfo: str,
        pGroupName: str,
        pKursTitel: str,
        pKursFilter: str,
    ):
        super().__init__()
        self.info: str = pInfo
        self.GroupName: str = pGroupName
        self.DokTitle: cDokTitle = cDokTitle(pKursTitel)
        self.DokTitle.set_role(cRoles.PAGE_TITLE_H1)

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_otherinfos(self)


class cFigureList_HeadLine(Node):
    def __init__(self, pGroup: str, pDance: str):
        super().__init__()
        self.Group: str = pGroup
        self.Dance: str = pDance
        self.css: str = cFigureList_HeadLine.__name__ + "_css"

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_figureListHeadline(self)


class cFigureList(Node):
    Group: str
    Dance: str
    headline: "cDokTitle"

    def __init__(self):
        super().__init__()
        self.figures: List[cFigure] = []
        self.ToC: cToC = cToC()
        self.ToC.set_role(cRoles.TOC_DANCES)
        self.Group = ""
        self.Dance = ""  # gesetzt im XLS_Reader.Convert_DataFrame_to_Figures()
        outStr: str = f"<h2>{self.Group} - {self.Dance}</h2>"
        self.headline = cDokTitle(outStr)

    def setGroup(self, pGroup: str):
        self.Group = pGroup
        # self.headline.Group = pGroup

    def setDance(self, pDance: str):
        self.Dance = pDance  # gesetzt im XLS_Reader.Convert_DataFrame_to_Figures()
        # self.headline.Dance = pDance

    # gibt eine List[str] der Figurennamen zurück
    def getNameList(self) -> List[str]:
        result: List[str] = []
        for i in range(len(self.figures)):
            result.append(self.figures[i].figureName)
        return result

    def buildTOC(self) -> "cToC":
        toc: cToC = cToC()
        for iFigure in self.figures:
            toc.addEntry(
                cToC_Entry(
                    pLink=f"#{cleanFromSpecialChars(iFigure.figureName)}",
                    pText=iFigure.figureName,
                )
            )
        self.ToC = toc
        return toc

    def getAll(self) -> List[cFigure]:
        return self.figures

    def getKursInfo(self) -> str:
        return self.Group

    def getDance(self) -> str:
        return self.Dance

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_figureList(self)


# Dict das jedem Tanz eine Liste mit Figuren zuordnet
class cDanceDict(Node):
    def __init__(self):
        super().__init__()
        # Dict: Tanz -> Figurenliste (nur Tänze -> FigurenListen, keine Metadaten)
        self.DanDi_raw: Dict[str, cFigureList] = {}
        self.KursInfo: cKursInfo = cKursInfo("", "", "", "")
        # Schlüssel init
        for iKey in XLS_Dance_SheetList:
            self.DanDi_raw[iKey] = cFigureList()
        self.ToC: cToC = cToC()

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_DanDi(self)

    def addFigure(self, pDanceIndex: str, pFig: "cFigure"):
        self.DanDi_raw[pDanceIndex].figures.append(pFig)

    def buildTOC(self) -> "cToC":
        """
        TOC aus DanceDict erstellen
        """
        toc: cToC = cToC()
        for iDance in self.DanDi_raw.keys():
            if len(self.DanDi_raw[iDance].figures) != 0:
                ThisEntry: cToC_Entry = cToC_Entry(
                    pLink=iDance + ".html", pText=XLS_Dance_SheetList[iDance]
                )
                ThisEntry.set_role(cRoles.MAL_SEHEN)  # xxx
                toc.entries.append(ThisEntry)

        self.ToC = toc
        return toc

    # gibt eine List[str] zurück, die alle Tänze enthält, zu denen es Figuren gibt
    def getListOfDances_Long(self) -> List[str]:
        res: list[str] = []
        for iDance in self.DanDi_raw.keys():
            if len(self.DanDi_raw[iDance].figures) != 0:
                res.append(XLS_Dance_SheetList[iDance])
        return res

    def getListOfDances_Short(self) -> List[str]:
        res: list[str] = []
        for iDance in self.DanDi_raw.keys():
            if len(self.DanDi_raw[iDance].figures) != 0:
                res.append(iDance)
        return res

    def filter_Gr(self, pGrKey: str) -> Dict[str, cFigureList]:
        # result:Dict[str ,List[cFigure]] = Dict{"", List[cFigure(cDance(""), "","",cLink("",""),cGroupLessonDates("","","",""), "")}

        result: Dict[str, cFigureList] = {}

        # über alle Tänze
        for iDance, allFigureList in self.DanDi_raw.items():
            filteredFigureList_raw: List[cFigure] = []
            ThisTOC: cToC = cToC()

            # über alle Figuren von iDance
            for iFig in allFigureList.figures:
                # aFig:cFigure=cFigure()
                aFig = iFig.copy()
                if aFig.checkGroupe(pGrKey):  # Prüfung auf Gruppe
                    # Filtereinstellungen speichern
                    aFig.set_assigned_Filter(pGrKey, aFig.getLessonDate(pGrKey))
                    # Figur zur gefilterten Liste hinzufügen
                    filteredFigureList_raw.append(aFig)

                    # TOC
                    TOC_ThisEntry: cToC_Entry = cToC_Entry(
                        pLink=f"#{cleanFromSpecialChars(aFig.figureName)}",
                        pText=aFig.figureName,
                    )
                    TOC_ThisEntry.set_role(cRoles.NAV_FIGURES)

                    ThisTOC.set_role(cRoles.TOC_DANCES)
                    ThisTOC.addEntry(TOC_ThisEntry)

            if len(filteredFigureList_raw) > 0:
                filteredFigureList: cFigureList = cFigureList()
                filteredFigureList.ToC = ThisTOC
                filteredFigureList.figures = filteredFigureList_raw

                filteredFigureList.setDance(iDance)
                filteredFigureList.setGroup(pGrKey)

                result[iDance] = filteredFigureList

        return result


class cToC_Entry(Node):
    # xxx hier die selbe Klasse wie für die Buttonlist!
    # Es sind beides Linklisten, sie sehen nur anders aus
    def __init__(self, pLink: str, pText: str):
        super().__init__()
        self.LinkStr: str = pLink
        self.LinkPosix: str = quote(Path(pLink).as_posix())
        self.text: str = pText
        super().__init__()

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_ToC_Entry(self)


class cToC(Node):
    # Klasse für das TOC der Tänze (einer Filterung)
    def __init__(self):
        super().__init__()
        self.Links: List[str] = []
        self.Texte: List[str] = []
        self.entries: List[cToC_Entry] = []
        super().__init__()

    def set_role(self, pRole: str):
        return super().set_role(pRole)

    def setLinkTexts(self, pTexte: List[str]):
        self.Texte = pTexte

    def setLinkList(self, pLinks: List[str]):
        self.Links = pLinks

    def addEntry(self, pEntry: "cToC_Entry"):
        self.entries.append(pEntry)

    def match(self):
        for i in range(len(self.Texte)):
            self.entries.append(cToC_Entry(self.Links[i], self.Texte[i]))

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_ToC(self)


class cGenInfo:
    """
    Pfadangaben sind relativ zum main
    """

    def __init__(
        self,
        pGenInfo: str,
        pWORK_absDIR: Path,
        pXLS_Input_absDIR: Path,
        pHTML_Output_absDir: Path,
        pXLS_InputFileName: str,
        pHTML_OutputFileName: str,
        pHTML_Output_relPath: Path,
        pARCH_SUB_absDIR: Path,
    ) -> None:
        super().__init__()
        self.description: str = pGenInfo

        # Pfad zur Excel-Datei, wird im XLS_Reader genutzt
        self.BASE_DIR: Path = pWORK_absDIR
        self.XLS_Input_absDIR: Path = pXLS_Input_absDIR
        self.HTML_Output_absDir: Path = pHTML_Output_absDir  # Pfad zum Ausgabeordner
        self.HTML_Output_relPath: Path = pHTML_Output_relPath
        self.XLS_InputFileName: str = pXLS_InputFileName
        self.HTML_OutputFileName: str = pHTML_OutputFileName
        self.ARCH_SUB_absDIR: Path = pARCH_SUB_absDIR
        self.dummy: str = ""


class cTSV_TANZ(Node):
    def __init__(
        self,
        pGenericInfo: cGenInfo,
        pAllKursInfo: Dict[str, cKursInfo],
        pComplDanceDict: cDanceDict,
    ):
        super().__init__()
        self.CompleteDanceDict: cDanceDict = pComplDanceDict
        self.AllKursInfo: Dict[str, cKursInfo] = pAllKursInfo
        self.GenInfo: cGenInfo = pGenericInfo
        self.MainPage: cSubPage = cSubPage()
        self.SubPages: List[cSubPage] = []

    def getGroupList(self) -> List[str]:
        ret: List[str] = []
        for iGr in self.AllKursInfo.values():
            ret.append(cleanFromSpecialChars(iGr.GroupName))
        return ret

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_TSV_Tanz(self)


# Titel des gesamten Dokumentes
class cDokTitle(Node):
    def __init__(self, pDocTitle: str):
        super().__init__()
        self.text = pDocTitle
        self.role: str = ""

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_DocumentTitle(self)


class cButton(Node):
    def __init__(self, pLink: str, pText: str):
        super().__init__()
        self.link: str = pLink
        self.text = pText
        self.css: str = cButton.__name__ + "_css"

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_Button(self)


class cButtonList(Node):
    def __init__(self):
        super().__init__()
        self.elem: List[cButton] = []
        self.link: str = ""
        self.text = ""
        self.css: str = cButtonList.__name__ + "_css"

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_ButtonList(self)


# sup pages für die Gruppen (enthält ein Inhaltsverzeichnis der Tänze (cTOC_Dance))
# (hier keine Figure-List, da diese uU später eigene Seiten werden)
class cSubPage(Node):
    html: str = ""
    role: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.TOC: cToC = cToC()
        self.docTitle: cDokTitle = cDokTitle("")
        self.gruppe: str = ""

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_SubPage(self)

    def set_role(self, pRole: str):
        self.role = pRole


# die Hautpseite mit den buttons zu den sub-pages
class cMainPage(Node):
    def __init__(self):
        super().__init__()
        self.buttonlist: cButtonList = cButtonList()
        self.DocTitle: cDokTitle = cDokTitle("")
        self.css: str = cMainPage.__name__ + "_css"

    def accept(self, visitor: cVisitor) -> str:
        return visitor.visit_MainPage(self)


class c_tag_p(Node):
    def __init__(self, pText: str):
        super().__init__()
        self.text = pText

    def accept(self, visitor: cVisitor) -> str:
        return ""
