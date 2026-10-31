/**
 * Tests de la complétion des chemins du document source.
 *
 * Exécution : `node --test packages/urban-json-editor/tests/` (node >= 18) ;
 * également lancés par pytest via test_paths_js.py.
 */

import assert from "node:assert/strict";
import test from "node:test";

import {
  DEFAULT_HINT_MESSAGES,
  describeValue,
  findPathStart,
  formatHint,
  parsePath,
  parseSourceDoc,
  pathHint,
  suggestPaths,
  treeFromPaths,
} from "../src/urban_json_editor/static/jslt-paths.js";

const DOC = {
  user: { name: "Alice", age: 30, "ville natale": "Lyon" },
  items: [
    { name: "a", n: 1, ok: true },
    { name: "b", extra: null },
  ],
  seuil: 2,
};

/** Signatures proposées au caret marqué par `|` dans le template. */
function sigs(template, doc = DOC) {
  const caret = template.indexOf("|");
  assert.notEqual(caret, -1, "le template doit marquer le caret avec |");
  const text = template.slice(0, caret) + template.slice(caret + 1);
  const res = suggestPaths(text, caret, doc);
  return res === null ? null : res.items.map((i) => i.signature);
}

/** Texte obtenu en acceptant la proposition `signature` au caret `|`. */
function accept(template, signature, doc = DOC) {
  const caret = template.indexOf("|");
  const text = template.slice(0, caret) + template.slice(caret + 1);
  const res = suggestPaths(text, caret, doc);
  assert.ok(res, "des propositions sont attendues");
  const item = res.items.find((i) => i.signature === signature);
  assert.ok(item, `proposition absente : ${signature} (parmi ${res.items.map((i) => i.signature)})`);
  return text.slice(0, res.from) + item.insert + text.slice(res.to);
}

test("$ seul propose les clés de la racine", () => {
  assert.deepEqual(sigs('{ "a": $| }'), ["user", "items", "seuil"]);
});

test("@ seul hors filtre ne propose rien", () => {
  assert.equal(sigs('{ "a": @| }'), null);
});

test("$. propose les clés de la racine, $.u les filtre", () => {
  assert.deepEqual(sigs('{ "a": $.| }'), ["user", "items", "seuil"]);
  assert.deepEqual(sigs('{ "a": $.u| }'), ["user"]);
});

test("descend dans un objet", () => {
  assert.deepEqual(sigs('{ "a": $.user.| }'), ["name", "age", "ville natale"]);
});

test("un tableau propose les clés de ses éléments avec [*]", () => {
  // `$.items.name` vaut null dans le moteur : la proposition porte son [*].
  assert.deepEqual(sigs('{ "a": $.items.| }'), ["[*].name", "[*].n", "[*].ok", "[*].extra"]);
  assert.equal(accept('{ "a": $.items.| }', "[*].name"), '{ "a": $.items[*].name }');
});

test("index et wildcard mènent aux clés d'un élément", () => {
  assert.deepEqual(sigs('{ "a": $.items[0].| }'), ["name", "n", "ok"]);
  assert.deepEqual(sigs('{ "a": $.items[*].n| }'), ["name", "n"]);
});

test("[ propose les sous-scripts disponibles", () => {
  assert.deepEqual(sigs('{ "a": $.items[| }'), ["[*]", "[0]", "[1]"]);
  assert.equal(accept('{ "a": $.items[| }', "[*]"), '{ "a": $.items[*] }');
  assert.equal(accept('{ "a": $.items[| }', "[1]"), '{ "a": $.items[1] }');
});

test("une clé non identifiant s'insère en forme crochets", () => {
  assert.equal(accept('{ "a": $.user.| }', "ville natale"), '{ "a": $.user["ville natale"] }');
});

test(".. propose les clés à toute profondeur", () => {
  assert.deepEqual(sigs('{ "a": $..| }'), ["..user", "..name", "..age", "..ville natale", "..items", "..n", "..ok", "..extra", "..seuil"]);
  assert.equal(accept('{ "a": $..na| }', "..name"), '{ "a": $..name }');
});

test("@ dans un filtre propose les clés de l'élément filtré", () => {
  assert.deepEqual(sigs('{ "a": $.items[?(@.| }'), ["name", "n", "ok", "extra"]);
  assert.deepEqual(sigs('{ "a": $.items[?(@.n| }'), ["name", "n"]);
  // La comparaison à la racine reste résolue depuis la racine.
  assert.deepEqual(sigs('{ "a": $.items[?(@.n >= $.s| }'), ["seuil"]);
});

test("@ dans un filtre d'un chemin non résolu ne propose rien", () => {
  assert.equal(sigs('{ "a": $.inconnu[?(@.| }'), null);
});

test("dans une boucle $source, $ désigne l'élément", () => {
  assert.deepEqual(sigs('[ { "$source": $.items, "v": $.| } ]'), ["name", "n", "ok", "extra"]);
  // y compris sous un objet imbriqué de la boucle
  assert.deepEqual(sigs('[ { "$source": $.items, "o": { "v": $.| } } ]'), ["name", "n", "ok", "extra"]);
  // et quand la boucle est alimentée par un filtre
  assert.deepEqual(sigs('[ { "$source": $.items[?(@.ok == true)], "v": $.| } ]'), ["name", "n", "ok", "extra"]);
});

test("le chemin du $source lui-même se complète depuis la racine", () => {
  assert.deepEqual(sigs('[ { "$source": $.| } ]'), ["user", "items", "seuil"]);
});

test("boucles imbriquées : la portée est celle de la boucle la plus proche", () => {
  const doc = { a: [{ b: [{ c: 1 }], z: 0 }] };
  assert.deepEqual(sigs('[ { "$source": $.a, "x": [ { "$source": $.b, "y": $.| } ] } ]', doc), ["c"]);
});

// La portée d'un `$source` est celle de l'objet qui porte la CLÉ, et d'aucun
// autre : un objet qui contient un bloc de boucle n'est pas lui-même en boucle.
// Le défaut inverse ne levait rien — il rendait un template qui vaut null.
test("après un bloc de boucle refermé, la portée redevient celle de l'objet englobant", () => {
  const doc = {
    Account: [{ Name: "Acme" }],
    Carrier: [{ Carriername: "X", PlatformCode: "P" }],
    Animation: [{ Libelle: "L" }],
  };
  const template = '{ "Carriers": [ { "$source": $.Carrier[*], "Name": $.Carriername } ], "Apres": $.| }';
  assert.deepEqual(sigs(template, doc), ["Account", "Carrier", "Animation"]);
  // Dans le bloc, l'élément : le comportement juste ne change pas.
  const dedans = '{ "Carriers": [ { "$source": $.Carrier[*], "Name": $.| } ], "Apres": 1 }';
  assert.deepEqual(sigs(dedans, doc), ["Carriername", "PlatformCode"]);
});

test("deux boucles côte à côte : chacune reste dans sa portée", () => {
  const doc = { a: [{ x: 1 }], b: [{ y: 2 }] };
  assert.deepEqual(sigs('{ "A": [ { "$source": $.a, "v": $.| } ], "B": [ { "$source": $.b } ] }', doc), ["x"]);
  assert.deepEqual(sigs('{ "A": [ { "$source": $.a } ], "B": [ { "$source": $.b, "v": $.| } ] }', doc), ["y"]);
  // Objet frère du même tableau : sa clé $source n'est pas la nôtre.
  assert.deepEqual(sigs('{ "L": [ { "$source": $.a, "v": $.| }, { "$source": $.b } ] }', doc), ["x"]);
});

test("un $source écrit dans une valeur texte n'ouvre aucune portée", () => {
  assert.deepEqual(sigs('{ "note": "le \"$source\": $.items sert à boucler", "v": $.| }'), [
    "user",
    "items",
    "seuil",
  ]);
});

test("template non refermé : la portée reste celle du niveau, sans exception", () => {
  const doc = { a: [{ x: 1 }], b: 2 };
  // Accolade de la racine manquante : le bloc de boucle est clos, le caret est
  // hors de lui — les clés de la racine, jamais celles de l'élément.
  assert.deepEqual(sigs('{ "A": [ { "$source": $.a, "v": $.x } ], "Apres": $.| ', doc), ["a", "b"]);
  // Bloc de boucle lui-même non refermé : on est dedans, donc l'élément.
  assert.deepEqual(sigs('{ "A": [ { "$source": $.a, "v": $.| ', doc), ["x"]);
});

test("pas de proposition hors contexte de chemin ni dans une chaîne", () => {
  assert.equal(sigs('{ "a": up| }'), null);
  assert.equal(sigs('{ "a|": 1 }'), null);
  assert.equal(sigs('{ "a": "$.u|" }'), null);
  assert.equal(sigs('{ "a": sum($.user.age, 1)| }'), null); // hors de tout chemin
});

test("un chemin déjà écrit se complète encore sur sa dernière clé", () => {
  // Le caret en fin de `$.seuil` : l'utilisateur peut être en train de la taper.
  assert.deepEqual(sigs('{ "a": $.user.name + $.seuil| }'), ["seuil"]);
});

test("document source absent ou invalide : aucune proposition", () => {
  assert.equal(suggestPaths("$.", 2, undefined), null);
  assert.equal(suggestPaths("$.", 2, "{ pas du json"), null);
  assert.equal(suggestPaths("$.", 2, "{}"), null);
});

test("clé inconnue : aucune proposition plutôt qu'une fausse", () => {
  assert.equal(sigs('{ "a": $.zzz.| }'), null);
});

test("le texte JSON est accepté comme document source", () => {
  assert.deepEqual(parseSourceDoc('{"a":1}'), { a: 1 });
  assert.equal(parseSourceDoc("{oops"), undefined);
  assert.equal(parseSourceDoc(null), undefined);
  assert.deepEqual(sigs('{ "x": $.| }', '{"a":1,"b":2}'), ["a", "b"]);
});

test("les propositions portent un libellé de type et de valeur", () => {
  const caret = '{ "a": $.'.length;
  const res = suggestPaths('{ "a": $. }', caret, DOC);
  const byName = Object.fromEntries(res.items.map((i) => [i.name, i.description]));
  assert.equal(byName.user, "objet · 3 clés");
  assert.equal(byName.items, "tableau · 2 éléments");
  assert.equal(byName.seuil, "nombre · 2");
  assert.equal(describeValue("Alice"), 'texte · "Alice"');
  assert.equal(describeValue(true), "booléen · true");
  assert.equal(describeValue(null), "null");
  assert.equal(describeValue([1]), "tableau · 1 élément");
});

test("lecture du texte : début de chemin et décomposition", () => {
  assert.equal(findPathStart("{ x: $.a.b", 10), 5);
  assert.equal(findPathStart("sum(1)", 6), -1);
  assert.equal(findPathStart('{ "a": $.l[?(@.n', 16), 13);
  const p = parsePath('$.a[0]["k"][*]..d.e');
  assert.deepEqual(
    p.segments.map((s) => s.kind),
    ["key", "index", "key", "wildcard", "deep"],
  );
  assert.deepEqual(p.pending, { type: "key", prefix: "e", at: 17 });
  // Un filtre contenant une liste reste apparié correctement.
  const filtered = parsePath("$.l[?(@.id in [2, 3])].n");
  assert.deepEqual(
    filtered.segments.map((s) => s.kind),
    ["key", "filter"],
  );
  assert.equal(filtered.pending.prefix, "n");
  assert.equal(parsePath("$.l[1 + 2]"), null);
});

// --- chemins fournis par l'application hôte ---------------------------------

const HOST_PATHS = [
  "$.Account[0].PickupReference",
  { path: "$.Account[0].Name", type: "string", description: "raison sociale" },
  { path: "$.Client.Id", type: "integer" },
  "$.Tags[*].Label",
];
const HOST_TREE = treeFromPaths(HOST_PATHS);

test("une liste de chemins de l'hôte se complète comme un document", () => {
  assert.deepEqual(sigs('{ "a": $.| }', HOST_TREE), ["Account", "Client", "Tags"]);
  assert.deepEqual(sigs('{ "a": $.Account[0].| }', HOST_TREE), ["PickupReference", "Name"]);
  assert.deepEqual(sigs('{ "a": $.Client.| }', HOST_TREE), ["Id"]);
  assert.equal(
    accept('{ "a": $.Account[0].Pick| }', "PickupReference", HOST_TREE),
    '{ "a": $.Account[0].PickupReference }',
  );
});

test("les sous-scripts d'une liste de chemins ne sont pas inventés", () => {
  // `$.Account[0]` listé seul : pas de `[1]` proposé, mais `[*]` reste juste.
  assert.deepEqual(sigs('{ "a": $.Account[| }', HOST_TREE), ["[*]", "[0]"]);
  assert.deepEqual(sigs('{ "a": $.Tags[| }', HOST_TREE), ["[*]", "[0]"]);
  assert.deepEqual(sigs('{ "a": $.Account.| }', HOST_TREE), ["[*].PickupReference", "[*].Name"]);
});

test("le type déclaré par l'hôte est affiché, à défaut un libellé neutre", () => {
  const caret = '{ "a": $.Account[0].'.length;
  const res = suggestPaths('{ "a": $.Account[0]. }', caret, HOST_TREE);
  const byName = Object.fromEntries(res.items.map((i) => [i.name, i.description]));
  assert.equal(byName.Name, "string · raison sociale");
  assert.equal(byName.PickupReference, "valeur");
});

test("portées @ et $source valent aussi pour les chemins de l'hôte", () => {
  assert.deepEqual(sigs('{ "a": $.Tags[?(@.| }', HOST_TREE), ["Label"]);
  assert.deepEqual(sigs('[ { "$source": $.Tags, "v": $.| } ]', HOST_TREE), ["Label"]);
});

test("treeFromPaths ignore ce qu'il ne sait pas situer", () => {
  assert.equal(treeFromPaths([]), undefined);
  assert.equal(treeFromPaths(["pas un chemin", "$", 42, null, "$..x"]), undefined);
  assert.equal(treeFromPaths(undefined), undefined);
  // Une feuille ne remplace pas un nœud qui porte des enfants.
  const tree = treeFromPaths(["$.a", "$.a.b"]);
  assert.deepEqual(sigs('{ "x": $.a.| }', tree), ["b"]);
});

// --- causes du silence ------------------------------------------------------
//
// Une liste vide ne dit rien : elle valait « tu t'es trompé » ET « il n'y a rien
// ici ». Chaque situation porte donc un code distinct, et l'hôte en tire un
// texte. Un message ne remplace jamais une liste.

/** Cause au caret marqué `|`, ou null. */
function hint(template, doc = DOC) {
  const caret = template.indexOf("|");
  assert.notEqual(caret, -1, "le template doit marquer le caret avec |");
  const text = template.slice(0, caret) + template.slice(caret + 1);
  const h = pathHint(text, caret, doc);
  return h === null ? null : h.code;
}

test("@ hors d'un filtre et @ dans un ?(…) sans crochets sont deux causes distinctes", () => {
  assert.equal(hint('{ "a": @.| }'), "at-outside-filter");
  // Le `[` du tableau englobant ne doit pas passer pour le crochet du filtre.
  assert.equal(hint('[ { "$source": $.items?(@.| > 1) } ]'), "at-filter-without-brackets");
  // `@` dans un sous-script qui n'est pas un filtre : pas un filtre non plus.
  assert.equal(hint('{ "a": $.items[@.| }'), "at-outside-filter");
  // La forme juste n'est pas une cause : elle propose.
  assert.equal(hint('{ "a": $.items[?(@.| }'), null);
});

test("un segment absent du document est nommé", () => {
  assert.equal(hint('{ "a": $.Inconnu.| }'), "unknown-segment");
  const h = pathHint('{ "a": $.Inconnu.', 17, DOC);
  assert.equal(h.data.segment, "Inconnu");
  assert.match(formatHint(h), /^Inconnu n'existe pas/);
});

test("boucle en cours de frappe et boucle qui ne désigne rien se distinguent", () => {
  // `$.ite` est le préfixe d'une clé qui existe : le chemin n'est pas fini.
  assert.equal(hint('[ { "$source": $.ite, "v": $.| } ]'), "loop-source-incomplete");
  // `$.Inconnu[*]` est un chemin fini qui ne mène à aucune collection.
  assert.equal(hint('[ { "$source": $.Inconnu[*], "v": $.| } ]'), "loop-source-empty");
});

test("la collection d'un filtre introuvable ou non résoluble est dite", () => {
  assert.equal(hint('{ "a": $.inconnu[?(@.| }'), "filter-path-empty");
  assert.equal(hint('{ "a": sum($.items)[?(@.| }'), "filter-path-unknown");
});

test("un document source absent ou illisible est dit comme tel", () => {
  assert.equal(pathHint("$.", 2, undefined).code, "no-source-doc");
  assert.equal(pathHint("$.", 2, "{ pas du json").code, "no-source-doc");
});

test("le cas nominal sans enfant se distingue d'une erreur", () => {
  assert.equal(hint('{ "a": $.seuil.| }'), "no-children"); // feuille : rien dessous
  assert.equal(hint('{ "a": $.zz| }'), "no-match"); // bon endroit, aucune clé ainsi
  assert.equal(hint('{ "a": $.user.| }'), null); // des propositions : aucun message
});

test("un message ne remplace jamais une liste, ni ne commente la frappe", () => {
  assert.equal(hint('{ "a": $.| }'), null); // une liste est possible
  assert.equal(hint('{ "a": up| }'), null); // hors de tout chemin
  assert.equal(hint('{ "a": "$.u|" }'), null); // dans une chaîne
  assert.equal(hint('{ "a|": 1 }'), null); // dans une clé
});

test("aucune exception sur un template en cours de frappe", () => {
  const brutal = [
    '{ "a": $.',
    '[ { "$source": $.items, "v": $.',
    '{ "a": [ { "$source": $.items[?(@.',
    '{ "a": "$.items[?(@.ok == \"x',
    '{ "a": $.items[0][*]..',
    "@.",
    "$..",
    '{ "$source": ',
    '{ "a": $.items[?(@.ok)].name[?(@.',
  ];
  for (const text of brutal) {
    for (let caret = 0; caret <= text.length; caret++) {
      assert.doesNotThrow(() => suggestPaths(text, caret, DOC), `suggestPaths @${caret} : ${text}`);
      assert.doesNotThrow(() => pathHint(text, caret, DOC), `pathHint @${caret} : ${text}`);
    }
  }
});

test("les textes sont surchargeables par code, les autres gardent leur défaut", () => {
  const h = pathHint('{ "a": @.', 9, DOC);
  assert.equal(h.code, "at-outside-filter");
  const messages = { ...DEFAULT_HINT_MESSAGES, "at-outside-filter": "@ only inside a [?(…)] filter" };
  assert.equal(formatHint(h, messages), "@ only inside a [?(…)] filter");
  // Code non surchargé : texte livré, et non un silence de retour.
  const leaf = pathHint('{ "a": $.seuil.', 15, DOC);
  assert.equal(formatHint(leaf, messages), DEFAULT_HINT_MESSAGES["no-children"]);
  // Les données de la cause sont substituées dans le texte de l'hôte.
  const seg = pathHint('{ "a": $.Inconnu.', 17, DOC);
  assert.equal(formatHint(seg, { "unknown-segment": "no {segment} here" }), "no Inconnu here");
});

test("chaque cause possible a un texte par défaut", () => {
  const codes = [
    "no-source-doc",
    "at-outside-filter",
    "at-filter-without-brackets",
    "unknown-segment",
    "loop-source-incomplete",
    "loop-source-empty",
    "filter-path-unknown",
    "filter-path-empty",
    "no-children",
    "no-match",
  ];
  for (const code of codes) {
    assert.equal(typeof DEFAULT_HINT_MESSAGES[code], "string", code);
    assert.ok(DEFAULT_HINT_MESSAGES[code].length > 0, code);
  }
});
