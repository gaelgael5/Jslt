"""Plugin jslt : lecture de fichiers CSV (``loadcsv``).

Port de ``Bb.CustomServices.ServiceCsv.ExecuteLoadCsvSource`` du .NET. Fournit la
fonction de template ``loadcsv`` qui lit un fichier CSV et renvoie un tableau
d'objets JSON (une entrée par ligne).

Ce paquet est découvert automatiquement par ``jslt`` via le groupe d'entry points
``jslt.functions`` (il suffit de l'installer). Il peut aussi être enregistré
explicitement : ``from jslt_csv import register; register(mon_registre)``.

Écarts volontaires vs .NET (documentés) :

* La résolution de chemin du .NET (``ctx.Configuration.ResolveFile``) n'existe pas
  dans le portage cœur : ``source_path`` est ouvert tel quel (absolu ou relatif au
  répertoire courant). Le BOM éventuel est retiré (``utf-8-sig``).
* Les types ``decimal``/``long`` du .NET deviennent ``float``/``int`` (types JSON
  Python). La détection de type (bool / entier / décimal / chaîne) est fidèle.
"""

from __future__ import annotations

import csv as _csv
import unicodedata
from typing import Any

__version__ = "0.0.1"

__all__ = ["execute_loadcsv", "register"]


def _sanitize_header(name: str) -> str:
    """Assainit un nom de colonne (port de ``ServiceCsv.GetLabel``).

    Même intention que le .NET (alphanumérique conservé, accents -> ASCII,
    espaces/quotes -> ``_``, underscores multiples réduits), mais via la
    normalisation Unicode (NFKD) plutôt qu'une table figée : tous les accents sont
    traités uniformément (le .NET avait une table incomplète, p.ex. ``Â`` manquant).
    """
    decomposed = unicodedata.normalize("NFKD", name)
    out: list[str] = []
    for char in decomposed:
        if unicodedata.combining(char):
            continue  # supprime les diacritiques (accents)
        if char.isascii() and char.isalnum():
            out.append(char)
        elif char in (" ", "'", '"'):
            out.append("_")
        # tout autre caractère est supprimé
    label = "".join(out)
    while "___" in label:
        label = label.replace("___", "_")
    return label.replace("__", "_")


#: Sentinelle interne : la cellule doit être omise de l'objet résultat.
_DROP = object()


def _coerce(raw: Any, exclude_null_and_empty: bool) -> Any:
    """Coerce une cellule CSV en valeur JSON (port de ``ServiceCsv.GetValue``).

    Retourne la sentinelle :data:`_DROP` si la valeur doit être omise (null/vide
    avec ``exclude_null_and_empty``).
    """
    if raw is None:
        return _DROP if exclude_null_and_empty else None

    text = raw.strip()
    low = text.lower()

    if low == "":
        return _DROP if exclude_null_and_empty else ""

    if low == "true":
        return True
    if low == "false":
        return False

    # Détection numérique : commence par '-' ou un chiffre (fidèle au .NET).
    first = low[0]
    if first == "-" or first.isdigit():
        is_int = False
        is_decimal = False
        for index, char in enumerate(low):
            if index == 0 and char == "-":
                continue
            if char.isdigit():
                is_int = True
            elif is_int and char == ".":
                is_decimal = True
            else:
                break
        if is_decimal:
            try:
                return float(text)
            except ValueError:
                pass
        elif is_int:
            try:
                value = int(text)
            except ValueError:
                value = None
            # Garde-fou .NET (l.ToString() == v) : on ne coerce pas "007".
            if value is not None and str(value) == text:
                return value

    # Chaîne : valeur d'origine (déjà rognée), casse conservée.
    return text


def execute_loadcsv(
    ctx: Any,
    source_path: str | None = None,
    has_header: bool = True,
    separator: str = ";",
    quote: str = '"',
    escape: str = "\\",
    excluded_columns: str | None = None,
    exclude_null_and_empty: bool = False,
) -> list:
    """Lit un fichier CSV et renvoie un tableau d'objets (port de ``loadcsv``).

    Args:
        source_path: chemin du fichier CSV (absolu ou relatif au répertoire courant).
        has_header: la 1re ligne porte les noms de colonnes (sinon ``Column0``…).
        separator: séparateur de champs (défaut ``;``).
        quote: caractère de citation (défaut ``"``).
        escape: caractère d'échappement (défaut ``\\``).
        excluded_columns: noms de colonnes à exclure, séparés par ``separator``.
        exclude_null_and_empty: omet les cellules nulles/vides (et les lignes qui
            n'auraient plus aucune valeur).

    Returns:
        La liste des lignes, chacune sous forme de dict colonne -> valeur typée.
    """
    if not source_path:
        raise ValueError("loadcsv: source_path est requis")

    delimiter = separator[0] if separator else ";"
    quotechar = quote[0] if quote else '"'
    escapechar = escape[0] if escape else None

    excluded: set[str] = set()
    if excluded_columns:
        excluded = {c for c in excluded_columns.split(delimiter) if c}

    with open(source_path, newline="", encoding="utf-8-sig") as handle:
        reader = _csv.reader(
            handle, delimiter=delimiter, quotechar=quotechar, escapechar=escapechar
        )
        rows = list(reader)

    if not rows:
        return []

    if has_header:
        raw_headers = rows[0]
        data_rows = rows[1:]
    else:
        raw_headers = [f"Column{i}" for i in range(len(rows[0]))]
        data_rows = rows

    # (nom_brut, nom_assaini) par colonne ; l'exclusion compare le nom brut (.NET).
    columns = [
        (raw, raw if not has_header else _sanitize_header(raw)) for raw in raw_headers
    ]

    result: list[dict] = []
    for row in data_rows:
        obj: dict[str, Any] = {}
        for index, (raw_name, label) in enumerate(columns):
            if raw_name in excluded:
                continue
            cell = row[index] if index < len(row) else None
            value = _coerce(cell, exclude_null_and_empty)
            if value is _DROP:
                continue
            obj[label] = value
        if obj or not exclude_null_and_empty:
            result.append(obj)
    return result


def register(registry: Any) -> None:
    """Enregistre les fonctions du plugin dans un registre jslt.

    Point d'entrée déclaré via l'entry point ``jslt.functions`` (découverte
    automatique) et utilisable manuellement.
    """
    registry.register(
        "loadcsv",
        execute_loadcsv,
        description="Lit un fichier CSV et renvoie un tableau d'objets.",
    )
