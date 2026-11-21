# Platform recipes

Setup for each platform, used by step 1 and step 4 of the BVT Multi Language workflow. Every recipe follows the decision rules in `SKILL.md`: strings in language files, a fallback chain, lazy-loaded languages, and `lang`/`dir` updated on change.


## Plain HTML/JS (no build step)

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

## React (Vite / SPA): react-i18next

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

## Next.js App Router: next-intl

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

## React Native / Expo

`npx expo install expo-localization @react-native-async-storage/async-storage` + `npm i i18next react-i18next`.
- Initial language: saved choice from AsyncStorage, else `getLocales()[0].languageTag`, matched to supported list.
- Metro cannot do `import(\`./locales/${lng}.json\`)`. Bundle with a static map (`{ en: require('./locales/en.json'), ... }`) or download language files from a CDN and cache them.
- RTL: `I18nManager.allowRTL(true); I18nManager.forceRTL(isRtl)` then reload (`Updates.reloadAsync()`). Use `marginStart`/`paddingEnd`, not left/right.

## Vue, Svelte, Angular

- **Nuxt:** `@nuxtjs/i18n` with `strategy: 'prefix_except_default'`, `lazy: true`, `langDir: 'locales'`, `locales: [{ code: 'ar', language: 'ar', file: 'ar.json', dir: 'rtl' }]`. `useLocaleHead()` outputs `lang`, `dir` and hreflang.
- **Vue SPA:** `createI18n({ legacy: false, locale, fallbackLocale: 'en', messages })`, load message files on demand.
- **SvelteKit:** Paraglide JS (inlang). Messages in `messages/en.json`, compiled to tree-shaken functions (`m.nav_home()`), supports translated URLs.
- **Angular:** Transloco for live switching (`provideTransloco`, `TranslocoHttpLoader`, `translate` pipe). `@angular/localize` builds one app per language and needs a rebuild per change, so use it only for static per-language deploys.

## Flutter: gen-l10n + ARB

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

## FlutterFlow

1. Settings & Integrations → Languages: add languages, set the primary language **first**. Changing the primary language later clears existing translations.
2. Use the auto-translate ("Translate All", Google Translate) for a first pass, then edit, and mark edited strings as fixed so later runs don't overwrite them.
3. Add a switcher with the **Set App Language** action on a dropdown/list (follow the switcher rules below).
4. Export translations to CSV for human review, then import back.
5. Test regional variants (e.g. `pt_PT`): users have reported blank text instead of fallback. Prefer base languages unless a variant is truly needed.
6. User content: Cloud Function calling a translation API with a database cache (see `translating.md`, Live translation for user content).

## Android native

- `res/values/strings.xml`, `res/values-hi/strings.xml`, script variants as `res/values-b+sr+Latn/`.
- Compose: `stringResource(R.string.x)`, plurals with `pluralStringResource`.
- Per-app language: `AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags("hi"))`. Enable `androidResources { generateLocaleConfig = true }` and add `res/resources.properties` with `unqualifiedResLocale=en-US` so Android settings list your languages.
- Manifest `android:supportsRtl="true"`; use `start`/`end`, never `left`/`right`.

## iOS native

- Use a String Catalog (`Localizable.xcstrings`); add languages under Project → Info → Localizations.
- SwiftUI `Text("wallet.title")` looks up keys automatically; plurals via "Vary by Plural" in the catalog.
- iOS shows a per-app language setting automatically when the app has more than one localization. For an in-app switcher, deep-link to it with `UIApplication.openSettingsURLString`.

## Desktop: Electron / Tauri

- Electron: i18next in the renderer **and** main process (menus, dialogs, notifications). Initial language from `app.getPreferredSystemLanguages()` / `app.getLocale()`, persisted in a JSON file under `app.getPath('userData')`. Rebuild the menu after a language change.
- Tauri: i18next in the web layer; read the OS locale with the OS plugin's `locale()`; use Rust `fluent` only if the backend shows text itself.

## WordPress

| Need | Use |
|---|---|
| Free, translations stored in your own database, visual editing | TranslatePress |
| Free, separate linked posts per language, clean URLs | Polylang |
| Large site or WooCommerce, full control | WPML |
| Most languages with least work, OK with a subscription | Weglot or GTranslate (paid proxy) |
| Theme/plugin interface strings (.po/.mo) | Loco Translate |

Steps: install → set default + extra languages → choose **subdirectory** URLs (`/fr/`) → add the switcher to the menu with flags turned **off** and native names on → translate slugs and SEO titles → confirm the plugin outputs hreflang. The free GTranslate widget is client-side only and not indexable. Hosted proxies keep your translations on their servers: stop paying and they stop working.

## Backend, email, push, headless CMS

- Store `locale` on the user profile; it beats `Accept-Language` for emails and push.
- Render emails/notifications server-side with the same key files (i18next on Node, gettext/Babel on Python, Laravel lang files on PHP).
- API errors: return a stable error `code`; the client translates it.
- Headless CMS (Strapi, Sanity, Contentful): field-level localization; a webhook sends new content to machine translation and saves it as a **draft** for review.

## Language switcher component

React example (adapt it for other frameworks). It reads `languages.json` from `scripts/make_registry.mjs`, puts suggested (device) languages on top, sorts the rest with `Intl.Collator`, and searches native name, English name and code without caring about accents or case.

```tsx
import { useMemo, useState } from 'react';

type Lang = { code: string; native: string; english: string; tier?: string; dir?: 'ltr' | 'rtl' };
const fold = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();

export function LanguageSwitcher({ languages, current, onChange, t, uiLang }: {
  languages: Lang[]; current: string; onChange: (code: string) => void;
  t: (k: string) => string; uiLang: string;
}) {
  const [q, setQ] = useState('');
  const suggested = useMemo(() => {
    const device = (navigator.languages || []).map(l => l.toLowerCase());
    return new Set(languages.filter(l => device.some(d => d === l.code.toLowerCase() || d.split('-')[0] === l.code.toLowerCase()))
      .map(l => l.code));
  }, [languages]);
  const collator = useMemo(() => new Intl.Collator(uiLang), [uiLang]);
  const shown = useMemo(() => {
    const f = fold(q.trim());
    return languages
      .filter(l => !f || fold(`${l.native} ${l.english} ${l.code}`).includes(f))
      .sort((a, b) => Number(suggested.has(b.code)) - Number(suggested.has(a.code)) || collator.compare(a.native, b.native));
  }, [languages, q, suggested, collator]);

  return (
    <div>
      {languages.length > 10 && (
        <input type="search" value={q} onChange={e => setQ(e.target.value)}
          placeholder={t('language.search')} aria-label={t('language.search')} />
      )}
      <ul role="listbox" aria-label={t('language.choose')}>
        {shown.map(l => (
          <li key={l.code} role="option" aria-selected={l.code === current} tabIndex={0}
            lang={l.code} dir={l.dir}
            onClick={() => onChange(l.code)}
            onKeyDown={e => (e.key === 'Enter' || e.key === ' ') && onChange(l.code)}>
            {l.native} <small lang="en" dir="ltr">{l.english}</small>
            {l.tier === 'D' && <span> {t('language.beta')}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

On change: set `document.documentElement.lang` and `dir`, save the choice (cookie or localStorage, and the user profile when signed in), load that language file, and stay on the same page (swap the `/<lang>/` prefix in the URL on public sites).
