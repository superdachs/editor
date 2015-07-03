#!/usr/bin/env python

from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onOpen(self, *args):
        dialog = Gtk.FileChooserDialog("open file", app.builder.get_object("window1"),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open (dialog.get_filename(), "r") as loadedfile:
                app.updateEditor("".join(loadedfile.readlines()), dialog.get_filename())
        dialog.destroy()


    def onSaveAs(self, *args):
        dialog = Gtk.FileChooserDialog("save file as", app.builder.get_object("window1"),
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.save(dialog.get_filename())
        dialog.destroy()

    def onSave(self, *args):
        if app.file == "":
            self.onSaveAs(args)
            return
        self.save(app.file)

    def save(self, filename):
        with open (filename, "w") as loadedfile:
            buffer = app.builder.get_object("textview1").get_buffer()
            loadedfile.write(buffer.get_text(*buffer.get_bounds(), include_hidden_chars=True))
            app.file = filename
            app.saved = True
            window = app.builder.get_object("window1").set_title(filename)

    def onNew(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.delete(*buffer.get_bounds())
        app.file = ""
        app.builder.get_object("window1").set_title("editor")

    def onModified(self, *args):
        if app.saved:
            app.saved = False
            print("modified")
            title = app.builder.get_object("window1").get_title()
            app.builder.get_object("window1").set_title(title + "*")


class Editor:

    file = ""
    saved = True

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("editor.glade")
        self.builder.connect_signals(Handler())

    def updateEditor(self, text, title):
        self.builder.get_object("textview1").get_buffer().set_text(text)
        self.builder.get_object("window1").set_title(title)
        file = title

    def run(self):
        window = self.builder.get_object("window1")
        window.set_title("editor")
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.connect("modified-changed", Handler.onModified)
        window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = Editor()
    app.run()
