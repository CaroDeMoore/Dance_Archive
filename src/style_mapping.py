from src.nodes import *
from src.html_box import *

"""
    Hauptseite mit der Gruppennavigation
        <body>: PAGE_GROUPS
        <nav>: NAV_GROUPS
        ToC: TOC_GROUPS
        ToC-Eintrag: TOC_GROUP_ENTRY
    Unterseite mit den Tänzen einer Gruppe (Tanz-Navigation)
        <body>: PAGE_DANCES
        <nav>: NAV_DANCES
        ToC: TOC_DANCES
        ToC-Eintrag: TOC_DANCE_ENTRY
    Figurenseite
        Seite: PAGE_FIGURE
        ToC: TOC_FIGURE
        ToC-Eintrag: TOC_FIGURE_ENTRY
        Figuren-Karte
            FIGURE_CARD
    
"""


# roles für kontextabhängige Rollen
class cRoles:

    # -----------------------------
    PAGE_HEADER = "PAGE_HEADER"
    PAGE_CONTENT = "PAGE_CONTENT"
    PAGE_FOOTER = "PAGE_FOOTER"
    PAGE_TITLE_H1 = "PAGE_TITLE_H1"
    PAGE_TITLE_H2 = "PAGE_TITLE_H2"
    PAGE_TITLE_H3 = "PAGE_TITLE_H3"

    # -----------------------------
    PAGE_ROOT = "PAGE_ROOT"

    PAGE_GROUPS = "PAGE_GROUPS"
    NAV_GROUPS = "NAV_GROUPS"
    TOC_GROUPS = "TOC_GROUPS"
    TOC_GROUPS_ENTRY = "TOC_GROUP_ENTRY"

    # -----------------------------
    NAV_DANCES = "PAGE_DANCES"
    TOC_DANCES = "TOC_DANCES"
    TOC_DANCE_ENTRY = "NAV_DANCE_ENTRY"

    # -----------------------------
    NAV_FIGURES = "PAGE_FIGURES"
    TOC_FIGURES = "TOC_FIGURES"
    TOC_FIGURES_ENTRY = "TOC_FIGURE_ENTRY"
    FIGURE = "FIGURE"
    FIGURE_CARD = "FIGURE_CARD"
    FIGURE_CARD_LIST = "FIGURE_CARD_LIST"
    FIGURE_HEADER = "FIGURE_HEADER"
    FIGURE_TITLE = "FIGURE_TITLE"
    FIGURE_NAME = "FIGURE_NAME"
    FIGURE_COMMENT = "FIGURE_COMMENT"
    FIGURE_LINK_LIST_TABLE = "FIGURE_LINK_LIST"
    FIGURE_LINK_LIST_HEAD = "FIGURE_LINK_LIST_HEAD"
    FIGURE_LINK_LIST_BODY = "FIGURE_LINK_LIST_BODY"
    FIGURE_LINK_COMMENT = "FIGURE_LINK_COMMENT"
    FIGURE_LINK = "FIGURE_LINK"
    FIGURE_DATE = "FIGURE_DATE"
    MAL_SEHEN = "MAL_SEHEN"
    MAL_SEHEN_392 = "MAL_SEHEN_392"


def get_map_classes(role: str, element: str) -> list[str]:
    """
    Beispiel:
        cRoles.TOC_DANCE_ENTRY: {
            "div": {"class": ["page-sub"]},
            "li": {"class": ["toc-item"]},
            "a": {"class": ["toc-link"]},
    },"""

    # 1. Zugriff auf role
    """
    level1 liefert mit der Rolle cRoles.TOC_DANCE_ENTRY :
        level1 = {
            "div": {"class": ["page-sub"]},
            "li": {"class": ["toc-item"]},
            "a": {"class": ["toc-link"]},
        }
    """
    level1: Dict[str, Dict[str, list[str]]] = HTML_MAP[role]

    # 2. element suchen, sonst leeres dict
    """
        level2 liefert mit element "a" :
        level2 = {"class": ["toc-link"]}
    """
    level2: Dict[str, list[str]] = level1.get(element, {})

    # 3. "class" suchen, sonst leere Liste
    """
        level3 liefert mit "class" :
        level3 = ["toc-link"]
    """
    result: list[str] = level2.get("class", [])

    return result


DEFAULT_HEADER = {
    "h1": {"class": ["default_header_style"]},
    "h2": {"class": ["default_header_style"]},
    "h3": {"class": ["default_header_style"]},
    "h4": {"class": ["default_header_style"]},
    "h5": {"class": ["default_header_style"]},
}
# Mapping
# Abbildung von Rollen ---> Darstellung
#   Rolle ---> HTML-Element
#   css-Klassen je Element

HTML_MAP: dict[str, dict[str, dict[str, list[str]]]] = {
    # --------------------------------------
    "cLessonDate_default_role": {
        "li": {"class": ["default_li_style"]},
    },
    "cGroupLessonDates_default_role": {
        "ul": {"class": ["default_ul_style"]},
    },
    "cDance_default_role": {
        "p": {"class": ["default_p_style"]},
    },
    #
    # Überschriften
    "cDokTitle_default_role": DEFAULT_HEADER,
    "cDokumentHeader_default_role": DEFAULT_HEADER,
    "cFigureHeadline_default_role": DEFAULT_HEADER,
    "cFigureList_HeadLine_default_role": DEFAULT_HEADER,
    #
    # ToC und Einträg
    "cToC_Entry_default_role": {
        "li": {"class": ["default_li_style"]},  #
        "a": {"class": ["default_a_style"]},  #
    },
    "cToC_default_role": {
        "nav": {"class": ["default_nav_style"]},
        "ul": {"class": ["default_ul_style"]},
    },
    #
    # Links und Linklisten
    "cLink_default_role": {
        "li": {"class": ["default_li_style"]},
        "a": {"class": ["default_a_style"]},
    },
    "cLinkList_default_role": {
        "nav": {"class": ["default_nav_style"]},
        "ul": {"class": ["default_ul_style"]},
    },
    #
    # Buttons
    "cButton_default_role": {
        "a": {"class": ["default_button_style"]},
    },
    # ---------------------------------------------------
    cRoles.PAGE_TITLE_H1: {
        "h1": {"class": ["page-title-h1"]},
    },
    cRoles.PAGE_TITLE_H2: {
        "h2": {"class": ["page-title-h2"]},
    },
    cRoles.PAGE_TITLE_H3: {
        "h3": {"class": ["page-title-h3"]},
    },
    cRoles.PAGE_TITLE_H2: {
        "h2": {"class": ["page-title-h2"]},
    },
    cRoles.PAGE_TITLE_H3: {
        "h3": {"class": ["page-title-h3"]},
    },
    cRoles.MAL_SEHEN: {
        "a": {"class": ["mal-sehen-format"]},
    },
    cRoles.MAL_SEHEN_392: {
        "a": {"class": ["mal-sehen-format"]},
    },
    cRoles.PAGE_HEADER: {
        "header": {"class": ["page-header"]},
    },
    cRoles.PAGE_CONTENT: {
        "main": {"class": ["page-content"]},
    },
    cRoles.PAGE_FOOTER: {
        "footer": {"class": ["page-footer"]},
    },
    cRoles.PAGE_TITLE_H1: {
        "h1": {"class": ["page-title-h1"]},
    },
    # Groupus Page ----------------------------
    cRoles.PAGE_ROOT: {
        "body": {"class": ["page-root"]},
    },
    cRoles.NAV_GROUPS: {
        "div": {"class": ["page-groups"]},
    },
    cRoles.TOC_GROUPS: {
        "nav": {"class": ["nav", "nav-groups"]},
        "ul": {"class": ["toc"]},
    },
    cRoles.TOC_GROUPS_ENTRY: {
        "li": {"class": ["toc-item"]},
        "a": {"class": ["toc-link"]},
    },
    # Dances Page ---------------------------------
    cRoles.NAV_DANCES: {
        "div": {"class": ["page-dances"]},
    },
    cRoles.TOC_DANCES: {
        # TOC der Tänze auf den Gruppenseiten
        "nav": {"class": ["nav", "nav-dances"]},
        "ul": {"class": ["toc"]},
    },
    cRoles.TOC_DANCE_ENTRY: {
        "div": {"class": ["page-sub"]},
        "li": {"class": ["toc-item"]},
        "a": {"class": ["toc-link"]},
    },
    # Figures Page ---------------------------------
    cRoles.NAV_FIGURES: {
        "body": {"class": ["page-root"]},
    },
    cRoles.TOC_FIGURES: {
        # ToC der Figuren
        "nav": {"class": ["nav", "nav-figures"]},
        "ul": {"class": ["toc"]},
    },
    cRoles.TOC_FIGURES_ENTRY: {
        "li": {"class": ["toc-item"]},
        "a": {"class": ["toc-link"]},
    },

    cRoles.FIGURE_CARD: {
        "card": {"class": ["figure-card"]},
        
    },

    cRoles.FIGURE_LINK_LIST_TABLE: {
        "table": {"class": ["figure-links-table"]},
        "thead": {"class": ["figure-links-table-header"]},
        "tbody": {"class": ["figure-links-table-body"]},
        "tr": {"class": ["figure-links-table-row"]},
        "td_text": {"class": ["figure-links-link-text"]},
        "td_link": {"class": ["figure-links-link"]},
    },
    cRoles.FIGURE_LINK: {
        "a": {"class": ["figure-link"]},
    },
    #### Figuren-Karten
    cRoles.FIGURE: {
        "div": {"class": ["figure-card"]},
    },
    cRoles.FIGURE_HEADER: {
        "h2": {"class": ["figure-header"]},
    },
    cRoles.FIGURE_NAME: {
        "p": {"class": ["figure-name"]},
    },
    cRoles.FIGURE_COMMENT: {
        "div": {"class": ["figure-comment"]},
    },
    cRoles.FIGURE_DATE: {
        "div": {"class": ["figure-dates"]},
    },
    # Link-Liste der Figuren
    cRoles.FIGURE_LINK_LIST_TABLE: {
        "table": {"class": ["figure-links-table"]},
        "thead": {"class": ["figure-links-table-header"]},
        "tbody": {"class": ["figure-links-table-body"]},
        "tr": {"class": ["figure-links-table-row"]},
        "th": {"class": ["figure-links-table-cell"]},
        "td": {"class": ["figure-links-table-cell"]},
    },
    cRoles.FIGURE_LINK: {
        "a": {"class": ["figure-link"]},
    },
    cRoles.FIGURE_LINK: {
        "a": {"class": ["figure-link"]},
    },
}

"""
<div class="sub_page mainpage">
    <nav class="nav_buttons">
        <ul class="nav_list">
            <li class="nav_item">
                <a class="nav_link" href="...">Gruppe 1</a>
            </li>
        </ul>
    </nav>
</div>

1. deine bestehenden Rollen systematisch klassifizieren
layout layout
    main-page
    sub-page
navigation nav
    main-navigation-menu
    sub-page-toc
    toc-item  
    toc-link  
    button-back 
Komponente comp
    figure      - Komponente

...


eine konkrete CSS-Dateistruktur ableiten

Regeln definieren: Wann neue Rolle? Wann Variable?


"""
