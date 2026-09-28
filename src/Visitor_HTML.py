# from typing import List

from src.Visitor_Base import cVisitor
from src.nodes import *
from src.html_box import *
from src.style_mapping import cRoles, get_map_classes
from pathlib import Path




def build_YouTubeLink(target: str, text: str) -> str:
    #   <a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" rel="noopener noreferrer">
    #        Video ansehen
    # </a>
    outStr: str = ""
    outStr = f"""
        <a 
        href="{target}" target="_blank" rel="noopener noreferrer">{text}
        </a>
        """
    return outStr


def build_Download_Link(id: str, text: str) -> str:
    #   <a href="https://drive.google.com/uc?export=download&id=ABC123" download>
    #       MeinFile.txt herunterladen
    #   </a>
    outStr: str = ""
    outStr = f"""
        <a 
        href="https://drive.google.com/uc?export=download&id={id}" download>{text}
        </a>
        """
    return outStr


# baut ein einzeiliges <div>class=... id=...</div>
def build_divNcl(pText: str, pClass: str = "", id: str = "") -> str:
    outStr: str = ""
    if id == "":
        outStr = f'<div class="{pClass}">{pText}>'
    else:
        outStr = f'<div class="{pClass}" id="{id}">{pText}>'
    return outStr


def build_divCl(pText: str, pClass: str = "", id: str = "") -> str:
    outStr: str = replace_last_char(build_divNcl(pText, pClass, id), "</div>")
    return outStr


def replace_last_char(s: str, replacement: str) -> str:
    outstr: str = ""
    if not s:
        outstr = replacement
    else:
        outstr = s[:-1] + replacement
    return outstr


def build_href(pTarget: str, pText: str, pStyleClass: str = "") -> str:
    outSt: str = ""
    if pStyleClass == "":
        outSt = f'<a href="{pTarget}">{pText}</a>'
    else:
        outSt = f'<a href="{pTarget}" class="{pStyleClass}" >{pText}</a>'
    return outSt


# baut einen Eintrag im Inhaltsverzeichnis der Tänze
def build_TOC_Entry_Dance(pPath: str, pDance: str) -> str:
    outStr: str = ""

    fn: str = pPath + pDance.replace(" ", "_") + ".html"
    outStr = f"""<li><a href="{fn}">{pDance}</a></li>"""
    return outStr


def buildAnkerForFigure(pName: str) -> str:
    return cleanFromSpecialChars(pName)


# baut einen Eintrag im Inhaltsverzeichnis Figuren
#   <a href="#rumba">Zur Rumba springen</a>
def build_TOC_Entry_Figure(pFigureName: str) -> str:
    outStr: str = ""
    anker = buildAnkerForFigure(pFigureName)
    outStr = f"""<li><a href="#{anker}">{pFigureName}</a></li>"""
    return outStr


def build_html_head(pTitle: str, pStylesheet: str) -> str:
    head_tag: str = ""
    head_tag = "<!DOCTYPE html>\n<html lang=" + '"' + "de" + '"' + ">"
    head_tag += f"""<head>
    <meta charset="utf-8">
    <title>{pTitle}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{pStylesheet}">
    <script src="script.js"></script>
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>"""
    return head_tag


class HTMLVisitor(cVisitor):
    def __init__(self):
        self.html_title: str = ""  # pHtml.title
        self.HtmlRootFileName: str = ""  # pHtml.html_file_name
        self.stylesheet: str = ""  # pHtml.stylesheet
        self.html_root_string: str = ""  # komplette main html Datei
        self.html_sub_string: str = ""  # sub html Dateien für Tänze

    def write_html_sub_file(self, pHhtml_file_name: str, pPath: str) -> None:
        fn: str = pPath + pHhtml_file_name
        with open(fn, "w", encoding="utf-8") as f:
            f.write(
                self.html_sub_string
                + "/n Diese Methode gehört zum Visitor_HTML und sollte nicht mehr benutzt werden."
            )
        f.close()

    def printerRoot(self, txt: str):
        self.html_root_string += txt + "\n"

    def printerSub(self, txt: str):
        self.html_sub_string += txt + "\n"

    def get_css_classes(self, node: Node, element: str) -> str:
        """
        Liefert die CSS-Klassen für ein HTML-Element.
        """
        classes: list[str] = get_map_classes(node.role, element)
        return " ".join(classes)

    # Dokumentenkopf (nicht html <head>)
    def visit_header(self, node: cDokumentHeader) -> str:
        outStr: str = ""
        outStr = "<header>"
        outStr += f"<h1>{node.h1}</h1>"
        outStr += f'<p class="path mono">{node.h1}</p>'
        outStr += "</header>"
        return outStr

    def visit_link(self, node: cLink) -> str:
        # <a class="video" href="https://www.youtube.com/watch?v=xNx16-QIJ_A" target="_blank" rel="noopener">Video ansehen</a></p>
        return f"{node.link} - {node.linkComment}"

    def visit_dance(self, node: cDance) -> str:
        return f"{node.dance}"

    def HTML_Link_Button(self, page: str, txt: str):
        # <a href="my.html" class="button">Link zu my.html</a>
        ret: str = ""
        ret += "<a href=" + '"' + page + '"' + ' class="button-link">' + txt + "</a>"
        self.printerRoot(ret)

    def HTML_Link_Text(self, page: str, txt: str):
        # <a href="seite2.html">Zur Seite 2</a>
        ret = ""
        ret += "<a href=" '"' + page + '"' + ' class="text-link">' + txt + "</a>"
        self.printerRoot(ret)

    # --------------- Main Page mit Buttonlist ------------------------------------------------

    def visit_Button(self, node: cButton) -> str:
        return "Ein Button:   " + node.link + "   " + node.text

    def visit_ButtonList(self, node: cButtonList) -> str:
        outStr: str = ""

        outStr += f'<div class="button_spalte">'

        # buttons ausgeben
        for iButton in node.elem:
            outStr += iButton.accept(self)

        outStr += "</div>"

        return outStr

    def visit_MainPage(self, node: cMainPage) -> str:
        outStr: str = ""
        outStr = f'<div class="main_page">'
        outStr += node.DocTitle.accept(self)
        outStr += node.buttonlist.accept(self)

        outStr += "</div>"
        return outStr

    # ------------------------------------------------------------------------------------

    def visit_TSV_Tanz(self, node: cTSV_TANZ) -> str:

        FilterList: Dict[str, cDanceDict] = {}

        # TOC mit allen Gruppen anlegen
        GruppenListe_TOC: cToC = cToC()
        GruppenListe_TOC.set_role(cRoles.TOC_DANCES)

        # Gruppenfilterungen anlegen
        # TOC mit allen Gruppen anlegen
        for iGroupKey, iKursInfo in node.AllKursInfo.items():
            iDandi = cDanceDict()
            # DanDi_raw = Dict[str, cFigureList]:
            iDandi.DanDi_raw = node.CompleteDanceDict.filter_Gr(iGroupKey)
            iDandi.KursInfo = iKursInfo
            iDandi.buildTOC()  # ToC der Tänze in einer Filterung/Gruppe
            iDandi.ToC.set_role(cRoles.TOC_DANCES)

            FilterList[iGroupKey] = iDandi

            # Pfad zu den Gruppenseiten xxx214
            path_name: Path = Path("html")   / iKursInfo.GroupName / (cleanFromSpecialChars(iKursInfo.GroupName) + ".html")
            
            # ToC pflegen: Gruppe in TOC aufnehmen      xxx213
            Gruppe: cToC_Entry = cToC_Entry(
                path_name.as_posix(),
                iKursInfo.GroupName,
            )
            Gruppe.set_role(cRoles.TOC_DANCE_ENTRY)
            GruppenListe_TOC.addEntry(Gruppe)

        # ---------------------------------- Begin Groups Page ------------------------------
        Groups_Page: cSubPage = cSubPage()
        Groups_Page.docTitle.text = node.GenInfo.description
        Groups_Page.docTitle.set_role(cRoles.PAGE_TITLE_H1)
        Groups_Page.set_role(cRoles.NAV_GROUPS)
        Groups_Page.TOC = GruppenListe_TOC
        Groups_Page.TOC.set_role(cRoles.TOC_GROUPS)
        Groups_Page.html = Groups_Page.accept(self)

        # html-root, liegt in ARCHIV_SUB_DIR
        html: cHTML = cHTML(
            pHtmlFileNameStr=node.GenInfo.HTML_OutputFileName,
            pHtmlPath=node.GenInfo.ARCH_SUB_absDIR,
            pRelPathToProject="",
            pStylesheetName=HTML_StylesheetName,
            pPathToStylesheet="",
            pTitle="Archiv",
        )
        html.headTagTitle = "Tanzen"  # Titel in <head> - Tag (erscheint im Browser Tab)
        html.role = " ".join(get_map_classes(cRoles.PAGE_ROOT, "body"))
        html.tag_body(Groups_Page.html)
        html.write_html_file()

        # ---------------------------------- Dances Pages --------------------------
        # -> Seiten mit den Tänzen einer Gruppe/Filterung

        # Schleife über Filterungen
        for iDanceDict in FilterList.values():  # Info: Dict[str, cDanceDict]
            # SubPage anlegen
            Dances_Page = cSubPage()
            Dances_Page.gruppe = iDanceDict.KursInfo.GroupName
            Dances_Page.docTitle.text = iDanceDict.KursInfo.DokTitle.text
            Dances_Page.docTitle.role = cRoles.PAGE_TITLE_H2

            Dances_Page.set_role(cRoles.NAV_DANCES)

            Dances_Page.TOC = iDanceDict.buildTOC()
            Dances_Page.TOC.set_role(cRoles.TOC_DANCES)

            Dances_Page.html = Dances_Page.accept(self)

            # html mit den Tänzen einer Gruppe, zBsp Alles.html
            # Pfad: BASE_DIR / HTML_Output_relative_Path / GruppenName / GruppenName.html
            # bzw:  Archiv   / html                      / Alles       / Gruppe 1.html
            # (hier liegen auch die Tanz-Seiten, CC.html, ...)
            html: cHTML = cHTML(
                pHtmlFileNameStr=cleanFromSpecialChars(iDanceDict.KursInfo.GroupName)
                + ".html",
                # pHtmlPath=Path(HTML_RootPath) / iDanceDict.KursInfo.GroupName,
                pHtmlPath=node.GenInfo.HTML_Output_absDir
                / iDanceDict.KursInfo.GroupName,
                pRelPathToProject="../..",
                pStylesheetName=HTML_StylesheetName,
                pPathToStylesheet="../..",
                pTitle="Archiv - " + iDanceDict.KursInfo.GroupName,
            )
            html.headTagTitle = iDanceDict.KursInfo.GroupName
            html.role = cRoles.NAV_DANCES
            html.tag_body(Dances_Page.html)
            html.write_html_file()

        # ------------------------------- FigureList Pages ----------------------
        # Seiten mit Figuren-Inhaltsverzeichnis und Figuren-Karten:  nach Tanz und Gruppe/Filterung

        for iDanceDict in FilterList.values():
            # print(iDanceDict)
            for iDance, iFigutreList in iDanceDict.DanDi_raw.items():

                # Figurenliste mit Inhaltsverzeichnis
                Figure_Page: cSubPage = cSubPage()
                Figure_Page.set_role(cRoles.NAV_FIGURES)
                Figure_Page.gruppe = iDanceDict.KursInfo.GroupName

                Figure_Page.docTitle.text = (
                    iDanceDict.KursInfo.GroupName + " - " + XLS_Dance_SheetList[iDance]
                )
                Figure_Page.docTitle.set_role(cRoles.PAGE_TITLE_H2)
                iFigutreList.set_role(cRoles.FIGURE_LINK_LIST_TABLE)
                Figure_Page.TOC = iFigutreList.ToC
                Figure_Page.TOC.set_role(cRoles.TOC_FIGURES)

                Figure_Page.html = Figure_Page.accept(self)
                Figure_Page.html += iFigutreList.accept(self)

                # html mit den Figuren einer Gruppe und einem Tanz, zBsp Alles.html / CC.html
                # gleiche Pfade wie bei den Tanz-Seiten
                html: cHTML = cHTML(
                    pHtmlFileNameStr=iDance + ".html",
                    pRelPathToProject="../..",
                    pHtmlPath=node.GenInfo.HTML_Output_absDir
                    / iDanceDict.KursInfo.GroupName,
                    pStylesheetName=HTML_StylesheetName,
                    pPathToStylesheet="../..",
                    pTitle=iDanceDict.KursInfo.GroupName + " - " + iDance,
                )
                html.headTagTitle = (
                    iDanceDict.KursInfo.GroupName + " - " + XLS_Dance_SheetList[iDance]
                )
                html.role = cRoles.NAV_FIGURES
                html.tag_body(Figure_Page.html)
                html.write_html_file()

        # ------------------------------- End FigureList Pages ------------------------
        return "read"

    def visit_otherinfos(self, node: cKursInfo) -> str:
        return node.DokTitle.accept(self)

    def visit_html_head(self, node: cHTML):
        self.printerRoot(build_html_head(node.headTagTitle, node.StyleSheetName))

    def visit_figureListHeadline(self, node: cFigureList_HeadLine) -> str:
        outStr: str = f"<h2>{node.Group} - {node.Dance}</h2>"
        return outStr

    def visit_figureList(self, node: cFigureList) -> str:
        outStr: str = ""
        # Figurenliste mit den Figurenkarten
        # (TOC wird von der SubPage gebaut)

        # Figurenliste
        for ifigure in node.figures:
            outStr += ifigure.accept(self)

        return outStr

    # Darstellung einer Figur mit allen Eigenschaften
    def visit_figure(self, node: cFigure) -> str:

        #  hier weiter mit der Ausgabe der Figur:

        outStr: str = ""
        anker = buildAnkerForFigure(node.figureName)

        # Header
        # ...

        # Rahmen
        class_list: str = self.get_css_classes(node, "card")  # figure-card
        outStr = f'<div id="{anker}" class="{class_list}">'

        # Titelzeile mit Name, xls-Zeile, Datum
        node.setHeadLine(node.filter_group)
        node.headline.set_role(cRoles.FIGURE_HEADER)
        outStr += node.headline.accept(self)

        # Kommentar
        # style_classes: str = self.get_css_classes(node.headline, "div")  # figure-comment
        style_classes_list = get_map_classes(cRoles.FIGURE_COMMENT, "div")
        style_classes = " ".join(style_classes_list)
        com_div = build_divCl(node.figureComment, style_classes)

        outStr += com_div

        # Linkliste
        outStr += node.linkListe.accept(self)

        # Ende Rahmen
        outStr += "</div>"

        # footer
        # ...

        return outStr

    def visit_ToC_Entry(self, node: cToC_Entry) -> str:
        outStr: str = ""
        class_list_li: str = self.get_css_classes(node, "li")
        outStr = f"""<li class="{class_list_li}">"""
        class_list_a: str = self.get_css_classes(node, "a")
        outStr += tag_href(node.LinkStr, node.text, class_list_a)
        outStr += "</li>"
        return outStr

    def visit_ToC(self, node: cToC) -> str:
        """
        gibt eine html-Link-Liste mit Links zu den Figuren zurück
        wird auf den Gruppenseiten benutzt:
        """
        outStr: str = ""
        nav_class_list: str = self.get_css_classes(node, "nav")
        ul_class_list: str = self.get_css_classes(node, "ul")
        outStr += f"""<nav class="{nav_class_list}"><ul class="{ul_class_list}">"""

        # über TOC-Einträge des jew. Tanzes iterieren
        for iTOC_Entry in node.entries:
            outStr += iTOC_Entry.accept(self)

        outStr += f"</ul></nav>"
        return outStr

    # baut aus allen KursInfos eine button list
    # benutzt in print_Main_Page()
    def build_ButtonList_for_Groups(self, pAllKursInformation: List[cKursInfo]) -> str:
        outStr: str = ""
        for i in range(len(pAllKursInformation)):
            target: str = (
                HTML_Output_relative_Path + pAllKursInformation[i].GroupName + "/"
            )
            buttonText: str = pAllKursInformation[i].GroupName
            outStr = build_href(
                target,
                buttonText,
                "site_button",
            )
        return outStr

    # baut eine kursspezifische sub page einem Verzeichnis der behandelten Tänzen
    def visit_SubPage(self, node: cSubPage) -> str:
        outStr: str = ""
        sty_class: str = self.get_css_classes(node, "div")  # main_page_container
        outStr += f'<div class="{sty_class}">'
        outStr += node.docTitle.accept(self)

        # Inhaltsverzeichnis
        outStr += node.TOC.accept(self)
        # outStr+= node.figureList.accept(self)

        outStr += "</div>"
        return outStr

    def visit_DanDi(self, node: cDanceDict) -> str:
        # outStr:str = ""

        return "Visit_HTML, visit_DanDi Zeile 258"

    def visit_DocumentTitle(self, node: cDokTitle) -> str:
        outStr: str = ""
        title_str: str = node.text

        if node.role == cRoles.PAGE_TITLE_H1:
            styleClass = self.get_css_classes(node, "h1")  # page-title-h1
            outStr = tag_h1(title_str, styleClass)
        elif node.role == cRoles.PAGE_TITLE_H2:
            styleClass = self.get_css_classes(node, "h2")  # page-title-h2
            outStr = tag_h2(title_str, styleClass)
        elif node.role == cRoles.PAGE_TITLE_H3:
            styleClass = self.get_css_classes(node, "h3")  # page-title-h3
            outStr = tag_h3(title_str, styleClass)
        return outStr

    def visit_figure_headline(self, node: cFigureHeadline) -> str:
        headLine: str = ""
        styleClass: str = self.get_css_classes(node, "h2")  # figure-header

        # Zeile xxx457: hartcodierte class figure-header-meta
        headLine = f"""
            <div class="{styleClass}">
                <h2>{node.figureTitle}</h2>      
                <div class="figure-meta">   
                    <span>{node.lessonDate}</span>                                       
        """
        if DEBUG:
            headLine += f"<span>{node.XLS_Line}</span>"

        headLine += "</div></div>"

        return headLine

    def visit_LinkList(self, node: cLinkListe) -> str:

        # Tabelle für Links und Link-Comments

        classes_head = self.get_css_classes(node, "table")  # figure-link-list-table
        outStr: str = f'<table class="{classes_head}">'

        # Tabellenkopf
        classes_head = self.get_css_classes(node, "thead")
        classes_body = self.get_css_classes(node, "tbody")
        classes_td_text = self.get_css_classes(node, "td_text")
        classes_td_link = self.get_css_classes(node, "td_link")

        link_table_head: str = f"""            
                <thead class="{classes_head}">
                    <tr class="{classes_body}">
                        <td class="{classes_td_text}">Erklärung</td>
                        <td class="{classes_td_link}">Link</td>
                    </tr>
                </thead>                     
            """

        # Tabellenkörper
        link_table_body: str = '<tbody class="' + cRoles.FIGURE_LINK_LIST_BODY + '">'
        for link in node.Links:
            link_table_body += f"""
                <tr>
                    <td class="{cRoles.FIGURE_LINK_COMMENT}">{link.linkComment}</td>
                    <td>
                        <a class="{cRoles.FIGURE_LINK}" href="{link.link}">Zum Video</a>
                    </td>
                </tr>                   
            """
        link_table_body += "</tbody>"

        outStr += link_table_head + link_table_body

        outStr += "</table>"

        return outStr

    def printFilterDanDi(self, pFiltDanDi: cDanceDict, pKursInfo: cKursInfo):

        # Für jeden Tanz:Figurenverzeichnis und Figurenlisten: Subseiten mit eigenem head und body
        for iDance in pFiltDanDi.DanDi_raw.keys():
            self.printerSub(
                build_html_head(
                    f"{XLS_Dance_SheetList[iDance]}", "../" + self.stylesheet
                )
            )

            self.printerSub("<body>")

            self.printerSub(tag_h1(f"{XLS_Dance_SheetList[iDance]}"))

            # Inhaltsverzeichnis Figuren
            self.printerSub(f'<nav class="sty_inhaltsverzeichnis_figuren"><ul>')
            for iFigure in pFiltDanDi.DanDi_raw[iDance].figures:
                self.printerSub(build_TOC_Entry_Figure(iFigure.figureName))
            self.printerSub("</ul></nav>")

            # alle Figuren schreiben
            all_frame_div = f'<div class="all_figure_frame">'

            self.printerSub(all_frame_div)

            figureList = pFiltDanDi.DanDi_raw[iDance].getAll()
            for iFigure in figureList:
                iFigure.accept(self)

            self.printerSub("</div>")
            self.printerSub("</body></html>")

            # Tanz-Seite schreiben
            fn: str = XLS_Dance_SheetList[iDance].replace(" ", "_") + ".html"
            self.write_html_sub_file(
                fn, pKursInfo.GroupName + "/" + pKursInfo.GroupName
            )
