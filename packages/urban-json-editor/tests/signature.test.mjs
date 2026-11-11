/**
 * Tests de l'aide à la signature (quel appel, quel paramètre, quelle page).
 *
 * Exécution : `node --test packages/urban-json-editor/tests/` ; également lancés
 * par pytest via test_signature_js.py.
 */

import assert from "node:assert/strict";
import test from "node:test";

import {
  DEFAULT_DOCS_BASE,
  activeParameter,
  callContextAt,
  descriptionFor,
  docLanguage,
  docUrlFor,
  findFunction,
  signatureSegments,
} from "../src/urban_json_editor/static/jslt-signature.js";

const FORMAT = {
  name: "format",
  signature: "format(token, mask, culture)",
  description: "Formate un nombre ou une date",
  description_en: "Formats a number or a date",
  doc: "fonctions/format",
  parameters: [{ name: "token" }, { name: "mask" }, { name: "culture" }],
};

/** Contexte d'appel au caret marqué par `|`. */
function at(template) {
  const caret = template.indexOf("|");
  assert.notEqual(caret, -1, "le template doit marquer le caret avec |");
  return callContextAt(template.slice(0, caret) + template.slice(caret + 1), caret);
}

// --- quel appel entoure le caret ---------------------------------------------

test("aucun appel autour du caret", () => {
  assert.equal(at('{ "a": $.x| }'), null);
  assert.equal(at("|"), null);
});

test("le caret derrière la parenthèse ouvre le premier paramètre", () => {
  assert.deepEqual(at("format(|)"), { name: "format", open: 6, argIndex: 0 });
});

test("la virgule fait passer au paramètre suivant", () => {
  assert.equal(at("format($.d, |)").argIndex, 1);
  assert.equal(at('format($.d, "yyyy", |)').argIndex, 2);
});

test("une virgule dans une chaîne ne compte pas", () => {
  // Sans la traversée des chaînes, « a, b » ferait croire au 2e paramètre.
  assert.equal(at('format($.d, "a, b"|)').argIndex, 1);
});

test("une parenthèse dans une chaîne n'ouvre pas d'appel", () => {
  assert.equal(at('upper("a (b"|)').name, "upper");
});

test("les virgules d'un tableau appartiennent au tableau", () => {
  // `sort($.l, [$.a, $.b], …)` : sans cadre pour `[`, on croirait au 3e paramètre.
  assert.equal(at("sort($.l, [$.a, $.b|], true)").argIndex, 1);
  assert.equal(at("sort($.l, [$.a, $.b], [false, |])").argIndex, 2);
});

test("les virgules d'un objet appartiennent à l'objet", () => {
  assert.equal(at('merge($.a, { "x": 1, "y": 2| })').argIndex, 1);
});

test("un appel imbriqué prend la main, et le rend en se fermant", () => {
  assert.equal(at("format(upper($.n|), $.m)").name, "upper");
  const outer = at("format(upper($.n), |)");
  assert.equal(outer.name, "format");
  assert.equal(outer.argIndex, 1);
});

test("le caret hors des parenthèses ne montre rien", () => {
  assert.equal(at("format($.d, $.m)|"), null);
});

test("l'aide survit à une parenthèse non fermée", () => {
  // C'est l'état normal pendant la saisie : il doit être le mieux traité.
  assert.equal(at("format($.d, |").argIndex, 1);
});

test("une parenthèse sans nom n'est pas un appel", () => {
  assert.equal(at("($.a + |$.b)"), null);
});

// --- quel paramètre est en cours ---------------------------------------------

test("le paramètre actif est mis en gras, et lui seul", () => {
  const segments = signatureSegments(FORMAT, 1);
  assert.deepEqual(
    segments.map((s) => `${s.active ? "*" : ""}${s.text}`),
    ["token", "*mask", "culture"]
  );
});

test("un argument en trop ne met rien en gras", () => {
  assert.equal(activeParameter(FORMAT, 3), -1);
  assert.ok(signatureSegments(FORMAT, 3).every((s) => !s.active));
});

test("un paramètre variadique absorbe les arguments suivants", () => {
  const concat = { name: "concat", parameters: [{ name: "parts", variadic: true }] };
  assert.equal(activeParameter(concat, 4), 0);
  assert.deepEqual(signatureSegments(concat, 4), [{ text: "...parts", active: true }]);
});

test("à défaut de paramètres, la signature écrite est découpée", () => {
  const fn = { name: "f", signature: "f(a, b)" };
  assert.deepEqual(
    signatureSegments(fn, 1).map((s) => s.text),
    ["a", "b"]
  );
  assert.deepEqual(signatureSegments({ name: "pi", signature: "pi()" }, 0), []);
});

test("la fonction est retrouvée sans égard à la casse", () => {
  assert.equal(findFunction([FORMAT], "FORMAT"), FORMAT);
  assert.equal(findFunction([FORMAT], "inconnue"), null);
});

// --- vers quelle documentation -----------------------------------------------

test("la langue de documentation se ramène à fr ou en", () => {
  assert.equal(docLanguage("fr-CA"), "fr");
  assert.equal(docLanguage("FR"), "fr");
  assert.equal(docLanguage("en-GB"), "en");
  assert.equal(docLanguage(undefined), "en");
});

test("le lien pointe la page de la fonction dans la langue du lecteur", () => {
  assert.equal(docUrlFor(FORMAT, "fr-FR"), `${DEFAULT_DOCS_BASE}fonctions/format.md`);
  assert.equal(docUrlFor(FORMAT, "en-US"), `${DEFAULT_DOCS_BASE}fonctions/format.en.md`);
});

test("la base de documentation est surchargeable", () => {
  assert.equal(docUrlFor(FORMAT, "fr", "https://interne/doc"), "https://interne/doc/fonctions/format.md");
});

test("sans page connue, pas de lien", () => {
  // Un lien fabriqué depuis le nom serait mort pour une fonction de plugin.
  assert.equal(docUrlFor({ name: "loadcsv" }, "fr"), null);
});

test("un plugin peut fournir l'URL complète de sa page", () => {
  const fn = { name: "loadcsv", doc: "https://exemple/loadcsv" };
  assert.equal(docUrlFor(fn, "fr"), "https://exemple/loadcsv");
});

test("la description suit la langue, et se replie sur le français", () => {
  assert.equal(descriptionFor(FORMAT, "en"), "Formats a number or a date");
  assert.equal(descriptionFor(FORMAT, "fr"), "Formate un nombre ou une date");
  assert.equal(descriptionFor({ description: "Seulement en français" }, "en"), "Seulement en français");
});
