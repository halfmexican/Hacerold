import sys
import gi
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib

class AgendaTask(Adw.ActionRow):

    taskName = ""
    index = 0

    def __init__(self, title, status, index):
        Adw.ActionRow.__init__(self)
        self.index = index
        self.taskName = title
        self.set_title(title)
        self.add_css_class("title-2")
        self.set_selectable(False);
        self.set_activatable(True);


        check = Gtk.CheckButton()
        self.add_prefix(check)
        check.connect("toggled", self.on_toggled)

        if(status == 'True'):
            self.complete()
            check.set_active(True)

        trash = Gtk.Button()
        trash.set_valign(Gtk.Align.CENTER)
        trash.add_css_class("destructive-action")
        trash.set_sensitive(True)
        trash.set_icon_name("user-trash-symbolic")
        trash.connect("clicked", self.on_trashed)
        self.add_suffix(trash)

    def on_trashed(self, widget):
        listBox = self.get_parent()
        listBox.remove(self)

        with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                del data['tasks'][self.index]
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()

    def complete(self):
        self.set_title("<s>" + self.taskName + "</s>")

    def on_toggled(self, widget):
        if(widget.get_active()):
            self.complete()
            with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                data['tasks'][self.index]['complete'] = "True"
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()
        else :
            self.set_title(self.taskName)
            with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                data['tasks'][self.index]['complete'] = "False"
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()


