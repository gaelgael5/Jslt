/*!
 * <jslt-editor> — éditeur jslt réutilisable (coloration syntaxique + intellisense).
 *
 * Web Component autonome, sans dépendance : utilisable dans n'importe quel projet
 * (Python ou autre) qui sert ce fichier + jslt-editor.css.
 *
 * Usage :
 *   <link rel="stylesheet" href="/jslt-editor/jslt-editor.css">
 *   <script type="module" src="/jslt-editor/jslt-editor.js"></script>
 *   <jslt-editor id="ed" catalog-url="/api/functions"></jslt-editor>
 *   ed.value = '{ "n": $.x }';           // get/set du contenu
 *   ed.setCatalog([{name, signature, description, parameters}]);  // intellisense
 *   ed.source = '{ "x": 1 }';             // document source -> chemins proposés
 *   ed.setPaths(["$.a[0].b"]);            // ou la liste de chemins de l'hôte
 *   ed.addEventListener("input", ...);    // émis à chaque modification
 *
 * La coloration et l'autocomplétion sont purement présentationnelles : la source
 * de vérité reste le texte (propriété `value`).
 */

import { findPathStart, parseSourceDoc, suggestPaths, treeFromPaths } from "./jslt-paths.js";

const KEYWORDS = new Set(["when", "switch", "default", "true", "false", "null"]);

// Tokenizer jslt → suite de {type, text}. Volontairement tolérant (présentation).
function tokenize(src) {
  const tokens = [];
  const re =
    /("(?:[^"\\]|\\.)*"?)|('(?:[^'\\]|\\.)*'?)|(#[A-Za-z]+)|(\$\.\.|\$\.|\$|@)|([A-Za-z_][A-Za-z0-9_]*)|(-?\d+\.\d+|-?\d+)|(\?\?|->|==|!=|>=|<=|&&|\|\||[-+*/%<>!&|^?:])|(\s+)|([\s\S])/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    if (m[1] !== undefined) tokens.push({ type: "string", text: m[1] });
    else if (m[2] !== undefined) tokens.push({ type: "string", text: m[2] });
    else if (m[3] !== undefined) tokens.push({ type: "cast", text: m[3] });
    else if (m[4] !== undefined) tokens.push({ type: "path", text: m[4] });
    else if (m[5] !== undefined) {
      // mot : fonction si suivi de '(', mot-clé, ou identifiant/chemin
      const rest = src.slice(re.lastIndex);
      if (KEYWORDS.has(m[5])) tokens.push({ type: "keyword", text: m[5] });
      else if (/^\s*\(/.test(rest)) tokens.push({ type: "function", text: m[5] });
      else tokens.push({ type: "ident", text: m[5] });
    } else if (m[6] !== undefined) tokens.push({ type: "number", text: m[6] });
    else if (m[7] !== undefined) tokens.push({ type: "operator", text: m[7] });
    else if (m[8] !== undefined) tokens.push({ type: "ws", text: m[8] });
    else tokens.push({ type: "punct", text: m[9] });
  }
  return tokens;
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlight(src) {
  let out = "";
  for (const t of tokenize(src)) {
    const text = escapeHtml(t.text);
    out += t.type === "ws" ? text : `<span class="tok-${t.type}">${text}</span>`;
  }
  // Un saut de ligne final garantit que la dernière ligne est rendue.
  return out + "\n";
}

const TEMPLATE = document.createElement("template");
TEMPLATE.innerHTML = `
  <div class="jslt-editor" part="editor">
    <pre class="jslt-highlight" aria-hidden="true"><code></code></pre>
    <textarea class="jslt-input" spellcheck="false" autocomplete="off"
              autocapitalize="off" autocorrect="off" wrap="off"></textarea>
    <div class="jslt-ac" role="listbox" hidden></div>
  </div>
`;

class JsltEditor extends HTMLElement {
  constructor() {
    super();
    this._catalog = [];
    this._source = undefined;
    this._paths = [];
    this._pathTree = undefined;
    this._ac = { open: false, items: [], index: 0, from: 0, to: 0 };
  }

  connectedCallback() {
    if (this._wired) return;
    this._wired = true;
    this.appendChild(TEMPLATE.content.cloneNode(true));
    this._root = this.querySelector(".jslt-editor");
    this._pre = this.querySelector(".jslt-highlight code");
    this._ta = this.querySelector(".jslt-input");
    this._acEl = this.querySelector(".jslt-ac");

    if (this.hasAttribute("value")) this._ta.value = this.getAttribute("value");
    // Chargé en module (différé), le composant est souvent défini APRÈS que la
    // page a écrit `el.value = …` : l'écriture a alors créé une propriété propre
    // qui masque l'accesseur de la classe, et la page lit ensuite cette valeur
    // figée au lieu de la saisie. On la reprend puis on la retire (patron
    // « lazy property » des custom elements).
    if (Object.prototype.hasOwnProperty.call(this, "value")) {
      const early = this.value;
      delete this.value;
      this._ta.value = early == null ? "" : String(early);
    }
    // Même piège pour les sources de chemins, souvent posées dès le chargement.
    for (const prop of ["source", "paths"]) {
      if (!Object.prototype.hasOwnProperty.call(this, prop)) continue;
      const early = this[prop];
      delete this[prop];
      this[prop] = early;
    }

    this._ta.addEventListener("input", () => this._onInput());
    this._ta.addEventListener("scroll", () => this._syncScroll());
    this._ta.addEventListener("keydown", (e) => this._onKeyDown(e));
    this._ta.addEventListener("blur", () => setTimeout(() => this._closeAc(), 120));
    this._acEl.addEventListener("mousedown", (e) => this._onAcMouseDown(e));

    const url = this.getAttribute("catalog-url");
    if (url) this._fetchCatalog(url);
    const pathsUrl = this.getAttribute("paths-url");
    if (pathsUrl) this._fetchPaths(pathsUrl);

    this._render();
  }

  // --- API publique --------------------------------------------------------
  get value() {
    return this._ta ? this._ta.value : this.getAttribute("value") || "";
  }
  set value(v) {
    const text = v == null ? "" : String(v);
    if (this._ta) {
      this._ta.value = text;
      this._render();
    } else {
      this.setAttribute("value", text);
    }
  }
  setCatalog(catalog) {
    this._catalog = Array.isArray(catalog) ? catalog : [];
  }
  /** Document source (objet/tableau, ou son texte JSON) : alimente les chemins. */
  get source() {
    return this._source;
  }
  set source(doc) {
    this.setSource(doc);
  }
  setSource(doc) {
    // Analysé une fois ici, pas à chaque frappe dans le template : l'appelant
    // repose typiquement le texte JSON à chaque modification de son éditeur.
    this._source = parseSourceDoc(doc);
  }
  /**
   * Chemins calculés par l'application hôte : `"$.a[0].b"` ou
   * `{path, type, description}`. Pour un hôte qui connaît son modèle d'entrée
   * sans en avoir d'instance — le composant ne lit aucun schéma, il ne replie
   * que ce qu'on lui donne.
   */
  get paths() {
    return this._paths;
  }
  set paths(list) {
    this.setPaths(list);
  }
  setPaths(list) {
    this._paths = Array.isArray(list) ? list : [];
    this._pathTree = treeFromPaths(this._paths);
  }

  async _fetchCatalog(url) {
    try {
      const resp = await fetch(url);
      const data = await resp.json();
      this.setCatalog(data.functions || data);
    } catch {
      /* intellisense simplement indisponible */
    }
  }

  async _fetchPaths(url) {
    try {
      const resp = await fetch(url);
      const data = await resp.json();
      this.setPaths(data.paths || data);
    } catch {
      /* complétion des chemins simplement indisponible */
    }
  }

  // --- rendu / coloration --------------------------------------------------
  _onInput() {
    this._render();
    this._maybeOpenAc();
    this.dispatchEvent(new Event("input", { bubbles: true }));
  }
  _render() {
    this._pre.innerHTML = highlight(this._ta.value);
    this._syncScroll();
  }
  _syncScroll() {
    this._pre.parentElement.scrollTop = this._ta.scrollTop;
    this._pre.parentElement.scrollLeft = this._ta.scrollLeft;
  }

  // --- intellisense --------------------------------------------------------
  _wordBeforeCaret() {
    const pos = this._ta.selectionStart;
    const before = this._ta.value.slice(0, pos);
    const m = /([A-Za-z_][A-Za-z0-9_]*)$/.exec(before);
    if (!m) return null;
    // Pas d'autocomplétion à l'intérieur d'une chaîne (heuristique : nb de " impair).
    const quotes = (before.match(/"/g) || []).length;
    if (quotes % 2 === 1) return null;
    return { word: m[1], from: pos - m[1].length, to: pos };
  }
  _maybeOpenAc() {
    const text = this._ta.value;
    const caret = this._ta.selectionStart;
    // Les chemins de l'hôte font foi quand il en fournit : ils décrivent son
    // modèle d'entrée, là où un document n'en est qu'une instance.
    const paths = suggestPaths(text, caret, this._pathTree !== undefined ? this._pathTree : this._source);
    if (paths) {
      this._ac = { open: true, items: paths.items, index: 0, from: paths.from, to: paths.to };
      return this._renderAc();
    }
    // Dans un chemin, les fonctions ne sont pas des candidats : `$.us` ne se
    // complète pas en `upper()`. Mieux vaut aucune proposition qu'une fausse.
    if (findPathStart(text, caret) !== -1) return this._closeAc();
    const w = this._wordBeforeCaret();
    if (!w || w.word.length < 1) return this._closeAc();
    const needle = w.word.toLowerCase();
    const items = this._catalog
      .filter((f) => f.name.toLowerCase().startsWith(needle))
      .slice(0, 50);
    if (items.length === 0) return this._closeAc();
    this._ac = { open: true, items, index: 0, from: w.from, to: w.to };
    this._renderAc();
  }
  _renderAc() {
    const { items, index } = this._ac;
    this._acEl.innerHTML = items
      .map(
        (f, i) =>
          `<div class="jslt-ac-item${i === index ? " active" : ""}" data-i="${i}" role="option">
             <span class="jslt-ac-sig">${escapeHtml(f.signature || f.name)}</span>
             ${f.description ? `<span class="jslt-ac-desc">${escapeHtml(f.description)}</span>` : ""}
           </div>`
      )
      .join("");
    this._positionAc();
    this._acEl.hidden = false;
  }
  _positionAc() {
    // Coordonnées du caret via une div-miroir (technique standard).
    const pos = this._ac.from;
    const style = getComputedStyle(this._ta);
    const mirror = document.createElement("div");
    const props = [
      "boxSizing", "width", "paddingTop", "paddingRight", "paddingBottom",
      "paddingLeft", "borderWidth", "fontFamily", "fontSize", "lineHeight",
      "letterSpacing", "whiteSpace", "wordWrap",
    ];
    for (const p of props) mirror.style[p] = style[p];
    mirror.style.position = "absolute";
    mirror.style.visibility = "hidden";
    mirror.style.whiteSpace = "pre-wrap";
    mirror.style.overflowWrap = "break-word";
    mirror.textContent = this._ta.value.slice(0, pos);
    const marker = document.createElement("span");
    marker.textContent = "​";
    mirror.appendChild(marker);
    this._root.appendChild(mirror);
    const top = marker.offsetTop - this._ta.scrollTop + marker.offsetHeight;
    const left = marker.offsetLeft - this._ta.scrollLeft;
    this._root.removeChild(mirror);
    this._acEl.style.top = `${top}px`;
    this._acEl.style.left = `${left}px`;
  }
  _closeAc() {
    if (this._ac.open) {
      this._ac.open = false;
      this._acEl.hidden = true;
    }
  }
  _accept() {
    const f = this._ac.items[this._ac.index];
    if (!f) return;
    const v = this._ta.value;
    // Un item de chemin porte son texte d'insertion (`.name`, `[*].name`, `0]`…) ;
    // une fonction s'insère appelée, caret entre les parenthèses.
    const insert = f.insert !== undefined ? f.insert : `${f.name}()`;
    this._ta.value = v.slice(0, this._ac.from) + insert + v.slice(this._ac.to);
    const caret = this._ac.from + (f.insert !== undefined ? insert.length : f.name.length + 1);
    this._ta.selectionStart = this._ta.selectionEnd = caret;
    this._closeAc();
    this._render();
    this.dispatchEvent(new Event("input", { bubbles: true }));
  }
  _onAcMouseDown(e) {
    const item = e.target.closest(".jslt-ac-item");
    if (!item) return;
    e.preventDefault();
    this._ac.index = Number(item.dataset.i);
    this._accept();
  }
  _onKeyDown(e) {
    if (this._ac.open) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        this._ac.index = (this._ac.index + 1) % this._ac.items.length;
        return this._renderAc();
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        this._ac.index = (this._ac.index - 1 + this._ac.items.length) % this._ac.items.length;
        return this._renderAc();
      }
      if (e.key === "Enter" || e.key === "Tab") {
        e.preventDefault();
        return this._accept();
      }
      if (e.key === "Escape") {
        e.preventDefault();
        return this._closeAc();
      }
    }
    if (e.key === "Tab") {
      // Indentation : insère deux espaces plutôt que de changer de focus.
      e.preventDefault();
      const s = this._ta.selectionStart;
      const en = this._ta.selectionEnd;
      this._ta.value = this._ta.value.slice(0, s) + "  " + this._ta.value.slice(en);
      this._ta.selectionStart = this._ta.selectionEnd = s + 2;
      this._render();
    }
  }
}

customElements.define("jslt-editor", JsltEditor);
export { JsltEditor };
