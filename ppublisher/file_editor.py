import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

import os
import mimetypes

@Gtk.Template.from_file("ppublisher/file_editor.ui")
class FileEditor(Gtk.Box):

    __gtype_name__ = "file_editor"

    editor_filename: Gtk.Label = Gtk.Template.Child()
    editor_mimetype: Gtk.Label = Gtk.Template.Child()
    editor_default_document: Gtk.CheckButton = Gtk.Template.Child()

    def __init__(self, file, window):
        super(Gtk.Box, self).__init__()

        self.file = file
        self.window = window

        self.editor_filename.set_text(file.list_filename.get_text())
        self.editor_mimetype.set_text(file.mimetype)
        self.editor_default_document.set_active(file.is_main)

    @Gtk.Template.Callback()
    def default_toggled(self, widget):
        enabled = widget.get_active()
        if(enabled):
            self.window.set_default_document(self.file)
        else:
            self.window.set_default_document(None)


