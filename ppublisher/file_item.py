import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

import os
import mimetypes
from PyPPUB import ppub_builder
import datetime

@Gtk.Template.from_file("ppublisher/file.ui")
class FileItem(Gtk.Box):

    __gtype_name__ = "file_item"

    list_filename: Gtk.Label = Gtk.Template.Child()
    star: Gtk.Image = Gtk.Template.Child()
    list_mimetype: Gtk.Label = Gtk.Template.Child()

    def __init__(self, path, is_metadata = False):
        super(Gtk.Box, self).__init__()
        self.path = path
        self.filename = "metadata"
        self.is_main = False
        self.is_metadata = is_metadata

        if(not is_metadata):
            self.mimetype = mimetypes.guess_type(path)[0] or "application/octet-stream"
            self.filename = os.path.split(path)[1]
            self.list_filename.set_text(self.filename)
            self.list_mimetype.set_text(self.mimetype)

        else:
            self.list_filename.set_text("Metadata")
            self.list_mimetype.set_text("application/x-ppub-metadata")
            self.mimetype = "application/x-ppub-metadata"
            self.star.set_from_icon_name("document-properties-symbolic", Gtk.IconSize.MENU)

            self.title = "My book"
            self.author = ""
            self.description = ""
            self.tags = ""
            self.licence = ""
            self.copyright = ""
        
        self.set_main(False)

    def set_main(self, main):
        self.is_main = main
        if(not self.is_metadata):
            if(main):
                self.star.set_from_icon_name("starred-symbolic", Gtk.IconSize.MENU)
            else:
                self.star.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.MENU)

    def build_metadata(self):
        metadata = ppub_builder.Metadata()
        
        def add_if_present(field, value):
            if(value != None or value != ""):
                metadata.set_value(field, value)

        add_if_present("title", self.title)
        add_if_present("author", self.author)
        add_if_present("description", self.description)
        add_if_present("tags", self.tags)
        add_if_present("licence", self.licence)
        add_if_present("copyright", self.copyright)
        metadata.set_value("date", datetime.datetime.now().astimezone().isoformat())
        return metadata