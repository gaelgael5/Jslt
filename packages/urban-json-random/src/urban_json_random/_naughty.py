"""Chaînes piégeuses pour éprouver un traitement de texte (``getrandom_naughtystrings``).

Extrait de la « Big List of Naughty Strings » (Max Woolf, licence MIT,
https://github.com/minimaxir/big-list-of-naughty-strings), la source qu'utilise
``RandomDataGenerator`` côté .NET. Une entrée par famille de piège, pas la liste
complète : l'objectif est la variété, pas l'exhaustivité.
"""

from __future__ import annotations

NAUGHTY_STRINGS: tuple[str, ...] = (
    # vides et réservés
    "",
    " ",
    "undefined",
    "null",
    "NULL",
    "nil",
    "None",
    "true",
    "false",
    "NaN",
    "Infinity",
    "-Infinity",
    "0",
    "-0",
    "0.0",
    "1E+02",
    "0xffffffff",
    "999999999999999999999",
    "1/0",
    # espaces et contrôles
    "\t",
    "\u00a0",
    "\u200b",
    "\ufeff",
    "\u2028",
    # Unicode
    "Ω≈ç√∫˜µ≤≥÷",
    "Œ„´‰ˇÁ¨ˆØ∏”’",
    "田中さんにあげて下さい",
    "社會科學院語學研究所",
    "울란바토르",
    "👾 🙇 💁 🙅 🙆 🙋 🙎 🙍",
    "👨‍👩‍👦",
    "ثم نفس سقطت وبالتحديد",
    "בְּרֵאשִׁית, בָּרָא אֱלֹהִים",
    "Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳",
    "ﾟ･✿ヾ╲(｡◕‿◕｡)╱✿･ﾟ",
    # injections et formats
    "<script>alert(123)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "' OR '1'='1",
    "1; DROP TABLE users",
    "${7*7}",
    "{{7*7}}",
    "%s%s%s%s%s",
    "../../../../../../etc/passwd",
    "C:\\Windows\\System32",
    "$HOME",
    "`ls -la`",
    "\\\\",
    '"',
    "'",
)
