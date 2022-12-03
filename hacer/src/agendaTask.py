import sys
import gi
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib

class AgendaTask(Adw.ActionRow):

    task_name = ""
    #taskId = 0
    task_list = ""
    next_task = ""
    previous_task = ""

    def __init__(self, data):
        Adw.ActionRow.__init__(self)
        #TODO:Make this a ui file

        self.add_css_class("title-2")
        self.set_selectable(False);
        self.set_activatable(True);

        self.create_trash_button()
        self.create_check_button(data)



    def on_trashed(self, widget):
        list_box = self.get_parent()
        window = self.get_root()
        window.taskcount -= 1
        list_box.remove(self)

        with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                i = 0
                #finds by name
                for x in data['tasks']:
                    if(data['tasks'][i]['task_name'] == self.task_name):
                        del data['tasks'][i]
                    i += 1

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()

    def complete(self):
        self.set_title("<s>" + self.task_name + "</s>")

    def on_toggled(self, widget):
        if(widget.get_active()):
            self.complete()
            with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                i = 0
                #finds by name
                for x in data['tasks']:
                    if(data['tasks'][i]['task_name'] == self.task_name):
                        data['tasks'][i]['complete'] = "True"
                    i += 1

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()
        else :
            self.set_title(self.task_name)
            with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
                data = json.load(file)
                i = 0
                #finds by name
                for x in data['tasks']:
                    if(data['tasks'][i]['task_name'] == self.task_name):
                        data['tasks'][i]['complete'] = "False"
                    i += 1

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                file.close()

    def create_trash_button(self):
        trash = Gtk.Button()
        trash.set_valign(Gtk.Align.CENTER)
        trash.set_halign(Gtk.Align.CENTER)
        trash.add_css_class("destructive-action")
        #trash.add_css_class("circular")
        trash.set_sensitive(True)
        trash.set_icon_name("user-trash-symbolic")
        trash.connect("clicked", self.on_trashed)
        self.add_suffix(trash)

    def create_check_button(self, data):
        check = Gtk.CheckButton()
        self.add_prefix(check)
        check.connect("toggled", self.on_toggled)

         #fills data from JSON
        if(type(data) is dict):
            self.task_name = data['task_name']
            self.set_title(self.task_name)
            #self.taskId = data['id']
            if(data['complete'] == 'True'):
                check.set_active(True)
        #fills data from string
        else:
            self.task_name = data
            self.set_title(self.task_name)

