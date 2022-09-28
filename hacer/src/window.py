# window.py
#
# Copyright 2022 josehunter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib
from .agendaTask import AgendaTask
from pathlib import Path

@Gtk.Template(resource_path='/com/github/halfmexican/hacer/window.ui')
class HacerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'HacerWindow'

    list = Gtk.Template.Child("list")
    entry = Gtk.Template.Child("entry")
    leaflet = Gtk.Template.Child("leaflet")
    taskview = Gtk.Template.Child("TaskView")
    listview = Gtk.Template.Child("ListView")
    leafletBackButton = Gtk.Template.Child("LeafletBackButton")
    leafletForwardButton = Gtk.Template.Child("LeafletForwardButton")
    taskcount = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry.connect("activate", self.on_enter_released)
        self.leafletBackButton.connect("clicked", self.on_leaflet_back_clicked)
        self.leafletForwardButton.connect("clicked", self.on_leaflet_forward_clicked)
        self.load_json()
        self.set_icon_name('com.github.halfmexican.hacer')
        self.leaflet.set_visible_child(self.taskview)
        print(self.taskcount)

    def on_enter_released(self, widget):
     text = self.entry.get_text()
     self.add_agenda_item(text, False)
     self.entry.set_text("")

     with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
        data = json.load(file)
        data['tasks'].append({'taskname':text, 'complete':'False'})
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        file.close()

    def add_agenda_item(self, title, status):
        task = AgendaTask(title, status, (self.taskcount - 1)) #sets new tasks index in the array
        self.list.append(task)

    def on_leaflet_back_clicked(self, widget):
        self.leaflet.navigate(Adw.NavigationDirection.BACK)

    def on_leaflet_forward_clicked(self, widget):
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    def load_json(self):
        file = Path(GLib.get_user_data_dir()+'/tasks.json')
        #if the file exists then we can read it and generate tasks from it
        if(file.is_file()):
            file = open(GLib.get_user_data_dir()+'/tasks.json') #directory where lists are stored
            data = json.load(file)
            name =''
            index = 0
            for i in data['tasks']:
                self.taskcount += 1
                self.add_agenda_item(data['tasks'][index]['taskname'], data['tasks'][index]['complete'])
                index += 1
        else:
            #if the file doesn't exist then lets create new file with an empty array
            print('nofile')
            with open(GLib.get_user_data_dir()+'/tasks.json', 'w+') as file:
                dictionary = {"tasks":[]}
                json_object = json.dumps(dictionary, indent=4)
                json.dump(dictionary, file)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Hacer'
        self.props.version = "0.1.0"
        self.props.authors = ['josehunter']
        self.props.copyright = '2022 josehunter'
        self.props.logo_icon_name = 'com.github.halfmexican.hacer'
        self.props.modal = True
        self.set_transient_for(parent)
