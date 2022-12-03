
from gi.repository import Gtk, Gio, Adw, GLib

class PrefWindow(Adw.PreferencesWindow):
      def __init__(self, parent):
          Adw.PreferencesWindow.__init__(self)
