---
name: "adding-language-switching"
description: "Adds a full multilingual system and language switcher to any website, web app, mobile app, desktop app, WordPress, Flutter or FlutterFlow project. Use when building any digital product, or when languages, translation, multilingual, i18n, localization, locale, RTL or a language switcher come up."
---

# Adding language switching

Every product built with this skill ships with a language switcher and is ready for hundreds of languages, even if it launches in one.

Related skills in this pack:
- `translating-app-languages`: fills the locale files with translations (machine, Claude, or human) and adds live translation for user content.
- `checking-translation-quality`: release gate, QA script, review, legal checks.

## The idea in simple words

There are two layers:

1. **Saved strings (always).** Every visible text lives in a language file (`en.json`, `hi.json`, ...), never inside the code. The app shows the file for the chosen language. Fast, offline, searchable by Google, cheap.
2. **Live translation (only when needed).** Text that changes all the time (chat, reviews, comments) or languages you did not prepare are translated on the fly through a translation service, with a cache.

Default = **hybrid**: layer 1 for all UI and public pages, layer 2 for user content plus an optional "Translate this page (beta)" fallback.

Never use the old free Google Website Translator embed (`translate_a/element.js`, `google.translate.TranslateElement`). Google ended support for it. Replace it if you find it.

## Workflow checklist

Copy this list into your task list and tick it off:

1. Detect the platform (table below) and open its recipe.
2. Pick languages. If the user names none, ship the base language plus the languages they mention; if they ask for "all" or "maximum", follow the coverage strategy in `translating-app-languages`.
3. Externalize every visible string into key files (rules below).
4. Wire the platform library from the recipe.
5. Add the language switcher (rules + component below).
6. Make layout work for RTL and non-Latin scripts; format numbers/dates with Intl.
7. Public websites: set up per-language URLs, hreflang and sitemaps.
8. Fill translations with `translating-app-languages`.
9. Run the release gate in `checking-translation-quality`.

## Decision rules

1. **Saved strings first.** No hard-coded UI text, ever. Even a one-language MVP gets locale files and a switcher-ready structure.
2. **Library by platform:** Next.js → next-intl. Other React and React Native → i18next. Vue/Nuxt → vue-i18n / @nuxtjs/i18n. Svelte → Paraglide JS. Angular → Transloco (live switching). Flutter → gen-l10n + ARB. FlutterFlow → built-in Languages. Android → string resources + per-app language. iOS → String Catalogs. Electron/Tauri → i18next. WordPress → see recipe.
3. **Fallback chain for every lookup:** regional → base language → closest related language → default. Example: `pt-PT → pt → en`, `gsw → de → en`. Never show blank text or raw keys.
4. **Public pages are server-rendered per language** with their own URL (`/fr/...`). Client-only translation is invisible to Google and AI search.
5. **Live translation only for user content or unshipped languages**, always through your backend with a cache or on-device APIs. Never put a translation API key in client code.
6. **Detect, suggest, never force.** No automatic redirects based on IP.

## Platform detection

| Look for | Platform | Recipe |
|---|---|---|
| `next.config.*` + `app/` | Next.js | Next.js |
| `package.json` with `react`, no Next | React SPA | React |
| `app.json` / `expo` or `react-native` in package.json | React Native / Expo | React Native |
| `nuxt.config.*` / `vue` | Vue / Nuxt | Vue, Svelte, Angular |
| `svelte.config.*` | SvelteKit | Vue, Svelte, Angular |
| `angular.json` | Angular | Vue, Svelte, Angular |
| `pubspec.yaml` | Flutter | Flutter |
| FlutterFlow project / user says FlutterFlow | FlutterFlow | FlutterFlow |
| `build.gradle(.kts)` + `AndroidManifest.xml` | Android native | Android |
| `*.xcodeproj` / `Package.swift` | iOS native | iOS |
| `electron` / `src-tauri/` | Desktop | Desktop |
| `wp-config.php`, `wp-content/` | WordPress | WordPress |
| plain `.html` files | Static site | Plain HTML/JS |

## Key file rules

- **Keys** describe place and purpose: `checkout.payButton.label`, `errors.network.offline`. Not the English sentence (except gettext/PO projects).
- **Whole sentences only.** Never glue fragments (`"You have " + n + " coins"`). Use placeholders: `"You have {count} coins"`.
- **Plurals:** use the library's plural system (ICU `{count, plural, one {# coin} other {# coins}}` or i18next `_one`/`_other` keys). Languages need different forms: Arabic has 6, Chinese 1. `new Intl.PluralRules('ar').resolvedOptions().pluralCategories` lists them.
- **Context for translators:** add a description per key where the meaning is unclear (ARB `@key.description`, a `_context` comment file, or TMS notes). "Save" (button) and "Save" (discount) are different words in many languages.
- **Language tags:** BCP 47 (`pt-BR`, `zh-Hans`, `zh-Hant`, `sr-Latn`, `es-419`). Flutter/Android file names use `_` or `b+` forms; map them, don't invent tags.
- **Lazy-load:** ship only the active language file. 200 languages must not bloat the bundle.
- **Do not translate:** brand names, code, URLs, placeholders. Keep a glossary (see `translating-app-languages`).

## Language registry

Keep one `languages.json` that every part of the app reads (switcher, SEO, fonts, tiers):

```json
[{ "code": "ar", "english": "Arabic", "native": "العربية", "script": "Arab", "dir": "rtl", "tier": "B", "fallback": "en" }]
```

Generate the first version with Intl, then store the native names in the registry. Don't rely on `Intl.DisplayNames` for native names at runtime: Chrome ships trimmed locale data, and in testing (Nov 2026) it returned the English name or the bare code for about 40 languages, including Odia, Assamese, Nepali, Sinhala, Burmese, Khmer, Lao, Georgian, Armenian, Basque, Welsh, Irish and Maltese. Node has fuller data, so generate there and keep the result:

```js
const RTL_SCRIPTS = new Set(['Arab', 'Hebr', 'Thaa', 'Syrc', 'Nkoo', 'Adlm', 'Rohg']);
const info = (code) => {
  const script = new Intl.Locale(code).maximize().script;
  return {
    code,
    english: new Intl.DisplayNames(['en'], { type: 'language' }).of(code),
    native: new Intl.DisplayNames([code], { type: 'language' }).of(code),
    script,
    dir: RTL_SCRIPTS.has(script) ? 'rtl' : 'ltr',
  };
};
```

Native names Chrome was missing, ready to paste into the registry:

```js
const ENDONYMS = { or: 'ଓଡ଼ିଆ', as: 'অসমীয়া', ne: 'नेपाली', si: 'සිංහල', sa: 'संस्कृतम्', bho: 'भोजपुरी', mai: 'मैथिली',
  ks: 'کٲشُر', ps: 'پښتو', ckb: 'کوردیی ناوەندی', ku: 'Kurdî', ug: 'ئۇيغۇرچە', yi: 'ייִדיש', dv: 'ދިވެހި',
  my: 'မြန်မာ', km: 'ខ្មែរ', lo: 'ລາວ', bo: 'བོད་སྐད་', ka: 'ქართული', hy: 'հայերեն', mn: 'монгол',
  ha: 'Hausa', yo: 'Èdè Yorùbá', ig: 'Asụsụ Igbo', zu: 'isiZulu', xh: 'isiXhosa', so: 'Soomaali',
  be: 'беларуская', is: 'íslenska', eu: 'euskara', gl: 'galego', ast: 'asturianu', oc: 'occitan',
  cy: 'Cymraeg', ga: 'Gaeilge', mt: 'Malti', lb: 'Lëtzebuergesch', gsw: 'Schwiizertüütsch', sq: 'shqip',
  fil: 'Filipino', qu: 'Runasimi', haw: 'ʻŌlelo Hawaiʻi', ht: 'Kreyòl ayisyen', mi: 'Te reo Māori' };
```

The language names inside sentences ("Marathi isn't translated yet") also come from `Intl.DisplayNames` in the UI language. Write those message templates so any name fits (for example Korean `{fallback}(으)로`, Indonesian `bahasa {fallback}`, Arabic `باللغة {fallback}`).

## Recipes

### Plain HTML/JS (no build step)

Files: `/locales/en.json`, `/locales/hi.json` ... Mark elements with `data-i18n="nav.home"`.

```html
<script type="module">
const SUPPORTED = ['en', 'hi', 'ar', 'fr'], DEFAULT = 'en';
const RTL_SCRIPTS = new Set(['Arab', 'Hebr', 'Thaa', 'Syrc', 'Nkoo', 'Adlm', 'Rohg']);
const match = (tag) => SUPPORTED.find(s => s === tag)
  || SUPPORTED.find(s => s === tag.split('-')[0])
  || SUPPORTED.find(s => s.split('-')[0] === tag.split('-')[0]);
function pick() {
  const url = new URLSearchParams(location.search).get('lang');
  for (const t of [url, localStorage.getItem('lang'), ...navigator.languages].filter(Boolean)) {
    const m = match(t); if (m) return m;
  }
  return DEFAULT;
}
const load = (l) => fetch(`/locales/${l}.json`).then(r => r.json());
const dig = (o, k) => k.split('.').reduce((x, p) => x?.[p], o);
export async function setLang(lang) {
  const [msgs, base] = await Promise.all([load(lang), load(DEFAULT)]);
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = dig(msgs, el.dataset.i18n) ?? dig(base, el.dataset.i18n) ?? '';
  });
  const script = new Intl.Locale(lang).maximize().script;
  document.documentElement.lang = lang;
  document.documentElement.dir = RTL_SCRIPTS.has(script) ? 'rtl' : 'ltr';
  localStorage.setItem('lang', lang);
}
setLang(pick());
</script>
```

For SEO, pre-render one folder per language (`/fr/index.html`) instead of switching only in the browser.

### React (Vite / SPA): react-i18next

`npm i i18next react-i18next i18next-browser-languagedetector i18next-resources-to-backend`

```ts
// src/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import resourcesToBackend from 'i18next-resources-to-backend';

i18n
  .use(resourcesToBackend((lng: string) => import(`./locales/${lng}.json`)))
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    supportedLngs: ['en', 'hi', 'ar', 'pt', 'pt-BR'],
    nonExplicitSupportedLngs: true,
    fallbackLng: { 'pt-PT': ['pt', 'en'], default: ['en'] },
    detection: { order: ['querystring', 'localStorage', 'navigator'], caches: ['localStorage'] },
    interpolation: { escapeValue: false },
  });
i18n.on('languageChanged', (l) => {
  document.documentElement.lang = l;
  document.documentElement.dir = i18n.dir(l);
});
export default i18n;
```

Use `const { t } = useTranslation(); t('nav.home')`, plurals `t('items', { count })` with `items_one` / `items_other` keys. Change language with `i18n.changeLanguage('hi')`.

### Next.js App Router: next-intl

Structure: `messages/en.json`, `src/i18n/routing.ts`, `src/i18n/request.ts`, `app/[locale]/...`, plus `middleware.ts` (named `proxy.ts` on Next.js 16+). Check the installed next-intl version's docs if an API name differs.

```ts
// src/i18n/routing.ts
import { defineRouting } from 'next-intl/routing';
export const routing = defineRouting({ locales: ['en', 'hi', 'ar'], defaultLocale: 'en' });

// src/i18n/request.ts
import { getRequestConfig } from 'next-intl/server';
import { hasLocale } from 'next-intl';
import { routing } from './routing';
const deepMerge = (a: any, b: any): any => Object.fromEntries(
  [...new Set([...Object.keys(a), ...Object.keys(b)])].map(k => [k,
    typeof a[k] === 'object' && typeof b[k] === 'object' ? deepMerge(a[k], b[k]) : b[k] ?? a[k]]));
export default getRequestConfig(async ({ requestLocale }) => {
  const req = await requestLocale;
  const locale = hasLocale(routing.locales, req) ? req : routing.defaultLocale;
  const base = (await import(`../../messages/${routing.defaultLocale}.json`)).default;
  const own = (await import(`../../messages/${locale}.json`)).default;
  return { locale, messages: deepMerge(base, own) }; // base fills missing keys
});

// middleware.ts / proxy.ts (inside src/ when the project uses src/, then import from './i18n/routing')
import createMiddleware from 'next-intl/middleware';
import { routing } from './src/i18n/routing';
export default createMiddleware(routing);
export const config = { matcher: '/((?!api|_next|_vercel|.*\\..*).*)' };
```

- Wrap `next.config` with `createNextIntlPlugin()`.
- In `app/[locale]/layout.tsx`: validate the locale, call `setRequestLocale(locale)`, render `<html lang={locale} dir={dir}>`, wrap children in `<NextIntlClientProvider>`, and export `generateStaticParams` returning every locale.
- Server components: `getTranslations('nav')`; client components: `useTranslations('nav')`.
- Switcher: use next-intl's `Link`/`useRouter` from `createNavigation(routing)` so the URL prefix changes with the language.
- hreflang: return `alternates: { canonical, languages: { en: '/en', hi: '/hi', 'x-default': '/en' } }` from `generateMetadata`.

### React Native / Expo

`npx expo install expo-localization @react-native-async-storage/async-storage` + `npm i i18next react-i18next`.
- Initial language: saved choice from AsyncStorage, else `getLocales()[0].languageTag`, matched to supported list.
- Metro cannot do `import(\`./locales/${lng}.json\`)`. Bundle with a static map (`{ en: require('./locales/en.json'), ... }`) or download language files from a CDN and cache them.
- RTL: `I18nManager.allowRTL(true); I18nManager.forceRTL(isRtl)` then reload (`Updates.reloadAsync()`). Use `marginStart`/`paddingEnd`, not left/right.

### Vue, Svelte, Angular

- **Nuxt:** `@nuxtjs/i18n` with `strategy: 'prefix_except_default'`, `lazy: true`, `langDir: 'locales'`, `locales: [{ code: 'ar', language: 'ar', file: 'ar.json', dir: 'rtl' }]`. `useLocaleHead()` outputs `lang`, `dir` and hreflang.
- **Vue SPA:** `createI18n({ legacy: false, locale, fallbackLocale: 'en', messages })`, load message files on demand.
- **SvelteKit:** Paraglide JS (inlang). Messages in `messages/en.json`, compiled to tree-shaken functions (`m.nav_home()`), supports translated URLs.
- **Angular:** Transloco for live switching (`provideTransloco`, `TranslocoHttpLoader`, `translate` pipe). `@angular/localize` builds one app per language and needs a rebuild per change, so use it only for static per-language deploys.

### Flutter: gen-l10n + ARB

```yaml
# pubspec.yaml
dependencies:
  flutter_localizations: { sdk: flutter }
  intl: any
flutter:
  generate: true
```

```yaml
# l10n.yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

`lib/l10n/app_en.arb`:

```json
{
  "@@locale": "en",
  "coinCount": "{count, plural, =0{No coins} =1{1 coin} other{{count} coins}}",
  "@coinCount": { "description": "Wallet balance label", "placeholders": { "count": { "type": "int" } } }
}
```

Run `flutter gen-l10n` (it prints the import path for `AppLocalizations`). Then:

```dart
MaterialApp(
  locale: appLocale.value,               // null = follow the device
  supportedLocales: AppLocalizations.supportedLocales,
  localizationsDelegates: [
    ...AppLocalizations.localizationsDelegates,
    const FallbackMaterialDelegate(),     // for languages Flutter itself doesn't translate
  ],
);
// in widgets: AppLocalizations.of(context)!.coinCount(3)
```

Flutter's built-in Material/Cupertino strings cover a fixed list of languages. For any other language, add a fallback so the app doesn't crash:

```dart
class FallbackMaterialDelegate extends LocalizationsDelegate<MaterialLocalizations> {
  const FallbackMaterialDelegate();
  @override
  bool isSupported(Locale l) => !GlobalMaterialLocalizations.delegate.isSupported(l);
  @override
  Future<MaterialLocalizations> load(Locale l) =>
      GlobalMaterialLocalizations.delegate.load(const Locale('en'));
  @override
  bool shouldReload(_) => false;
}
```

Do the same for `CupertinoLocalizations` if Cupertino widgets are used. Keep the chosen locale in a `ValueNotifier<Locale?>` persisted with `shared_preferences`. RTL comes from the locale automatically; use `EdgeInsetsDirectional`, `AlignmentDirectional`, `PositionedDirectional`.

### FlutterFlow

1. Settings & Integrations → Languages: add languages, set the primary language **first**. Changing the primary language later clears existing translations.
2. Use the auto-translate ("Translate All", Google Translate) for a first pass, then edit, and mark edited strings as fixed so later runs don't overwrite them.
3. Add a switcher with the **Set App Language** action on a dropdown/list (follow the switcher rules below).
4. Export translations to CSV for human review, then import back.
5. Test regional variants (e.g. `pt_PT`): users have reported blank text instead of fallback. Prefer base languages unless a variant is truly needed.
6. User content: Cloud Function calling a translation API with a database cache (see `translating-app-languages`).

### Android native

- `res/values/strings.xml`, `res/values-hi/strings.xml`, script variants as `res/values-b+sr+Latn/`.
- Compose: `stringResource(R.string.x)`, plurals with `pluralStringResource`.
- Per-app language: `AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags("hi"))`. Enable `androidResources { generateLocaleConfig = true }` and add `res/resources.properties` with `unqualifiedResLocale=en-US` so Android settings list your languages.
- Manifest `android:supportsRtl="true"`; use `start`/`end`, never `left`/`right`.

### iOS native

- Use a String Catalog (`Localizable.xcstrings`); add languages under Project → Info → Localizations.
- SwiftUI `Text("wallet.title")` looks up keys automatically; plurals via "Vary by Plural" in the catalog.
- iOS shows a per-app language setting automatically when the app has more than one localization. For an in-app switcher, deep-link to it with `UIApplication.openSettingsURLString`.

### Desktop: Electron / Tauri

- Electron: i18next in the renderer **and** main process (menus, dialogs, notifications). Initial language from `app.getPreferredSystemLanguages()` / `app.getLocale()`, persisted in a JSON file under `app.getPath('userData')`. Rebuild the menu after a language change.
- Tauri: i18next in the web layer; read the OS locale with the OS plugin's `locale()`; use Rust `fluent` only if the backend shows text itself.

### WordPress

| Need | Use |
|---|---|
| Free, translations stored in your own database, visual editing | TranslatePress |
| Free, separate linked posts per language, clean URLs | Polylang |
| Large site or WooCommerce, full control | WPML |
| Most languages with least work, OK with a subscription | Weglot or GTranslate (paid proxy) |
| Theme/plugin interface strings (.po/.mo) | Loco Translate |

Steps: install → set default + extra languages → choose **subdirectory** URLs (`/fr/`) → add the switcher to the menu with flags turned **off** and native names on → translate slugs and SEO titles → confirm the plugin outputs hreflang. The free GTranslate widget is client-side only and not indexable. Hosted proxies keep your translations on their servers: stop paying and they stop working.

### Backend, email, push, headless CMS

- Store `locale` on the user profile; it beats `Accept-Language` for emails and push.
- Render emails/notifications server-side with the same key files (i18next on Node, gettext/Babel on Python, Laravel lang files on PHP).
- API errors: return a stable error `code`; the client translates it.
- Headless CMS (Strapi, Sanity, Contentful): field-level localization; a webhook sends new content to machine translation and saves it as a **draft** for review.

## Language switcher rules

- **Native names (endonyms):** "Deutsch", "العربية", "日本語", with the English name small next to them for search.
- **No flags.** Flags are countries, not languages.
- **Search box when there are more than 10 languages**, matching native name, English name and code. Put "Suggested" (detected) languages on top.
- **Placement:** header top-right (top-left in RTL), again in the footer, and in Settings in apps. Show a globe/language icon **plus** the current language name.
- **On change:** update `<html lang>` and `dir` (or the platform equivalent), save the choice (localStorage/cookie + user profile when logged in), keep the user on the same page.
- **Order of signals:** the URL decides what a page shows; the saved choice decides where `/` sends a visitor; then device languages; then the default. IP location is a weak hint only.
- **Quality badge:** show "beta" next to machine-only (Tier D) languages.
- **Accessibility:** each option has its own `lang` attribute; keyboard reachable; the switcher's own labels come from translation keys too.

React example (adapt for other frameworks):

```tsx
import { useMemo, useState } from 'react';

const label = (code: string, inLang: string) => {
  try { return new Intl.DisplayNames([inLang], { type: 'language' }).of(code) ?? code; }
  catch { return code; }
};

export function LanguageSwitcher({ languages, current, onChange, t }: {
  languages: { code: string; native?: string; tier?: string }[];
  current: string; onChange: (code: string) => void; t: (k: string) => string;
}) {
  const [q, setQ] = useState('');
  const items = useMemo(() => languages.map(l => ({
    ...l, native: l.native ?? label(l.code, l.code), english: label(l.code, 'en'),
  })), [languages]);
  const shown = items.filter(l =>
    `${l.native} ${l.english} ${l.code}`.toLowerCase().includes(q.trim().toLowerCase()));
  return (
    <div>
      {items.length > 10 && (
        <input type="search" value={q} onChange={e => setQ(e.target.value)}
          placeholder={t('language.search')} aria-label={t('language.search')} />
      )}
      <ul role="listbox" aria-label={t('language.choose')}>
        {shown.map(l => (
          <li key={l.code} role="option" aria-selected={l.code === current} tabIndex={0} lang={l.code}
            onClick={() => onChange(l.code)}
            onKeyDown={e => (e.key === 'Enter' || e.key === ' ') && onChange(l.code)}>
            {l.native} <small lang="en">{l.english}</small>
            {l.tier === 'D' && <span> beta</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## RTL, scripts, fonts, formatting

- **RTL** (Arabic, Hebrew, Persian, Urdu, Pashto, Sindhi, Uyghur, Yiddish, Dhivehi, Kurdish Sorani): set `dir="rtl"`; use CSS logical properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`); mirror directional icons (arrows, back), not logos, media controls or checkmarks; wrap user names and numbers in `<bdi>` or `unicode-bidi: isolate`.
- **Complex scripts** (Devanagari, Bengali, Tamil, Thai, Khmer, Myanmar, Ethiopic): rely on the platform text engine; never split strings by character. Thai, Khmer and Lao have no spaces, so use `Intl.Segmenter`/ICU for line breaks. CJK needs taller line height.
- **Fonts:** Noto families as fallback stack; load per script with `unicode-range` so Latin users don't download CJK fonts.
- **Text grows 30–40%** (more for short labels): no fixed-width buttons, allow wrapping, test with the pseudo-locale.
- **Formatting:** never hand-format. Use `Intl.NumberFormat`, `DateTimeFormat`, `RelativeTimeFormat`, `PluralRules`, `ListFormat`, `DisplayNames` (or Flutter `intl`, Android/iOS formatters). Currency comes from the user's account/region, not the UI language. Support other calendars if the market needs them.
- **Normalize** text to NFC before comparing, hashing or caching.

## SEO for public websites

- One URL per language, preferably subdirectories: `example.com/fr/`. Query params work but are weaker; cookie-only switching is invisible to crawlers.
- Every page lists all its language versions plus `x-default` with `<link rel="alternate" hreflang="..." href="...">`, and every version links back (reciprocal).
- Translate slugs, titles, meta descriptions and Open Graph tags; put all language URLs in the sitemap (`xhtml:link` alternates).
- Server-render translated HTML; client-only translations are mostly not indexed by search engines or AI crawlers.
- Machine translation is allowed when useful, but mass-producing low-value unreviewed pages risks Google's scaled-content policy. Review the top languages.
- Showing raw Google Translate output on indexable pages requires machine-translation markup and "powered by Google Translate" attribution.

## Done when

- No hard-coded user-facing strings remain (grep check in `checking-translation-quality`).
- Switcher works, is saved, updates `lang`/`dir`, and follows the rules above.
- Every language falls back cleanly; nothing blank or showing raw keys.
- RTL and pseudo-locale screenshots look right.
- Public sites: hreflang, x-default, sitemap and translated slugs in place.
- The release gate in `checking-translation-quality` passes.