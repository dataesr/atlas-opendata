import os
import re
import glob
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter


YEAR_COL_CANDIDATES = ["ANNEE", "RENTREE"]


def _read_any(path: str) -> pd.DataFrame:
    """Lit un fichier csv, excel ou json, en devinant le séparateur pour le csv."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        df = pd.read_json(path)
        # les colonnes utiles sont castées en str pour un croisement homogène
        return df.astype(
            {c: str for c in ["COMPOS", "COM_U", "ETABLI", "COM_M"] if c in df.columns}
        )
    if ext in (".xlsx", ".xls", ".xlsm"):
        return pd.read_excel(path, dtype=str)
    # CSV : on essaie ; puis , puis tab
    for sep in [";", ",", "\t"]:
        try:
            df = pd.read_csv(path, sep=sep, dtype=str, engine="python")
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    # dernier recours
    return pd.read_csv(path, dtype=str, engine="python")


def _find_year_column(df: pd.DataFrame) -> str:
    for c in YEAR_COL_CANDIDATES:
        if c in df.columns:
            return c
    raise ValueError(
        f"Aucune colonne d'année trouvée parmi {YEAR_COL_CANDIDATES}. "
        f"Colonnes disponibles : {list(df.columns)}"
    )


def _crosstab_pair(df: pd.DataFrame, code_col: str, commune_col: str, year_col: str) -> pd.DataFrame:
    """
    Retourne un DataFrame indexé par (code_col, commune_col), colonnes = années,
    valeurs = nombre de lignes (comptage) pour cette combinaison cette année-là.
    """
    sub = df[[code_col, commune_col, year_col]].copy()
    sub = sub.dropna(subset=[code_col])
    grouped = (
        sub.groupby([code_col, commune_col, year_col])
        .size()
        .reset_index(name="n")
    )
    pivot = grouped.pivot_table(
        index=[code_col, commune_col],
        columns=year_col,
        values="n",
        aggfunc="sum",
        fill_value=0,
    )
    return pivot


def build_annual_crosstab(files: dict, output_path: str) -> str:
    """
    files : dict {annee (int) -> chemin du fichier}
    output_path : chemin du fichier Excel à produire
    """
    compos_frames = []
    etabli_frames = []

    for year, path in sorted(files.items()):
        df = _read_any(path)
        # normalise les noms de colonnes (espaces, casse)
        df.columns = [c.strip() for c in df.columns]

        required = ["COMPOS", "COM_U", "ETABLI", "COM_M"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Fichier {path} ({year}) : colonnes manquantes {missing}")

        # on force l'année depuis le nom de fichier/dict plutôt que la colonne du fichier,
        # au cas où RENTREE / ANNEE ne correspond pas exactement à l'année du fichier
        df["_YEAR_"] = year

        compos_frames.append(df[["COMPOS", "COM_U", "_YEAR_"]])
        etabli_frames.append(df[["ETABLI", "COM_M", "_YEAR_"]])

    all_compos = pd.concat(compos_frames, ignore_index=True)
    all_etabli = pd.concat(etabli_frames, ignore_index=True)

    pivot_compos = _crosstab_pair(all_compos, "COMPOS", "COM_U", "_YEAR_")
    pivot_etabli = _crosstab_pair(all_etabli, "ETABLI", "COM_M", "_YEAR_")

    _write_excel(pivot_compos, pivot_etabli, sorted(files.keys()), output_path)
    return output_path


def build_annual_crosstab_from_atlas_json(
    folder: str,
    output_path: str,
    years: range = range(2001, 2026),
    template: str = "atlas{annee}.json",
) -> str:
    """
    Convention de nommage : ./POST_IMPORTTAB/atlas{rentree_sco}.json
    (ex: atlas2025.json), rentree_sco étant l'année en string.

    Exemple :
        build_annual_crosstab_from_atlas_json(
            "./POST_IMPORTTAB", "resultat.xlsx"
        )
    """
    files = {}
    for year in years:
        path = os.path.join(folder, template.format(annee=year))
        if os.path.exists(path):
            files[year] = path
        else:
            print(f"[attention] fichier introuvable pour {year} : {path}")

    if not files:
        raise ValueError(f"Aucun fichier atlas trouvé dans {folder}")

    return build_annual_crosstab(files, output_path)


def build_annual_crosstab_from_folder(folder: str, output_path: str, pattern: str = "*") -> str:
    """
    Détecte automatiquement l'année (4 chiffres, 2001-2025) dans chaque nom de fichier
    du dossier correspondant au pattern, puis appelle build_annual_crosstab.
    """
    files = {}
    for path in glob.glob(os.path.join(folder, pattern)):
        if not path.lower().endswith((".csv", ".xlsx", ".xls", ".xlsm", ".tsv")):
            continue
        m = re.search(r"(20[0-2][0-9])", os.path.basename(path))
        if not m:
            continue
        year = int(m.group(1))
        files[year] = path

    if not files:
        raise ValueError(f"Aucun fichier avec une année (20xx) trouvé dans {folder}")

    return build_annual_crosstab(files, output_path)


def _write_excel(pivot_compos: pd.DataFrame, pivot_etabli: pd.DataFrame, years: list, output_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Croise annuel"

    header_font = Font(name="Arial", bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    section_font = Font(name="Arial", bold=True, size=11)
    section_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    normal_font = Font(name="Arial")

    row_cursor = 1

    # Titre général
    ws.cell(row=row_cursor, column=1, value="Tableau croisé annuel").font = Font(name="Arial", bold=True, size=13)
    row_cursor += 1

    # En-tête commun
    header_row = row_cursor
    ws.cell(row=header_row, column=1, value="Code").font = header_font
    ws.cell(row=header_row, column=1).fill = header_fill
    ws.cell(row=header_row, column=2, value="Commune").font = header_font
    ws.cell(row=header_row, column=2).fill = header_fill
    for j, year in enumerate(years, start=3):
        c = ws.cell(row=header_row, column=j, value=year)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")
    row_cursor = header_row + 1

    first_data_row = None
    last_data_row = None

    def write_section(section_label, pivot):
        nonlocal row_cursor, first_data_row, last_data_row

        # ligne de section (fusionnée visuellement par un fond gris)
        ws.cell(row=row_cursor, column=1, value=section_label).font = section_font
        for col in range(1, 3 + len(years)):
            ws.cell(row=row_cursor, column=col).fill = section_fill
        row_cursor += 1

        for (code_val, commune_val), row in pivot.iterrows():
            if first_data_row is None:
                first_data_row = row_cursor
            ws.cell(row=row_cursor, column=1, value=code_val).font = normal_font
            ws.cell(row=row_cursor, column=2, value=commune_val).font = normal_font
            for j, year in enumerate(years, start=3):
                val = int(row[year]) if year in row.index else 0
                cell = ws.cell(row=row_cursor, column=j, value=val)
                cell.font = normal_font
                cell.alignment = Alignment(horizontal="center")
            last_data_row = row_cursor
            row_cursor += 1

    write_section("COMPOS / COM_U", pivot_compos)
    write_section("ETABLI / COM_M", pivot_etabli)

    # Une seule heatmap sur l'ensemble des données (hors lignes de section)
    if first_data_row and last_data_row:
        first_col_letter = get_column_letter(3)
        last_col_letter = get_column_letter(2 + len(years))
        # openpyxl ne gère pas nativement les plages discontinues avec une regle unique
        # facilement lisible -> on applique la règle sur toute la zone du haut jusqu'en bas,
        # les lignes de section (texte, pas de nombre) sont ignorées par le color scale.
        data_range = f"{first_col_letter}{header_row + 1}:{last_col_letter}{last_data_row}"
        rule = ColorScaleRule(
            start_type="min", start_color="FFFFFF",
            mid_type="percentile", mid_value=50, mid_color="FFEB84",
            end_type="max", end_color="F8696B",
        )
        ws.conditional_formatting.add(data_range, rule)

    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 16
    for j in range(3, 3 + len(years)):
        ws.column_dimensions[get_column_letter(j)].width = 8

    ws.freeze_panes = "C3"
    wb.save(output_path)


if __name__ == "__main__":
    # Exemple d'utilisation avec un dossier contenant un fichier par année
    # (adapter le chemin et le pattern à vos fichiers réels)
    import sys

    if len(sys.argv) >= 3:
        folder_arg = sys.argv[1]
        out_arg = sys.argv[2]
        build_annual_crosstab_from_folder(folder_arg, out_arg)
        print(f"Fichier généré : {out_arg}")
    else:
        print("Usage: python build_crosstab.py <dossier_fichiers> <sortie.xlsx>")