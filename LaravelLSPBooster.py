import sublime
import sublime_plugin
import os
import shutil
import json

class SetupLaravelLspCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # Copy stub file
        stub_src = os.path.join(sublime.packages_path(), 'LaravelLSPBooster', 'laravel_helpers.phpstub')
        stub_dst = os.path.expanduser('~/.intelephense-stubs/laravel_helpers.phpstub')
        os.makedirs(os.path.dirname(stub_dst), exist_ok=True)
        shutil.copyfile(stub_src, stub_dst)

        # Load LSP settings
        settings = sublime.load_settings("LSP.sublime-settings")
        clients = settings.get("clients", {})
        intelephense = clients.get("intelephense", {})

        # Add includePaths
        init_opts = intelephense.get("initializationOptions", {})
        env = init_opts.get("environment", {})
        include_paths = env.get("includePaths", [])
        stub_path = os.path.expanduser("~/.intelephense-stubs")
        if stub_path not in include_paths:
            include_paths.append(stub_path)
        env["includePaths"] = include_paths
        init_opts["environment"] = env
        intelephense["initializationOptions"] = init_opts

        # Add *.phpstub association
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

        # Save changes
        clients["intelephense"] = intelephense
        settings.set("clients", clients)
        sublime.save_settings("LSP.sublime-settings")

        sublime.message_dialog("Laravel LSP config applied! Restart LSP for changes to take effect.")
