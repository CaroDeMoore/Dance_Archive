import pandas as pd
from typing import Optional, Dict, Tuple

from src.defs import *  # xxx kann raus?
from src.nodes import *


# Repräsentation einer xls-Zeile
class aLine:
    Groups: List[str] = []

    def __init__(
        self,
        pGroups: List[str],
        pFigurName: str,
        pFigComment: str,
        pLink: str,
        pLinkComment: str,
    ):
        for aGroup in pGroups:
            if aGroup == "":
                self.Groups.append(CellIsEmpty)
            else:
                self.Groups.append(aGroup)

        self.figureName = pFigurName
        self.figComment = pFigComment
        self.link = pLink
        self.linkComment = pLinkComment


def Read_AllFigures_from_Sheet(pXLS_FileName: str, pXLS_SheetName: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(  # type: ignore
        pXLS_FileName, sheet_name=pXLS_SheetName, engine="openpyxl"
    )
    df = df.fillna(CellIsEmpty)  # type: ignore Fehler bei Pandas 1.3.3
    # print(df.head(8))
    return df


def printXLS_Line(lineNr: int, outStr: str):
    print("XLS Line ", lineNr + 2, ": ", outStr)  # +2 wegen headerzeile
    print(f"XLS line {lineNr + 2}: {outStr}")


def Convert_DataFrame_to_Figures(
    df: pd.DataFrame, pDanceIndex: str
) -> cFigureList:  # -> Dict[str, cFigureList]:
    """
    DataFrame (ein Sheet mit Figuren) in Figurenobjekte konvertieren
    """

    # Figurenliste
    figureList: cFigureList = cFigureList()
    figureList.Dance = pDanceIndex

    """
    for iKey in XLS_Dance_SheetList:
        complete_dance_list[iKey] = cFigureList(
            cKursInfo("", "", "", "", "", titleText(""), ""),
            XLS_Dance_SheetList[iKey],
        )
    """

    objFig: Optional[cFigure] = None
    objFig = cFigure(
        pTanz=cDance(pDanceIndex),
        pFigureName="",
        pFigureComment="",
        pLink=cLink(None, ""),
        pGroupLessonDates=cGroupLessonDates(),
        pXlsLine=0,
    )

    # über alle Figuren eines Tanzes (Zeilen eines DataFrames)
    dfLine = START_ZEILE  # xxx65 ändern auf 1
    dfLastLine = len(df)
    while dfLine < dfLastLine:
        row = df.iloc[dfLine]

        admin = row.iloc[colAdmin]  # Spalte A mit line tags

        if admin == Line_Start:
            printXLS_Line(dfLine, Line_Start)
            dfLine = dfLine + 1
            continue

        if admin == Hide_Tag:
            printXLS_Line(dfLine, Hide_Tag)
            dfLine = dfLine + 1
            continue

        if admin == Line_End:
            printXLS_Line(dfLine, Line_End + "\n")
            dfLine = dfLine + 1
            break  # Ende

        # eine DataFrame-Zeile zerlegen

        # Gruppenspalten in eine Liste übernehmen   xxx96
        groups: List[str] = []
        for iGr in range(NUM_OF_GROUPs):
            groups.append(row.iloc[colFirstGroup + iGr])

        # Zeile in ein aLine-Objekt umwandeln
        iRow = aLine(
            pGroups=groups,  # Liste der Gruppen
            pFigurName=row.iloc[colFigur],
            pFigComment=row.iloc[colFigCom],
            pLink=row.iloc[colLink],
            pLinkComment=row.iloc[colLinkCom],
        )  # wert.strftime("%d.%m.%Y")

        GroupLessonDates: cGroupLessonDates = cGroupLessonDates()
        for i in range(NUM_OF_GROUPs):
            GroupLessonDates.Add(df.columns[colFirstGroup + i], row.iloc[colFirstGroup + i])

        # xls line defines a figure
        if admin == Line_Def:
            if admin == Line_Def:
                # eine Figur
                objFig = cFigure(
                    pTanz=cDance(pDanceIndex),
                    pFigureName=iRow.figureName,
                    pFigureComment=iRow.figComment,
                    pLink=cLink(iRow.link, iRow.linkComment),
                    pGroupLessonDates=GroupLessonDates,
                    pXlsLine=dfLine + 2,
                )
                objFig.set_role(cRoles.FIGURE_CARD)
                outStr: str = objFig.dance.dance + ", " + objFig.figureName
                printXLS_Line(dfLine, outStr)

        # xls line defines a link
        elif admin == Line_Link:
            thisLink = cLink(iRow.link, iRow.linkComment)
            if figureList:
                figureList.figures[-1].addLink(
                    thisLink
                )  # xxx figures wird unten nicht weitergereicht
            else:
                print("Warning: Link found before any figure definition.")

            outStr = thisLink.printen()
            printXLS_Line(dfLine, outStr)

        # xls line ist eine Kommentarzeile
        elif admin == Line_Comment:
            outStr = row.iloc[colLineCom]
            printXLS_Line(dfLine, outStr)

        # unbekannter Tag
        else:
            outStr: str = ""
            outStr = "Convert_DataFrame_to_Figures(): Unkown tag " + admin + " in line "
            printXLS_Line(dfLine, outStr)
            break

        if admin == Line_Def:  # nur anhängen, wenn eine Figur definiert wurde
            figureList.figures.append(objFig)

        dfLine = dfLine + 1

    # complete_dance_list[pDanceIndex].figureList = figures
    figureList.set_role(
        cRoles.FIGURE_CARD_LIST
    )  # xxx eigentlich sollte die Rolle schon beim Erstellen der Figur gesetzt werden
    return figureList
    # ende des DataFrames


def XLS_Reader(
    pXLS_FileName: Path, pSheetList: Dict[str, str]
) -> Tuple[Dict[str, cFigureList], List[str]]:
    """
    Einlesen aller Figuren aus der Excel-Datei und Umwandeln in Figurenobjekte
    Gruppen werden als Liste von Strings zurückgegeben (für alle Tänze gleich sind)
    """
    gruppen_liste: List[str] = []
    dance_dict: Dict[str, cFigureList] = {}
    print("reading from ", pXLS_FileName)

    # Schleife über alle Sheets/Tänze
    for iDance in pSheetList.keys():
        df: pd.DataFrame = Read_AllFigures_from_Sheet(pXLS_FileName, iDance)  # type: ignore
        # print(df)

        print(
            "************** Sheet",
            iDance,
            " *****************************",
            pSheetList[iDance],
        )

        # Figurenliste beim Tanz ablegen
        dance_dict[iDance] = Convert_DataFrame_to_Figures(df, iDance)

        if iDance == "ALL":  # xxx189
            break

        # Gruppennamen
        gruppen_liste = list(df.columns[colFirstGroup : colFirstGroup + NUM_OF_GROUPs])

    return dance_dict, gruppen_liste
