# Bancs d'essai (performance)

Scripts de mesure du débit du moteur. **Hors suite de tests** (`pytest` ne les
collecte pas) : ils ne tournent pas en CI, on les lance à la main.

```bash
pip install -e "packages/urban-json[dev]"
python benchmarks/bench_transform.py                 # tailles par défaut
python benchmarks/bench_transform.py --size 50000 --repeats 9
```

## `bench_transform.py`

Mesure `JsltTemplate.transform` sur des scénarios « import en masse » (grands
tableaux via boucle `$source`, avec opérateurs / casts / `when`). Le template
est analysé une fois, puis réappliqué N fois ; on reporte la médiane et le débit
(éléments/s).

Les chiffres sont **relatifs à la machine** : ils servent à comparer des
variantes du moteur entre elles, pas à donner une valeur absolue.

## À venir : comparaison interpréteur vs compilé

Quand le chemin compilé (`JsltTemplate.build()`) existera, ce banc exécutera
chaque scénario sur **les deux chemins** et affichera le facteur d'accélération,
après avoir vérifié que les deux produisent un résultat **identique** (la
compilation doit être prouvée équivalente, pas seulement plus rapide).
