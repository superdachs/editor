#!/usr/bin/env python

from gi.repository import Gtk, Gdk

class Handler:
    def onDeleteWindow(self, *args):
        quit = True
        if app.builder.get_object("textview1").get_buffer().get_modified():
            quit = self.askForSave()
        if quit:
            Gtk.main_quit(*args)

    def askForSave(self, *args):
        dialog = Gtk.Dialog("ask for save dialog", app.builder.get_object("window1"), 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_YES, Gtk.ResponseType.YES,
             Gtk.STOCK_NO, Gtk.ResponseType.NO))
        dialog.get_content_area().add(Gtk.Label("Datei nicht gespeichert. Wollen Sie die datei jetzt speichern?"))
        dialog.set_default_size(150, 100)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            self.onSave(*args)
            dialog.destroy()
            if not app.builder.get_object("textview1").get_buffer().get_modified():
                return True
            else:
                return False
        elif response == Gtk.ResponseType.NO:
            dialog.destroy()
            return True
        else:
            dialog.destroy()
            return False

    def onOpen(self, *args):
        dialog = Gtk.FileChooserDialog("open file", app.builder.get_object("window1"),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open (dialog.get_filename(), "r") as loadedfile:
                app.updateEditor("".join(loadedfile.readlines()), dialog.get_filename())
                app.file = dialog.get_filename()
                app.builder.get_object("textview1").get_buffer().set_modified(False)
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
            self.onSaveAs(*args)
            return
        self.save(app.file)

    def save(self, filename):
        with open (filename, "w") as loadedfile:
            buffer = app.builder.get_object("textview1").get_buffer()
            loadedfile.write(buffer.get_text(*buffer.get_bounds(), include_hidden_chars=True))
            app.file = filename
            buffer.set_modified(False)
            window = app.builder.get_object("window1").set_title(filename)

    def onNew(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.delete(*buffer.get_bounds())
        app.file = ""
        app.builder.get_object("window1").set_title("editor")
        buffer.set_modified(False)

    def onModified(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        if buffer.get_modified():
            title = app.builder.get_object("window1").get_title()
            app.builder.get_object("window1").set_title(title + "*")

    def onCopy(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.copy_clipboard(app.clipboard)

    def onCut(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.cut_clipboard(app.clipboard, True)

    def onPaste(self, *args):
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.paste_clipboard(app.clipboard, None, True)

    def onInfo(self, *args):
        dialog = app.builder.get_object("window2")
        dialog.set_title("info")
        dialog.show_all()

    def onInfoOk(sel, *args):
        app.builder.get_object("window2").hide()

class Editor:

    file = ""

    def __init__(self):
        self.builder = Gtk.Builder()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.builder.add_from_file("editor.glade")
        self.builder.connect_signals(Handler())

    def updateEditor(self, text, title):
        self.builder.get_object("textview1").get_buffer().set_text(text)
        self.builder.get_object("window1").set_title(title)
        file = title

    def run(self):
        window = self.builder.get_object("window1")
        window.set_title("editor")
        window.set_default_size(480, 340)
        buffer = app.builder.get_object("textview1").get_buffer()
        buffer.connect("modified-changed", Handler.onModified)
        window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = Editor()
    app.run()
