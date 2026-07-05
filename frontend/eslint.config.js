// Flat config (ESLint 9+) rather than the legacy .eslintrc — it's the format
// ESLint itself is standardizing on, and CI should exercise the same config
// shape you'll be maintaining long-term rather than a deprecated one.

import js from '@eslint/js'
import tseslint from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import globals from 'globals'

export default [
  { ignores: ['dist'] },
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2022,
      sourceType: 'module',
      // Without this, ESLint assumes a Node-only environment and flags
      // browser globals like `fetch` and `document` as undefined.
      globals: globals.browser,
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...tseslint.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      // Warn (not error) so fast-refresh quirks don't block a PR outright,
      // but still show up in review.
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
]
