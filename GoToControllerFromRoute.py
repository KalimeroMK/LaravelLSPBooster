import sublime
import sublime_plugin
import os
import re

class GoToControllerFromRouteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()[0]
        line = self.view.substr(self.view.line(sel))
        match = re.search(r"route\(['\"]([^'\"]+)['\"]", line)
        if not match:
            sublime.status_message("No route() name found on this line.")
            return

        route_name = match.group(1)
        folders = self.view.window().folders()
        if not folders:
            return

        root = folders[0]
        route_file = os.path.join(root, "routes", "web.php")
        if not os.path.exists(route_file):
            sublime.status_message("web.php not found.")
            return

        with open(route_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = re.compile(r"Route::[a-zA-Z]+\([^\)]*\)->name\(['\"]" + re.escape(route_name) + r"['\"]\)")
        match = pattern.search(content)
        if not match:
            sublime.status_message("Named route not found.")
            return

        line_content = match.group(0)
        ctrl_match = re.search(r"(\[\w\\]+)::class\s*,\s*['\"](\w+)['\"]", line_content)
        if not ctrl_match:
            sublime.status_message("Could not parse controller from route.")
            return

        controller_class = ctrl_match.group(1).replace("\\", "/")
        method_name = ctrl_match.group(2)

        controller_path = os.path.join(root, "app", "Http", "Controllers", controller_class + ".php")
        if not os.path.exists(controller_path):
            sublime.status_message("Controller not found: " + controller_path)
            return

        # Open file and try to find method
        view = self.view.window().open_file(controller_path)
        sublime.set_timeout_async(lambda: self.jump_to_method(view, method_name), 500)

    def jump_to_method(self, view, method):
        def run_jump():
            region = view.find(r"function\s+" + re.escape(method) + r"\b", 0)
            if region:
                view.sel().clear()
                view.sel().add(region)
                view.show(region)
        sublime.set_timeout(run_jump, 1000)
