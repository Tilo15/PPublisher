import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

import os
import mimetypes

@Gtk.Template.from_file("ppublisher/metadata.ui")
class MetadataEditor(Gtk.Box):

    __gtype_name__ = "metadata_editor"

    title_edit: Gtk.Entry = Gtk.Template.Child()
    author_edit: Gtk.Entry = Gtk.Template.Child()
    description_edit: Gtk.Entry = Gtk.Template.Child()
    tags_edit: Gtk.Entry = Gtk.Template.Child()
    licence_edit: Gtk.Entry = Gtk.Template.Child()
    copyright_edit: Gtk.Entry = Gtk.Template.Child()

    def __init__(self, metadata):
        super(Gtk.Box, self).__init__()

        self.metadata = metadata

        self.title_edit.set_text(self.metadata.title)
        self.author_edit.set_text(self.metadata.author)
        self.description_edit.set_text(self.metadata.description)
        self.tags_edit.set_text(self.metadata.tags)
        self.licence_edit.set_text(self.metadata.licence)
        self.copyright_edit.set_text(self.metadata.copyright)

    @Gtk.Template.Callback()
    def data_changed(self, widget):
        self.metadata.title = self.title_edit.get_text()
        self.metadata.author = self.author_edit.get_text()
        self.metadata.description = self.description_edit.get_text()
        self.metadata.tags = self.tags_edit.get_text()
        self.metadata.licence = self.licence_edit.get_text()
        self.metadata.copyright = self.copyright_edit.get_text()


