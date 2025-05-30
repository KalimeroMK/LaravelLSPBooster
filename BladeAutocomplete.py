import sublime
import sublime_plugin
import os
import re

class LaravelBladeViewCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger for PHP files containing "view("
        if not view.match_selector(locations[0], "source.php"):
            return None

        # Get current line and check for view(
        line = view.substr(view.line(locations[0]))
        if "view(" not in line:
            return None

        # Get project root
        folders = view.window().folders()
        if not folders:
            return None
        root = folders[0]

        completions = []

        # Search resources/views
        res_path = os.path.join(root, "resources", "views")
        completions += self.collect_blade_views(res_path)

        # Search Modules/*/Resources/views
        modules_path = os.path.join(root, "Modules")
        if os.path.isdir(modules_path):
            for module in os.listdir(modules_path):
                mod_view_path = os.path.join(modules_path, module, "Resources", "views")
                if os.path.isdir(mod_view_path):
                    completions += self.collect_blade_views(mod_view_path, prefix=module + "::")

        return (completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def collect_blade_views(self, base_path, prefix=""):
        views = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".blade.php"):
                    full_path = os.path.join(root, file)
                    relative = os.path.relpath(full_path, base_path)
                    view_name = relative.replace(".blade.php", "").replace(os.sep, ".")
                    views.append((f"{prefix}{view_name}	view", f"{prefix}{view_name}"))
        return views
