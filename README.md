# Laravel LSP Booster

This Sublime Text plugin installs Laravel helper stubs for Intelephense and sets up recommended configuration.

## Installation

1. Unzip to your `Packages/` folder under the name `LaravelLSPBooster`.
2. Open the command palette and run: `Laravel: Setup LSP (Intelephense)`
3. Update your `LSP.sublime-settings` to include:
   - `"*.phpstub"` in `files.associations`
   - `~/.intelephense-stubs` in `includePaths`
