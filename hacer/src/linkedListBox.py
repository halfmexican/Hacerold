import sys
import gi
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib

@Gtk.Template(resource_path="/com/github/halfmexican/hacer/linkedListBox.ui")
class LinkedListBox(Gtk.ListBox):
    __gtype_name__ = "LinkedListBox"

    def __init__(self):
        Gtk.ListBox.__init__(self)
