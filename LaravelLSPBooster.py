import sublime
import sublime_plugin
import os
import shutil
import re

class SetupLaravelLspCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # Copy stub file
        stub_src = os.path.join(sublime.packages_path(), 'LaravelLSPBooster', 'laravel_helpers.phpstub')
        stub_dst = os.path.expanduser('~/.intelephense-stubs/laravel_helpers.phpstub')
        os.makedirs(os.path.dirname(stub_dst), exist_ok=True)
        shutil.copyfile(stub_src, stub_dst)

        # Update LSP settings
        settings = sublime.load_settings("LSP.sublime-settings")
        clients = settings.get("clients", {})
        intelephense = clients.get("intelephense", {})

        # includePaths
        init_opts = intelephense.get("initializationOptions", {})
        env = init_opts.get("environment", {})
        include_paths = env.get("includePaths", [])
        stub_path = os.path.expanduser("~/.intelephense-stubs")
        if stub_path not in include_paths:
            include_paths.append(stub_path)
        env["includePaths"] = include_paths
        init_opts["environment"] = env
        intelephense["initializationOptions"] = init_opts

        # *.phpstub association
        settings_block = intelephense.get("settings", {})
        intelephense_core = settings_block.get("intelephense", {})
        files_block = intelephense_core.get("files", {})
        associations = files_block.get("associations", [])
        if "*.phpstub" not in associations:
            associations.append("*.phpstub")
        files_block["associations"] = associations
        intelephense_core["files"] = files_block
        settings_block["intelephense"] = intelephense_core
        intelephense["settings"] = settings_block

        # Save all changes
        clients["intelephense"] = intelephense
        settings.set("clients", clients)
        sublime.save_settings("LSP.sublime-settings")

        sublime.message_dialog("Laravel LSP configured. Restart LSP for changes to take effect.")

class GoToViewDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()[0]
        line = self.view.substr(self.view.line(sel))
        match = re.search(r"view\(\s*['\"]([\w\.:-]+)['\"]", line)
        if not match:
            sublime.status_message("Could not extract view() name.")
            return

        view_name = match.group(1)
        folders = self.view.window().folders()
        if not folders:
            sublime.status_message("No project folder detected.")
            return

        root = folders[0]
        blade_file = None

        if "::" in view_name:
            module, view_path = view_name.split("::", 1)
            blade_path = os.path.join(root, "Modules", module, "Resources", "views", view_path.replace('.', '/') + ".blade.php")
        else:
            blade_path = os.path.join(root, "resources", "views", view_name.replace('.', '/') + ".blade.php")

        if os.path.exists(blade_path):
            self.view.window().open_file(blade_path)
        else:
            sublime.status_message("Blade view not found: " + blade_path)
