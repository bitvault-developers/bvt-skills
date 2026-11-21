#!/usr/bin/env node
// Builds languages.json: one entry per language with native name, English name, script, direction,
// plural categories, quality tier and fallback. Every part of an app (switcher, SEO, fonts, tiers) reads it.
//
//   node make_registry.mjs en,hi,ar,fr,ru --tiers en=A,fr=B --fallback mr=hi --out languages.json
//   node make_registry.mjs --from locales/            # every <code>.json / app_<code>.arb in a folder
//
// Run it in Node (full ICU data). Chrome ships trimmed locale data, so do not rebuild native names in the
// browser at runtime: keep the generated file. Names marked "check": true should be confirmed by a person.
import { readdirSync, writeFileSync } from "node:fs";

const RTL_SCRIPTS = new Set(["Arab", "Hebr", "Thaa", "Syrc", "Nkoo", "Adlm", "Rohg", "Mand", "Samr"]);
// Native names Intl often lacks or gets wrong (endonyms); these win over Intl.DisplayNames.
const ENDONYMS = {
  or: "ଓଡ଼ିଆ", as: "অসমীয়া", ne: "नेपाली", si: "සිංහල", sa: "संस्कृतम्", bho: "भोजपुरी", mai: "मैथिली",
  ks: "کٲشُر", ps: "پښتو", ckb: "کوردیی ناوەندی", ku: "Kurdî", ug: "ئۇيغۇرچە", yi: "ייִדיש", dv: "ދިވެހި",
  my: "မြန်မာ", km: "ខ្មែរ", lo: "ລາວ", bo: "བོད་སྐད་", ka: "ქართული", hy: "հայերեն", mn: "монгол",
  ha: "Hausa", yo: "Èdè Yorùbá", ig: "Asụsụ Igbo", zu: "isiZulu", xh: "isiXhosa", so: "Soomaali",
  be: "беларуская", is: "íslenska", eu: "euskara", gl: "galego", ast: "asturianu", oc: "occitan",
  cy: "Cymraeg", ga: "Gaeilge", mt: "Malti", lb: "Lëtzebuergesch", gsw: "Schwiizertüütsch", sq: "shqip",
  fil: "Filipino", qu: "Runasimi", haw: "ʻŌlelo Hawaiʻi", ht: "Kreyòl ayisyen", mi: "Te reo Māori",
};

function parseMap(s) {
  const out = {};
  for (const pair of (s || "").split(",").filter(Boolean)) {
    const [k, v] = pair.split("=");
    if (k && v) out[k.trim()] = v.trim();
  }
  return out;
}

function codesFrom(dir) {
  const codes = new Set();
  for (const f of readdirSync(dir)) {
    let m = f.match(/^app_([A-Za-z]{2,3}(?:[_-][A-Za-z0-9]+)*)\.arb$/) || f.match(/^([A-Za-z]{2,3}(?:-[A-Za-z0-9]+)*)\.json$/);
    if (m && m[1] !== "languages") codes.add(m[1].replace(/_/g, "-"));
  }
  return [...codes].sort();
}

function canonical(code) {
  try { return Intl.getCanonicalLocales(code)[0]; } catch { return null; }
}

function entry(code, tiers, fallbacks, base) {
  const loc = new Intl.Locale(code);
  const script = loc.script || loc.maximize().script || "Latn";
  const en = new Intl.DisplayNames(["en"], { type: "language" }).of(code);
  let native = ENDONYMS[code] || ENDONYMS[loc.language];
  let check = false;
  if (!native) {
    try { native = new Intl.DisplayNames([code], { type: "language" }).of(code); } catch { native = undefined; }
    // Intl returned the code itself or the English name: a person should supply the endonym
    if (!native || native === code || (native === en && !code.startsWith("en"))) check = true;
    if (!native || native === code) native = en;
  }
  let plurals = ["other"];
  try { plurals = new Intl.PluralRules(code).resolvedOptions().pluralCategories; } catch { check = true; }
  const order = ["zero", "one", "two", "few", "many", "other"];
  plurals = [...plurals].sort((a, b) => order.indexOf(a) - order.indexOf(b));
  const fallback = fallbacks[code] || (code.includes("-") ? loc.language : (code === base ? null : base));
  const e = {
    code, english: en, native: native.charAt(0).toLocaleUpperCase(code) + native.slice(1),
    script, dir: RTL_SCRIPTS.has(script) ? "rtl" : "ltr", plurals,
    tier: tiers[code] || (code === base ? "A" : "C"), fallback,
  };
  if (check) e.check = true;
  return e;
}

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const base = opt("--base") || "en";
let codes = opt("--from") ? codesFrom(opt("--from")) : (args[0] && !args[0].startsWith("--") ? args[0].split(",") : []);
if (!codes.length) {
  console.error("usage: node make_registry.mjs en,hi,ar [--tiers en=A,hi=B] [--fallback mr=hi] [--base en] [--out languages.json]\n" +
                "       node make_registry.mjs --from locales/ [--out languages.json]");
  process.exit(2);
}
if (!codes.includes(base)) codes.unshift(base);
const tiers = parseMap(opt("--tiers")), fallbacks = parseMap(opt("--fallback"));
const out = [], bad = [];
for (const raw of codes) {
  const c = canonical(raw.trim());
  if (!c) { bad.push(raw); continue; }
  if (!out.some((e) => e.code === c)) out.push(entry(c, tiers, fallbacks, base));
}
const json = "[\n" + out.map((e) => "  " + JSON.stringify(e)).join(",\n") + "\n]\n";  // one language per line
if (opt("--out")) writeFileSync(opt("--out"), json); else process.stdout.write(json);
const checks = out.filter((e) => e.check).map((e) => e.code);
console.error(`${out.length} languages${opt("--out") ? " -> " + opt("--out") : ""}` +
  (checks.length ? `; confirm native names for: ${checks.join(", ")}` : "") +
  (bad.length ? `; invalid tags skipped: ${bad.join(", ")}` : ""));
