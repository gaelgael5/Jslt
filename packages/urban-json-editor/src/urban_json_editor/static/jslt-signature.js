/*!
 * Aide à la signature de <jslt-editor> : quel appel entoure le caret, quel
 * paramètre y est en cours de saisie, et vers quelle page de documentation
 * pointer.
 *
 * Logique **pure** (aucun DOM), comme `jslt-paths.js` : elle tourne dans le
 * navigateur mais s'éprouve sous node (`tests/signature.test.mjs`). Le composant
 * ne fait qu'afficher ce qu'elle décide.
 */

/** Base des pages de référence, surchargeable par l'attribut `docs-base`. */
export const DEFAULT_DOCS_BASE = "https://github.com/gaelgael5/Jslt/blob/main/docs/";

const IDENT_END = /[A-Za-z_][A-Za-z0-9_]*$/;

/** Index du guillemet fermant d'une chaîne ouverte en `start`. */
function endOfString(text, start) {
  const quote = text[start];
  for (let i = start + 1; i < text.length; i++) {
    if (text[i] === "\\") {
      i++; // échappement : le caractère suivant ne ferme jamais la chaîne
      continue;
    }
    if (text[i] === quote) return i;
  }
  // Chaîne non terminée (saisie en cours) : tout le reste en fait partie, donc
  // aucune parenthèse au-delà ne compte — sinon une accolade écrite dans un
  // texte déséquilibrerait la pile et l'aide disparaîtrait sans raison visible.
  return text.length;
}

/** Nom de fonction écrit juste avant la parenthèse `open`, ou `null`. */
function nameBefore(text, open) {
  let end = open;
  while (end > 0 && /\s/.test(text[end - 1])) end--;
  const m = IDENT_END.exec(text.slice(0, end));
  return m ? m[0] : null;
}

/**
 * Appel de fonction qui entoure le caret : `{name, open, argIndex}` ou `null`.
 *
 * Les crochets et accolades empilent un cadre **sans nom** : une virgule de
 * tableau ou d'objet appartient à ce cadre, pas à l'appel qui le contient, donc
 * `sort($.l, [$.a, $.b], [false, true])` reste au 2e paramètre pendant qu'on
 * écrit le tableau de clefs. On remonte ensuite la pile jusqu'au premier cadre
 * nommé : écrire au fond d'un littéral garde l'aide de l'appel englobant.
 */
export function callContextAt(text, caret) {
  const source = String(text == null ? "" : text);
  const limit = Math.max(0, Math.min(caret == null ? 0 : caret, source.length));
  const stack = [];
  for (let i = 0; i < limit; i++) {
    const ch = source[i];
    if (ch === '"' || ch === "'") {
      i = endOfString(source, i);
      continue;
    }
    if (ch === "(") {
      stack.push({ name: nameBefore(source, i), open: i, argIndex: 0 });
      continue;
    }
    if (ch === "[" || ch === "{") {
      stack.push({ name: null, open: i, argIndex: 0 });
      continue;
    }
    if (ch === ")" || ch === "]" || ch === "}") {
      stack.pop();
      continue;
    }
    if (ch === "," && stack.length > 0) stack[stack.length - 1].argIndex++;
  }
  for (let depth = stack.length - 1; depth >= 0; depth--) {
    const frame = stack[depth];
    if (frame.name) return { name: frame.name, open: frame.open, argIndex: frame.argIndex };
  }
  return null;
}

/** Entrée du catalogue portant ce nom (casse ignorée), ou `null`. */
export function findFunction(catalog, name) {
  if (!Array.isArray(catalog) || !name) return null;
  const needle = String(name).toLowerCase();
  return catalog.find((f) => f && String(f.name).toLowerCase() === needle) || null;
}

/** Noms des paramètres, depuis le catalogue ou, à défaut, la signature écrite. */
function parameterNames(fn) {
  if (fn && Array.isArray(fn.parameters)) {
    return fn.parameters.map((p) => (p.variadic ? `...${p.name}` : p.name));
  }
  const written = fn && typeof fn.signature === "string" ? fn.signature : "";
  const inner = written.slice(written.indexOf("(") + 1, written.lastIndexOf(")"));
  return inner.trim() === "" ? [] : inner.split(",").map((p) => p.trim());
}

/** Position du paramètre en cours de saisie, ou -1 si l'argument est en trop. */
export function activeParameter(fn, argIndex) {
  const params = fn && Array.isArray(fn.parameters) ? fn.parameters : null;
  const count = parameterNames(fn).length;
  if (argIndex < count) return argIndex;
  // Variadique : tous les arguments suivants tombent dans le dernier paramètre.
  if (params && params.length > 0 && params[params.length - 1].variadic) return params.length - 1;
  // Argument surnuméraire : rien n'est mis en gras. Le moteur le refusera, et
  // désigner un paramètre au hasard laisserait croire que l'appel est valable.
  return -1;
}

/** Segments à rendre : `[{text, active}]`, un par paramètre. */
export function signatureSegments(fn, argIndex) {
  const active = activeParameter(fn, argIndex);
  return parameterNames(fn).map((text, index) => ({ text, active: index === active }));
}

/** Langue de documentation retenue pour une étiquette BCP 47 (`fr-CA` -> `fr`). */
export function docLanguage(tag) {
  return String(tag == null ? "" : tag).toLowerCase().startsWith("fr") ? "fr" : "en";
}

/**
 * URL de la page de référence d'une fonction, ou `null` s'il n'y en a pas.
 *
 * Le chemin vient du catalogue (`doc`), pas du nom : une fonction de plugin n'a
 * pas sa page dans ce dépôt, et fabriquer l'URL depuis le nom donnerait un lien
 * mort — pire qu'un lien absent, parce qu'on y clique.
 */
export function docUrlFor(fn, lang, base) {
  const doc = fn && fn.doc;
  if (!doc) return null;
  if (/^https?:\/\//i.test(doc)) return doc; // page fournie par un plugin
  const root = base || DEFAULT_DOCS_BASE;
  const prefix = root.endsWith("/") ? root : `${root}/`;
  return `${prefix}${doc}${docLanguage(lang) === "fr" ? ".md" : ".en.md"}`;
}

/**
 * Description dans la langue demandée.
 *
 * Repli volontaire sur le français quand la traduction manque (cas d'un plugin
 * tiers) : une infobulle vide n'apprendrait rien, là où la description d'origine
 * reste utile même dans l'autre langue.
 */
export function descriptionFor(fn, lang) {
  if (!fn) return "";
  if (docLanguage(lang) === "en" && fn.description_en) return fn.description_en;
  return fn.description || "";
}
