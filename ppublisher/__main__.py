import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk

import sys
from ppublisher.file_item import FileItem
from ppublisher.metadata import MetadataEditor
from ppublisher.file_editor import FileEditor
from PyPPUB import ppub_builder


#
# 1. our .glade file (may contain paths)
#
@Gtk.Template.from_file("ppublisher/ppublisher.ui")
class AppWindow(Gtk.ApplicationWindow):
    #
    # 2. the GtkApplicationWindow class
    #
    __gtype_name__ = "ppublisher"

    #
    # 3. the Button id
    #
    editor: Gtk.Box = Gtk.Template.Child()
    file_list: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super(Gtk.ApplicationWindow, self).__init__(**kwargs)
        self.current_editor = None

    def set_editor(self, child):
        if(self.current_editor != None):
            self.editor.remove(self.current_editor)
        self.current_editor = child
        self.editor.add(child)

    def get_all_items(self):
        return [x.get_child() for x in self.file_list.get_children()]

    def set_default_document(self, item):
        items = self.get_all_items()
        for i in items:
            i.set_main(False)
        if(item != None):
            item.set_main(True)

    def get_default_document(self):
        items = self.get_all_items()
        for item in items:
            if(item.is_main):
                return item
        return None

    def get_metadata(self):
        items = self.get_all_items()
        for item in items:
            if(item.is_metadata):
                return item
        return None

    def build_ppub(self, path):
        metadata = self.get_metadata()
        default = self.get_default_document()
        if(metadata == None or default == None):
            raise Exception("No default document or metadata present!")

        builder = ppub_builder.PpubBuilder()
        builder.metadata = metadata.build_metadata()
        self.add_asset(builder, default)
        for item in self.get_all_items():
            if(item == metadata or item == default):
                continue
            self.add_asset(builder, item)

        f = open(path, 'wb')
        builder.write_to_stream(f)
        f.close()

    def add_asset(self, builder, item):
        f = open(item.path, 'rb')
        builder.add_asset(item.filename, item.mimetype, f.read())

    def build_ppix(self, folder_path):
        from PyPPUB.ppix_builder import PpixBuilder
        from PyPPUB import ppub
        builder = PpixBuilder()
        import glob
        paths = glob.glob(folder_path + "/*.ppub")
        for path in paths:
            builder.add_publication(path.split("/")[-1], ppub.Ppub.from_stream(open(path, 'rb')))

        f = open(folder_path + "/lib.ppix", 'wb')
        builder.write_out(f)

    @Gtk.Template.Callback()
    def file_selected(self, widget, list_item):
        item = list_item.get_child()
        if(item.is_metadata):
            self.set_editor(MetadataEditor(item))
        else:
            self.set_editor(FileEditor(item, self))

    @Gtk.Template.Callback()
    def add_file_click(self, widget):
        dialog = Gtk.FileChooserDialog(title = "Add File", parent = self, action = Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            files = dialog.get_filenames()
            for file in files:
                print(file)
                self.file_list.add(FileItem(file))

        dialog.destroy()

    @Gtk.Template.Callback()
    def save_click(self, widget):
        dialog = Gtk.FileChooserDialog(title = "Save PPUB", parent = self, action = Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.build_ppub(dialog.get_filename())
            except Exception as ex:
                error = Gtk.MessageDialog(
                    transient_for=dialog,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text="Error exporting PPUB!",
                )
                error.format_secondary_text(str(ex))
                error.run()

                error.destroy()
            
        dialog.destroy()

    @Gtk.Template.Callback()
    def create_index_click(self, widget):
        dialog = Gtk.FileChooserDialog(title = "Choose a file to build a PPIX index in", parent = self, action = Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Build Index",
            Gtk.ResponseType.OK,
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.build_ppix(dialog.get_filename())
            except Exception as ex:
                error = Gtk.MessageDialog(
                    transient_for=dialog,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text="Error creating PPIX!",
                )
                error.format_secondary_text(str(ex))
                error.run()

                error.destroy()
            
        dialog.destroy()

    @Gtk.Template.Callback()
    def remove_file_click(self, widget):
        item_container = self.file_list.get_selected_row()
        item = item_container.get_child()
        if(item.is_metadata):
            return

        self.file_list.remove(item_container)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.pcthingz.ppublisher",
                         flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        self.window = None

    def do_activate(self):
        self.window = self.window or AppWindow(application=self)
        self.window.present()
        self.window.file_list.add(FileItem(None, True))


if __name__ == '__main__':
    Application().run(sys.argv)
