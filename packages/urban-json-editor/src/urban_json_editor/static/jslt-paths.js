/*!
 * Complétion des chemins — logique pure, sans DOM.
 *
 * Deux sources possibles, même moteur de complétion :
 *  - un DOCUMENT source (objet/tableau/texte JSON) dont les chemins sont dérivés ;
 *  - une LISTE de chemins calculée par l'application hôte (`setPaths`), pour un
 *    hôte qui connaît son modèle d'entrée sans en avoir d'instance. La liste est
 *    repliée en arbre, ce qui lui fait traverser exactement la même résolution.
 *
 * Séparé de jslt-editor.js parce que le Web Component exige un navigateur alors
 * que cette logique, elle, s'éprouve sous node (voir tests/paths.test.mjs) :
 * c'est la partie où une erreur est silencieuse, donc celle qui doit être testée.
 *
 * Règle de fidélité au moteur : un chemin proposé est un chemin VALIDE. Le
 * moteur ne projette pas sur les tableaux (`$.items.name` vaut null, il faut
 * `$.items[*].name`) ; les clés d'éléments sont donc proposées avec leur `[*]`.
 */

const BAREWORD = /^[A-Za-z_][A-Za-z0-9_]*$/;
const MAX_ITEMS = 50;
//  Au-delà, la liste d'index n'aide plus personne : `[*]` ou une saisie directe.
const MAX_INDEXES = 10;
//  Les portées s'emboîtent (boucle dans une boucle, filtre sur un chemin de
//  boucle) : la résolution est récursive, donc bornée.
const MAX_SCOPE_DEPTH = 8;

/**
 * Messages par défaut des causes de silence, par code.
 *
 * Le composant est consommé par des projets qui ne sont pas tous en français et
 * ne porte aucun dispositif de traduction : chaque cause a donc un CODE stable,
 * et l'hôte remplace tout ou partie du dictionnaire (`setMessages`). Les textes
 * nomment un fait, jamais une intention supposée : « @ ne désigne un élément que
 * dans un filtre » et non « vous vouliez sûrement écrire [?( ».
 */
export const DEFAULT_HINT_MESSAGES = {
  "no-source-doc": "Aucun document source n'est fourni à l'éditeur.",
  "at-outside-filter": "@ ne désigne un élément que dans un filtre [?(…)].",
  "at-filter-without-brackets": "Un filtre s'écrit [?(…)] : sans ses crochets, le moteur refuse la construction.",
  "unknown-segment": "{segment} n'existe pas dans le document source.",
  "loop-source-incomplete": "Le chemin de la boucle ($source) n'est pas encore complet.",
  "loop-source-empty": "La boucle {path} ne désigne aucune collection du document source.",
  "filter-path-unknown": "La collection filtrée n'est pas un chemin que l'éditeur sait résoudre.",
  "filter-path-empty": "{path} ne désigne aucune collection du document source.",
  "no-children": "Rien à proposer sous ce nœud : c'est une valeur, pas un objet ni un tableau.",
  "no-match": "Aucune clé ne commence par « {prefix} » ici.",
};

/**
 * Note la cause du silence dans le collecteur, si collecteur il y a.
 *
 * Première notée, première gardée : la résolution part du caret, donc la
 * première cause rencontrée est la plus proche de ce que l'utilisateur écrit.
 */
function note(hint, code, data) {
  if (hint && !hint.code) {
    hint.code = code;
    hint.data = data || {};
  }
}

/** Message d'une cause, `{clé}` substitué depuis ses données. */
export function formatHint(hint, messages) {
  if (!hint || !hint.code) return null;
  const table = messages || DEFAULT_HINT_MESSAGES;
  const text = table[hint.code] !== undefined ? table[hint.code] : DEFAULT_HINT_MESSAGES[hint.code];
  if (text === undefined) return null;
  return text.replace(/\{(\w+)\}/g, (whole, key) => {
    const v = hint.data ? hint.data[key] : undefined;
    return v === undefined || v === "" ? whole : String(v);
  });
}

/** Feuille d'un arbre construit depuis une liste de chemins : type déclaré. */
export class PathLeaf {
  constructor(type, description) {
    this.type = type || "valeur";
    this.description = description;
  }
}

function isPlainObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v) && !(v instanceof PathLeaf);
}

/** Document source utilisable : objet/tableau tel quel, ou texte JSON analysé. */
export function parseSourceDoc(doc) {
  if (typeof doc !== "string") return doc == null ? undefined : doc;
  try {
    return JSON.parse(doc);
  } catch {
    // JSON en cours de frappe : pas de propositions plutôt que des fausses.
    return undefined;
  }
}

// --- lecture du texte -------------------------------------------------------

/** Index du `[` correspondant au `]` en `close`, ou -1. */
function matchBracketBackwards(text, close) {
  let depth = 0;
  for (let i = close; i >= 0; i--) {
    if (text[i] === "]") depth++;
    else if (text[i] === "[") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return -1;
}

/** Index du `]` fermant le `[` en `open`, ou -1. */
function matchBracketForward(text, open) {
  let depth = 0;
  for (let i = open; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      i = skipStringForward(text, i);
      continue;
    }
    if (c === "[") depth++;
    else if (c === "]") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return -1;
}

/** Index du `$`/`@` qui ouvre le chemin se terminant au caret, ou -1. */
export function findPathStart(text, caret) {
  let i = caret;
  while (i > 0) {
    const c = text[i - 1];
    if (c === "]") {
      const open = matchBracketBackwards(text, i - 1);
      if (open === -1) return -1;
      i = open;
      continue;
    }
    if (c === "[" || /[A-Za-z0-9_.]/.test(c)) {
      i -= 1;
      continue;
    }
    return c === "$" || c === "@" ? i - 1 : -1;
  }
  return -1;
}

/**
 * Décompose le texte d'un chemin en segments résolus + le segment en cours de
 * frappe (`pending`), seul candidat à la complétion. `null` si le texte n'est
 * pas un chemin que l'on sait résoudre (expression dans un sous-script…).
 */
export function parsePath(text) {
  const root = text[0];
  if (root !== "$" && root !== "@") return null;
  const segments = [];
  let pending = null;
  let i = 1;
  while (i < text.length) {
    const c = text[i];
    if (c === ".") {
      const deep = text[i + 1] === ".";
      i += deep ? 2 : 1;
      const m = /^[A-Za-z_][A-Za-z0-9_]*/.exec(text.slice(i));
      const key = m ? m[0] : "";
      i += key.length;
      if (i >= text.length) {
        pending = { type: deep ? "deepKey" : "key", prefix: key, at: i - key.length - (deep ? 2 : 1) };
      } else if (key === "") {
        return null;
      } else {
        segments.push({ kind: deep ? "deep" : "key", key });
      }
      continue;
    }
    if (c === "[") {
      // Crochets appariés, car un filtre peut en contenir : `[?(@.id in [2, 3])]`.
      const close = matchBracketForward(text, i);
      if (close === -1) {
        pending = { type: "subscript", prefix: text.slice(i + 1), at: i + 1 };
        break;
      }
      const inner = text.slice(i + 1, close).trim();
      i = close + 1;
      if (inner === "*") segments.push({ kind: "wildcard" });
      else if (/^-?\d+$/.test(inner)) segments.push({ kind: "index", index: Number(inner) });
      else if (/^"[^"]*"$|^'[^']*'$/.test(inner)) segments.push({ kind: "key", key: inner.slice(1, -1) });
      else if (inner.startsWith("?")) segments.push({ kind: "filter" });
      else return null;
      continue;
    }
    return null;
  }
  return { root, segments, pending };
}

/**
 * Segments d'un chemin déjà ÉCRIT en entier (collection d'un filtre, chemin
 * d'une boucle) : son dernier segment, que `parsePath` rend « en cours de
 * frappe » faute de savoir où s'arrête la saisie, y est un segment comme un
 * autre. `null` si le chemin est réellement incomplet.
 */
function completedSegments(parsed) {
  const p = parsed.pending;
  if (!p) return parsed.segments;
  if (p.type === "key" && p.prefix) return [...parsed.segments, { kind: "key", key: p.prefix }];
  if (p.type === "deepKey" && p.prefix) return [...parsed.segments, { kind: "deep", key: p.prefix }];
  return null;
}

/** Index du `{` ouvrant non refermé avant `caret`, ou -1. */
function enclosingObject(text, caret) {
  let depth = 0;
  let i = caret - 1;
  while (i >= 0) {
    const c = text[i];
    if (c === '"') {
      i = closeStringBackwards(text, i);
      continue;
    }
    if (c === "}") depth++;
    else if (c === "{") {
      if (depth === 0) return i;
      depth--;
    }
    i--;
  }
  return -1;
}

/** Index juste avant le guillemet ouvrant de la chaîne qui se ferme en `i`. */
function closeStringBackwards(text, i) {
  for (let j = i - 1; j >= 0; j--) {
    if (text[j] !== '"') continue;
    let bs = 0;
    for (let k = j - 1; k >= 0 && text[k] === "\\"; k--) bs++;
    if (bs % 2 === 0) return j - 1;
  }
  return -1;
}

/** Fin de l'objet ouvert en `start` (index du `}`), ou la fin du texte. */
function objectEnd(text, start) {
  let depth = 0;
  for (let i = start; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      i = skipStringForward(text, i);
      continue;
    }
    if (c === "{") depth++;
    else if (c === "}") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return text.length;
}

function skipStringForward(text, i) {
  for (let j = i + 1; j < text.length; j++) {
    if (text[j] === "\\") j++;
    else if (text[j] === '"') return j;
  }
  return text.length;
}

/**
 * Index de la valeur de la clé PROPRE `"$source"` dans le corps d'un objet
 * (`body` commence au `{`), ou -1.
 *
 * La clé doit être au niveau de l'objet lui-même : un `"$source"` d'un objet ou
 * d'un tableau imbriqué appartient à cette boucle-là, pas à celle-ci. Chercher
 * la chaîne dans tout le corps faisait lire la racine comme une boucle dès
 * qu'un bloc de boucle s'y trouvait — propositions crédibles et fausses, hors
 * du bloc. Les chaînes sont sautées : un `$source` écrit dans une valeur texte
 * n'est pas une clé.
 */
function ownSourceValueStart(body) {
  let depth = 0;
  for (let i = 0; i < body.length; i++) {
    const c = body[i];
    if (c === '"') {
      const close = skipStringForward(body, i);
      if (depth === 1 && body.slice(i + 1, close) === "$source") {
        const colon = /^\s*:\s*/.exec(body.slice(close + 1));
        if (colon) return close + 1 + colon[0].length;
      }
      i = close;
      continue;
    }
    if (c === "{" || c === "[" || c === "(") depth++;
    else if (c === "}" || c === "]" || c === ")") {
      depth--;
      // Objet refermé (ou texte déséquilibré) : rien au-delà ne lui appartient.
      if (depth <= 0) break;
    }
  }
  return -1;
}

/** Chemin donné à la clé propre `"$source"` de l'objet [start, end], ou null. */
function sourceExpression(text, start, end) {
  const body = text.slice(start, end);
  const from = ownSourceValueStart(body);
  if (from === -1) return null;
  let i = from;
  let depth = 0;
  for (; i < body.length; i++) {
    const c = body[i];
    if (c === '"') {
      i = skipStringForward(body, i);
      continue;
    }
    if (c === "[" || c === "(" || c === "{") depth++;
    else if (c === "]" || c === ")") depth--;
    else if (c === "}") {
      if (depth === 0) break;
      depth--;
    } else if (c === "," && depth === 0) break;
  }
  const expr = body.slice(from, i).trim();
  if (!expr.startsWith("$") && !expr.startsWith("@")) return null;
  return { expr, from: start + from, to: start + i };
}

// --- résolution -------------------------------------------------------------

function descendants(node, key, out) {
  if (Array.isArray(node)) {
    for (const v of node) descendants(v, key, out);
  } else if (isPlainObject(node)) {
    for (const [k, v] of Object.entries(node)) {
      if (k === key) out.push(v);
      descendants(v, key, out);
    }
  }
  return out;
}

/** Nœuds atteints depuis `nodes` en suivant `segments`. */
export function resolveSegments(nodes, segments) {
  let current = nodes;
  for (const seg of segments) {
    const next = [];
    for (const node of current) {
      if (seg.kind === "key") {
        if (isPlainObject(node) && Object.hasOwn(node, seg.key)) next.push(node[seg.key]);
      } else if (seg.kind === "index") {
        if (Array.isArray(node)) {
          const idx = seg.index < 0 ? node.length + seg.index : seg.index;
          if (idx >= 0 && idx < node.length) next.push(node[idx]);
        }
      } else if (seg.kind === "wildcard" || seg.kind === "filter") {
        // Un filtre sélectionne des éléments : pour la complétion, il se
        // comporte comme `[*]` (`$.l[?(@.ok)].name` est valide, cf. guide §13).
        if (Array.isArray(node)) next.push(...node);
        else if (isPlainObject(node)) next.push(...Object.values(node));
      } else if (seg.kind === "deep") {
        next.push(...descendants(node, seg.key, []));
      }
    }
    current = next;
  }
  return current;
}

/**
 * Nœuds que désigne la racine du chemin qui commence à `start`.
 *
 * `$` est la racine du document — sauf dans un objet de boucle `"$source"`, où
 * il désigne l'élément courant (guide §12) ; `@` est l'élément courant du
 * filtre `[?(…)]` englobant (guide §13). Sans ces deux reprises de portée,
 * l'intellisense proposerait les clés de la racine là où le moteur lit celles
 * d'un élément — le pire des cas : des propositions crédibles et fausses.
 */
export function scopeNodes(text, start, doc, depth = 0, hint = null) {
  if (depth > MAX_SCOPE_DEPTH) return [];
  if (text[start] === "@") return filterScope(text, start, doc, depth, hint);
  let at = start;
  for (let i = 0; i < MAX_SCOPE_DEPTH; i++) {
    const open = enclosingObject(text, at);
    if (open === -1) break;
    const loop = sourceExpression(text, open, objectEnd(text, open));
    // Le caret dans l'expression `$source` elle-même se résout dans la portée
    // ENGLOBANTE : la boucle ne s'ouvre qu'une fois son chemin écrit.
    if (loop !== null && !(start >= loop.from && start < loop.to)) {
      const parsed = parsePath(loop.expr);
      const segments = parsed && completedSegments(parsed);
      if (!segments) {
        note(hint, "loop-source-incomplete", { path: loop.expr });
        return [];
      }
      const outer = scopeNodes(text, loop.from, doc, depth + 1, hint);
      const elements = elementsOf(resolveSegments(outer, segments));
      if (elements.length === 0) {
        const code = beingTyped(outer, segments, parsed) ? "loop-source-incomplete" : "loop-source-empty";
        note(hint, code, { path: loop.expr });
      }
      return elements;
    }
    at = open; // objet simple : la portée est celle de l'objet englobant
  }
  if (doc === undefined) {
    note(hint, "no-source-doc");
    return [];
  }
  return [doc];
}

/**
 * Vrai si le dernier segment du chemin est le PRÉFIXE d'une clé qui existe à ce
 * niveau : le chemin est en cours de frappe. Sans cette distinction, un
 * `"$source": $.Anim` encore incomplet s'annonçait « ne désigne aucune
 * collection », ce qui envoie chercher une erreur là où il n'y en a pas.
 */
function beingTyped(outer, segments, parsed) {
  const last = segments[segments.length - 1];
  if (!parsed.pending || !last || (last.kind !== "key" && last.kind !== "deep")) return false;
  const parents = resolveSegments(outer, segments.slice(0, -1));
  const prefix = last.key.toLowerCase();
  for (const [k] of keysOf(parents)) {
    if (k.length > last.key.length && k.toLowerCase().startsWith(prefix)) return true;
  }
  return false;
}

/** Éléments des tableaux de `nodes` (un non-tableau est son propre élément). */
function elementsOf(nodes) {
  const out = [];
  for (const n of nodes) {
    if (Array.isArray(n)) out.push(...n);
    else out.push(n);
  }
  return out;
}

/**
 * Vrai si `@` est dans un `?(…)` écrit SANS ses crochets (`$.l?(@.x)`), forme
 * que le moteur refuse. À vérifier avant le balayage des crochets : un `[`
 * ouvert plus haut (un tableau du template) n'est pas le crochet du filtre.
 */
function bracketlessFilter(text, atIndex) {
  let depth = 0;
  for (let i = atIndex - 1; i >= 0; i--) {
    const c = text[i];
    if (c === ")") depth++;
    else if (c === "(") {
      if (depth > 0) {
        depth--;
        continue;
      }
      const before = text.slice(0, i).replace(/\s+$/, "");
      if (!before.endsWith("?")) return false;
      return !before.slice(0, -1).replace(/\s+$/, "").endsWith("["); // `[?(` est la forme juste
    }
  }
  return false;
}

function filterScope(text, atIndex, doc, depth, hint = null) {
  if (bracketlessFilter(text, atIndex)) {
    note(hint, "at-filter-without-brackets");
    return [];
  }
  let bracketDepth = 0;
  for (let i = atIndex - 1; i >= 0; i--) {
    const c = text[i];
    if (c === "]") bracketDepth++;
    else if (c === "[") {
      if (bracketDepth > 0) {
        bracketDepth--;
        continue;
      }
      if (!/^\[\s*\?/.test(text.slice(i))) {
        note(hint, "at-outside-filter");
        return [];
      }
      const start = findPathStart(text, i);
      const parsed = start === -1 ? null : parsePath(text.slice(start, i));
      const segments = parsed && completedSegments(parsed);
      if (!segments) {
        note(hint, "filter-path-unknown");
        return [];
      }
      const outer = scopeNodes(text, start, doc, depth + 1, hint);
      const elements = elementsOf(resolveSegments(outer, segments));
      if (elements.length === 0) {
        note(hint, "filter-path-empty", { path: text.slice(start, i) });
      }
      return elements;
    }
  }
  // Aucun crochet ouvert avant `@` : soit un filtre écrit sans ses crochets
  // (`$.l?(@.x)`, que le moteur refuse), soit `@` hors de tout filtre. Les deux
  // rendaient la même liste vide, donc le même silence.
  note(hint, /\?\s*\(\s*$/.test(text.slice(0, atIndex)) ? "at-filter-without-brackets" : "at-outside-filter");
  return [];
}

// --- propositions -----------------------------------------------------------

function truncate(s, n) {
  return s.length <= n ? s : `${s.slice(0, n - 1)}…`;
}

/** Libellé de type/valeur affiché sous une proposition. */
export function describeValue(v) {
  if (v instanceof PathLeaf) return v.description ? `${v.type} · ${v.description}` : v.type;
  if (v === null) return "null";
  if (Array.isArray(v)) return `tableau · ${v.length} élément${v.length > 1 ? "s" : ""}`;
  if (isPlainObject(v)) {
    const n = Object.keys(v).length;
    return `objet · ${n} clé${n > 1 ? "s" : ""}`;
  }
  if (typeof v === "string") return `texte · ${truncate(JSON.stringify(v), 32)}`;
  if (typeof v === "number") return `nombre · ${v}`;
  if (typeof v === "boolean") return `booléen · ${v}`;
  return typeof v;
}

function keyAccess(key) {
  return BAREWORD.test(key) ? `.${key}` : `[${JSON.stringify(key)}]`;
}

/** Clés des objets de `nodes`, dans l'ordre de première apparition. */
function keysOf(nodes) {
  const seen = new Map();
  for (const n of nodes) {
    if (!isPlainObject(n)) continue;
    for (const [k, v] of Object.entries(n)) if (!seen.has(k)) seen.set(k, v);
  }
  return seen;
}

function deepKeysOf(nodes) {
  const seen = new Map();
  const walk = (node) => {
    if (Array.isArray(node)) node.forEach(walk);
    else if (isPlainObject(node)) {
      for (const [k, v] of Object.entries(node)) {
        if (!seen.has(k)) seen.set(k, v);
        walk(v);
      }
    }
  };
  nodes.forEach(walk);
  return seen;
}

/** Caret dans une chaîne littérale (heuristique : guillemets impairs avant). */
function insideString(text, caret) {
  const before = text.slice(0, caret);
  let count = 0;
  for (let i = 0; i < before.length; i++) {
    if (before[i] === "\\") i++;
    else if (before[i] === '"') count++;
  }
  return count % 2 === 1;
}

/**
 * Propositions de chemins au caret, ou `null` hors contexte de chemin.
 *
 * Retourne `{items, from, to}` : les items portent `signature`/`description`
 * (affichage) et `insert` (texte à substituer dans `[from, to)`), de la même
 * forme que les items de fonctions afin que l'éditeur n'ait qu'une liste.
 */
export function suggestPaths(text, caret, source) {
  return resolveSuggestions(text, caret, source, null);
}

/**
 * Cause du silence au caret, ou `null`.
 *
 * Rendue UNIQUEMENT quand aucune liste n'était possible : un message ne remplace
 * jamais des propositions. `null` aussi quand le caret n'est pas dans un chemin
 * — un message répond à un geste, il ne commente pas la frappe.
 */
export function pathHint(text, caret, source) {
  const hint = {};
  let items;
  try {
    items = resolveSuggestions(text, caret, source, hint);
  } catch {
    // Un template en cours de frappe n'est équilibré ni en accolades ni en
    // guillemets : le repli silencieux vaut mieux qu'une pile dans la console.
    return null;
  }
  if (items !== null) return null;
  return hint.code ? { code: hint.code, data: hint.data } : null;
}

/** Désignation d'un segment dans un message (`.cle`, `[2]`, `[*]`, `..cle`). */
function segmentLabel(seg) {
  if (seg.kind === "key") return seg.key;
  if (seg.kind === "deep") return `..${seg.key}`;
  if (seg.kind === "index") return `[${seg.index}]`;
  if (seg.kind === "filter") return "[?(…)]";
  return "[*]";
}

function resolveSuggestions(text, caret, source, hint) {
  if (insideString(text, caret)) return null;

  const start = findPathStart(text, caret);
  if (start === -1) return null;
  const parsed = parsePath(text.slice(start, caret));
  if (!parsed) return null;

  const pending = parsed.pending;
  // Chemin complet mais pas de segment en cours : rien à proposer, sauf sur
  // `$`/`@` seul, qui est justement le déclencheur attendu.
  if (!pending && parsed.segments.length > 0) return null;

  const doc = parseSourceDoc(source);
  if (doc === undefined) {
    note(hint, "no-source-doc");
    return null;
  }

  let nodes = scopeNodes(text, start, doc, 0, hint);
  if (nodes.length === 0) return null; // cause notée par scopeNodes/filterScope
  // Segment par segment, pour pouvoir nommer celui qui ne mène à rien : c'est
  // la différence entre « tu t'es trompé de clé » et « il n'y a rien ici ».
  for (const seg of parsed.segments) {
    const next = resolveSegments(nodes, [seg]);
    if (next.length === 0) {
      note(hint, "unknown-segment", { segment: segmentLabel(seg) });
      return null;
    }
    nodes = next;
  }

  const from = pending ? start + pending.at : caret;
  const prefix = (pending ? pending.prefix : "").toLowerCase();
  const matches = (k) => k.toLowerCase().startsWith(prefix);
  const items = [];

  if (pending && pending.type === "subscript") {
    for (const node of nodes) {
      if (Array.isArray(node)) {
        items.push({ name: "*", signature: "[*]", description: `tous les éléments · ${node.length}`, insert: "*]" });
        let listed = 0;
        for (let i = 0; i < node.length && listed < MAX_INDEXES; i++) {
          // Un arbre bâti depuis une liste de chemins est creux : `[2]` seul
          // ne doit pas faire proposer `[0]` et `[1]`, qui n'existent pas.
          if (node[i] === undefined) continue;
          listed++;
          items.push({ name: String(i), signature: `[${i}]`, description: describeValue(node[i]), insert: `${i}]` });
        }
      } else if (isPlainObject(node)) {
        for (const [k, v] of Object.entries(node)) {
          items.push({ name: k, signature: `["${k}"]`, description: describeValue(v), insert: `${JSON.stringify(k)}]` });
        }
      }
      break; // un seul nœud suffit à lister des sous-scripts
    }
    const bare = prefix.replace(/^["']/, "");
    const kept = items.filter((it) => it.name.toLowerCase().startsWith(bare)).slice(0, MAX_ITEMS);
    if (kept.length === 0) note(hint, items.length ? "no-match" : "no-children", { prefix: bare });
    return kept.length ? { items: kept, from, to: caret } : null;
  }

  if (pending && pending.type === "deepKey") {
    const deep = deepKeysOf(nodes);
    for (const [k, v] of deep) {
      if (matches(k)) {
        items.push({
          name: k,
          signature: `..${k}`,
          description: `${describeValue(v)} · à toute profondeur`,
          insert: BAREWORD.test(k) ? `..${k}` : `..[${JSON.stringify(k)}]`,
        });
      }
    }
    const kept = items.slice(0, MAX_ITEMS);
    if (kept.length === 0) note(hint, deep.size ? "no-match" : "no-children", { prefix: pending.prefix });
    return kept.length ? { items: kept, from, to: caret } : null;
  }

  for (const [k, v] of keysOf(nodes)) {
    items.push({ name: k, signature: k, description: describeValue(v), insert: keyAccess(k) });
  }
  // Clés des ÉLÉMENTS quand le chemin désigne un tableau : proposées avec leur
  // `[*]`, sans quoi l'utilisateur écrirait `$.items.name`, qui vaut null.
  const arrays = nodes.filter(Array.isArray);
  if (arrays.length > 0) {
    for (const [k, v] of keysOf(elementsOf(arrays))) {
      items.push({
        name: k,
        signature: `[*].${k}`,
        description: `${describeValue(v)} · dans chaque élément`,
        insert: `[*]${keyAccess(k)}`,
      });
    }
  }
  // Filtrées après coup : la liste complète dit si le silence vient d'un nœud
  // sans enfant ou d'un préfixe qui ne correspond à rien — deux situations que
  // l'utilisateur ne doit pas confondre.
  const kept = items.filter((it) => matches(it.name)).slice(0, MAX_ITEMS);
  if (kept.length === 0) {
    note(hint, items.length ? "no-match" : "no-children", { prefix: pending ? pending.prefix : "" });
  }
  return kept.length ? { items: kept, from, to: caret } : null;
}

// --- chemins fournis par l'hôte ---------------------------------------------

function growInto(container, segments, index, spec) {
  const seg = segments[index];
  if (seg.kind === "deep") return; // `$..x` ne situe rien : non représentable
  const key = seg.kind === "key" ? seg.key : seg.kind === "index" && seg.index >= 0 ? seg.index : 0;
  if (index === segments.length - 1) {
    // Un chemin feuille ne doit pas écraser un nœud déjà porteur d'enfants
    // (l'hôte peut lister `$.a` ET `$.a.b`).
    if (container[key] === undefined) container[key] = new PathLeaf(spec.type, spec.description);
    return;
  }
  const next = segments[index + 1];
  const wantsArray = next.kind !== "key" && next.kind !== "deep";
  let child = container[key];
  if (child === undefined || child instanceof PathLeaf || Array.isArray(child) !== wantsArray) {
    child = wantsArray ? [] : {};
    container[key] = child;
  }
  growInto(child, segments, index + 1, spec);
}

/**
 * Arbre de complétion replié depuis une liste de chemins fournie par l'hôte.
 *
 * Entrées : `"$.a[0].b"` ou `{path, type, description}`. L'arbre obtenu se
 * résout comme un document, à ceci près que ses feuilles portent le type
 * DÉCLARÉ et non une valeur observée : l'hôte qui connaît son modèle d'entrée
 * n'a pas besoin d'en fournir une instance.
 */
export function treeFromPaths(paths) {
  const list = Array.isArray(paths) ? paths : [];
  let root;
  for (const entry of list) {
    const spec = typeof entry === "string" ? { path: entry } : entry || {};
    if (typeof spec.path !== "string") continue;
    const parsed = parsePath(spec.path.trim());
    const segments = parsed && completedSegments(parsed);
    if (!segments || segments.length === 0) continue;
    const wantsArray = segments[0].kind !== "key" && segments[0].kind !== "deep";
    if (root === undefined) root = wantsArray ? [] : {};
    else if (Array.isArray(root) !== wantsArray) continue; // racine incohérente : ignoré
    growInto(root, segments, 0, spec);
  }
  if (root === undefined) return undefined;
  const empty = Array.isArray(root) ? root.length === 0 : Object.keys(root).length === 0;
  return empty ? undefined : root;
}
