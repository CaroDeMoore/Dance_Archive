from abc import ABC  # , abstractmethod

from src.nodes import *

"""
    base.py 
        Enthält die abstrakte Visitor-Basis (Interface).
        Definiert sämtliche Knoten: visit_body(), visit_header(), usw.
"""


class cVisitor(ABC):

    # @abstractmethod
    def visit_header(self, node: "cDokumentHeader") -> str:
        return ""

    # @abstractmethod
    def visit_link(self, node: "cLink") -> str:
        return ""

    # @abstractmethod
    def visit_figure(self, node: "cFigure") -> str:
        return ""

    # @abstractmethod
    def visit_dance(self, node: "cDance") -> str:
        return ""

    # @abstractmethod
    def visit_TSV_Tanz(self, node: "cTSV_TANZ") -> str:
        return ""

    # @abstractmethod
    def visit_otherinfos(self, node: "cKursInfo") -> str:
        return ""

    def visit_figureListHeadline(self, node: "cFigureList_HeadLine") -> str:
        return ""

    # @abstractmethod
    def visit_figureList(self, node: "cFigureList") -> str:
        return ""

    # @abstractmethod
    def visit_ToC(self, node: "cToC") -> str:
        return ""

    # @abstractmethod
    def visit_DanDi(self, node: "cDanceDict") -> str:
        return ""

    # @abstractmethod
    def visit_DocumentTitle(self, node: "cDokTitle") -> str:
        return ""

    # @abstractmethod
    def visit_figure_headline(self, node: "cFigureHeadline") -> str:
        return ""

    # @abstractmethod
    def visit_LinkList(self, node: "cLinkListe") -> str:
        return ""

    # @abstractmethod
    def visit_MainPage(self, node: "cMainPage") -> str:
        return ""

    ##@abstractmethod
    def visit_SubPage(self, node: "cSubPage") -> str:
        return ""

    # @abstractmethod
    def visit_Button(self, node: "cButton") -> str:
        return ""

    # @abstractmethod
    def visit_ButtonList(self, node: "cButtonList") -> str:
        return ""

    # @abstractmethod
    def visit_ToC_Entry(self, node: "cToC_Entry") -> str:
        return ""
