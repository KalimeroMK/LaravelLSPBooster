# Laravel LSP Booster

This Sublime Text plugin installs Laravel helper stubs for Intelephense and sets up recommended configuration.

## Features

- ✅ Laravel `.phpstub` helpers for Intelephense
- ✅ Auto-update `LSP.sublime-settings` for Laravel projects
- ✅ Go to Blade View: supports `view('...')` and `Module::view(...)`
- ✅ Blade autocomplete based on view paths
- ✅ Blade snippets: `@auth`, `@can`, `@error`, `@foreach`, `@if`, `@isset`, `@session`
- ✅ Go to `Controller@method` from named `route(...)`

## Installation

### Option A: Package Control

1. Open Command Palette → `Package Control: Add Repository`
2. Paste:
   ```
   https://github.com/KalimeroMK/LaravelLSPBooster
   ```
3. Then run `Package Control: Install Package` → select `LaravelLSPBooster`

### Option B: Manual Install

1. Unzip to your `Packages/` folder as `LaravelLSPBooster`
2. Open Command Palette → run: `Laravel: Setup LSP (Intelephense)`

## LSP Configuration

Ensure your `LSP.sublime-settings` includes:

```json
"files": {
  "associations": ["*.php", "*.blade.php", "*.phpstub"]
},
"initializationOptions": {
  "storagePath": "${home}/.intelephense",
  "licenseKey": "YOUR_LICENSE_KEY",
  "environment": {
    "includePaths": [
      "${home}/.intelephense-stubs",
      "Modules",
      "vendor/laravel/framework/src",
      "vendor/illuminate"
    ]
  }
}
```

## Commands

- `Laravel: Setup LSP (Intelephense)` – One-time config
- `Laravel: Go to Blade View` – Opens Blade file from `view(...)`
- `Laravel: Go to Controller from route(...)` – Resolves `route('users.index')` to Controller@method

## Snippets

Trigger in `.blade.php` files:

- `@auth` / `@can` / `@error` / `@foreach`
- `@if` / `@isset` / `@session`

## Maintained by

Zoran Bogoevski✨
