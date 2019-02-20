import sublime
import sublime_plugin


def transform_file_to_json(self, file_content):
	file_name = self.view.file_name()
	if len(file_name) > 2:
		file_name = file_name[file_name.rfind("/")+1:]
	return """{\n\t\"name\":""" + "\"" + file_name + "\",\n" + """\t\"conversations\":\n\t[\n""" + file_content +"""\n\t]\n}"""


def transform_text_to_convos(self, sel, text):
    text = text.split("\n")
    result = ""
    for line in text:
        if text[len(text)-1] is not line:
            next_line = text[text.index(line)+1]
            if line is not "":
                if next_line is not "":
                    result += """\t\t{\"from\":\"""" + line + """\",\n\t\t\"to\":\"""" + next_line + """\"},\n"""

    if not self.view.substr(sublime.Region(sel.b, self.view.size()-1)).isalpha():
    	result = result[:-2]
    return result


class SrtJsonCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selections = self.view.sel()
		for s in selections:
			self.view.replace(edit, s, transform_text_to_convos(self, s, self.view.substr(s)))


class FileToJsonCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selections = self.view.sel()
		for s in selections:
			self.view.replace(edit, s, transform_file_to_json(self, self.view.substr(s)))
