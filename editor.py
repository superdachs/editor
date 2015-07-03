#!/usr/bin/env python

from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onOpen(self, *args):
        filechooser = app.builder.get_object("filechooserdialog1")
        filechooser.show_all()

class Editor:

    text = ""

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("editor.glade")
        self.builder.connect_signals(Handler())

    def run(self):
        window = self.builder.get_object("window1")
        window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = Editor()
    app.run()
