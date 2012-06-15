import sublime, sublime_plugin

from _align import String

class AlignCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		v = self.view
		reg = v.sel()[0]

		begin = reg.begin()
		row, col = v.rowcol(reg.end())

		char = v.substr(reg.end() - 1)
		reg = v.line(reg)
		v.replace(edit, reg, String(v.substr(reg)).align_at(char) )
		v.sel().clear()
		endline  = v.text_point(row, 0) 
		end = v.find(char, v.text_point(row, 0), 	sublime.LITERAL).end()	
		v.sel().add(sublime.Region(begin, end))

class PwdCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message(self.view.file_name())