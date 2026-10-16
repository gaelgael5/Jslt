# Bancs d'essai (performance)

Scripts de mesure du débit du moteur. **Hors suite de tests** (`pytest` ne les
collecte pas) : ils ne tournent pas en CI, on les lance à la main.

```bash
pip install -e "packages/urban-json[dev]"
python benchmarks/bench_transform.py                 # tailles par défaut
python benchmarks/bench_transform.py --size 50000 --repeats 9
```

## `bench_transform.py`

Compare, sur des scénarios « import en masse » (grands tableaux via boucle
`$source`, avec opérateurs / casts / `when`), **l'interpréteur d'AST** et le
**chemin compilé** (`JsltTemplate.build()`). Le template est analysé une fois,
puis réappliqué N fois ; on reporte la médiane de chaque chemin, le facteur
d'accélération, et le débit (éléments/s) du chemin compilé. Avant de mesurer, le
banc vérifie que les **deux chemins produisent un résultat identique** (la
compilation est prouvée équivalente, pas seulement plus rapide).

Les chiffres sont **relatifs à la machine** : ils servent à comparer les deux
chemins entre eux, pas à donner une valeur absolue. Ordre de grandeur observé :
**×3 à ×5** selon le template (gain maximal sur les accès de champs `$.x`,
dominants dans les imports).
