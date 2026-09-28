from urllib.parse import quote
from pathlib import Path


def __html_tag_h123(
    headlineType: str, title: str, classs: str = "", id: str = ""
) -> str:
    outStr: str = ""
    if id:
        idStr = f'id="{id}"'
    else:
        idStr = ""
    if classs:
        classStr = f'class="{classs}"'
    else:
        classStr = ""

    outStr = f"""<{headlineType} {idStr} {classStr}>{title}</{headlineType}>"""

    return outStr


def tag_h1(title: str, classs: str = "", id: str = "") -> str:
    return __html_tag_h123("h1", title, classs, id)


def tag_h2(title: str, classs: str = "", id: str = "") -> str:
    return __html_tag_h123("h2", title, classs, id)


def tag_h3(title: str, classs: str = "", id: str = "") -> str:
    return __html_tag_h123("h3", title, classs, id)


def tag_href(pTarget: str, pText: str, pStyleClass: str = "") -> str:
    outSt: str = ""
    if pStyleClass == "":
        outSt = f'<a href="{pTarget}">{pText}</a>'
    else:
        outSt = f'<a href="{pTarget}" class="{pStyleClass}" >{pText}</a>'
    return outSt


class cHTML:
    def __init__(
        self,
        pHtmlFileNameStr: str,  # Name der HTML-Datei
        pHtmlPath: Path,  # Pfad, wo diese Datei liegt
        pRelPathToProject: str,  # Weg zurück zum Projektverzeichnis HTML_Writer
        pStylesheetName: str,  # Name des Stylesheets
        pPathToStylesheet: str,  # Pfad vom Projekt zum Stylesheet
        pTitle: str = "",
    ):
        self.html_file_name: str = pHtmlFileNameStr
        self.Path: Path = pHtmlPath
        self.RelPathToProject = pRelPathToProject
        self.StyleSheetName: str = pStylesheetName
        self.StyleSheet_path: Path = Path(pPathToStylesheet)
        self.headTagTitle: str = pTitle
        self.body: str = ""
        self.html_String: str = ""
        styleSheet_PathName_posix: str = quote(
            (self.StyleSheet_path / self.StyleSheetName).as_posix()
        )
        self.tag_head(styleSheet_PathName_posix)
        self.role: str = ""

    def write_html_file(self):
        html_String: str = "<!DOCTYPE html>\n<html lang=" + '"' + "de" + '"' + ">"
        html_String += self.head + self.body + "</html>"

        path = Path(self.Path) / self.html_file_name
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            f.write(html_String)
        # nicht nötig, wird von with miterledigt: f.close()
        html_String = ""

    def tag_body(self, pBody: str):
        self.body = f'<body class="{self.role}">'
        self.body += pBody
        self.body += "</body>"

    def tag_head(self, pStylesheet_PathName: str):
        head_tag: str = ""
        head_tag += f"""<head>
        <meta charset="utf-8">
        <title>{self.headTagTitle}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{pStylesheet_PathName}">
        <script src="script.js"></script>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        </head>"""
        self.head = head_tag
