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
import time
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib
from .agendaTask import AgendaTask
from .linkedListBox import LinkedListBox
from pathlib import Path

@Gtk.Template(resource_path='/com/github/halfmexican/hacer/window.ui')
class HacerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'HacerWindow'

    tmp = LinkedListBox()

    taskList = Gtk.Template.Child("Gtk-ListBox-TaskList")
    ttRevealer = Gtk.Template.Child('TaskLabelRevealer')
    taskWindowTitle = Gtk.Template.Child('TaskWindowTitle')
    taskEntry = Gtk.Template.Child("Gtk-Entry-TaskEntry")
    leaflet = Gtk.Template.Child("Adw-Leaflet-leaflet")
    taskView = Gtk.Template.Child("TaskView")
    listView = Gtk.Template.Child("ListView")
    taskLabel = Gtk.Template.Child("TaskLabel")
    leafletBackButton = Gtk.Template.Child("LeafletBackButton")
    leafletForwardButton = Gtk.Template.Child("LeafletForwardButton")
    listBoxList = Gtk.Template.Child("Gtk-ListBox-Lists")
    allTasks = Gtk.Template.Child("Adw-ActionRow-AllTasks")
    completedTasks = Gtk.Template.Child("Adw-ActionRow-CompletedTasks")

    taskcount = 0
    maxId = 0

    def __init__(self, **kwargs):

        start_time = time.time()

        super().__init__(**kwargs)

        self.taskEntry.connect("activate", self.on_enter_released)

        self.leafletBackButton.connect("clicked", self.on_leaflet_back_clicked)
        self.leafletForwardButton.connect("clicked", self.on_leaflet_forward_clicked)
        self.leaflet.set_visible_child(self.taskView)

        self.load_all_tasks()
       ##################
        self.set_icon_name('com.github.halfmexican.hacer')

        self.allTasks.set_activatable(True)
        self.allTasks.connect("activated", self.display_all_tasks)
        self.completedTasks.set_activatable(True)
        self.completedTasks.connect("activated", self.display_completed_tasks)

        self.listBoxList.select_row(self.allTasks)

        self.ttRevealer.get_transition_type()

        #print(self.maxId)
        end_time = time.time()
        print(f"It took {end_time-start_time:.2f} seconds to init")

        GLib.timeout_add(120, self.resize_stuff)

    def on_enter_released(self, widget):

        text = self.taskEntry.get_text() #gets text from entry
        self.add_agenda_item(text) #creates new AgendaTask from text
        self.taskEntry.set_text("")

        with open(GLib.get_user_data_dir()+'/tasks.json', 'r+') as file :
            data = json.load(file)
            data['tasks'].append({'task_name':text, 'complete':'False'})
            #self.maxId += 1
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            file.close()

    def add_agenda_item(self, data):
        self.taskcount += 1
        task = AgendaTask(data)
        self.taskList.append(task)

    def on_leaflet_back_clicked(self, widget):
        self.leaflet.navigate(Adw.NavigationDirection.BACK)

    def on_leaflet_forward_clicked(self, widget):
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    def load_all_tasks(self): #//TODO:ADD seperate list support without breaking the all tasks lsit
        file = Path(GLib.get_user_data_dir()+'/tasks.json')
        #if the file exists then we can read it and generate tasks from it
        if(file.is_file()):
            file = open(GLib.get_user_data_dir()+'/tasks.json') #directory where lists are stored
            data = json.load(file)
            i = 0
            for x in data['tasks']:
                self.add_agenda_item(data['tasks'][i])
                #if(data['tasks'][i]['id'] > self.maxId):
                   # self.maxId = data['tasks'][i]['id'] + 1
                i += 1

        else:
            #if the file doesn't exist then lets create new file with an empty array
            print('nofile')
            with open(GLib.get_user_data_dir()+'/tasks.json', 'w+') as file:
                dictionary = {"tasks":[]}
                json_object = json.dumps(dictionary, indent=4)
                json.dump(dictionary, file)

    def load_completed_tasks(self): #//TODO:ADD seperate list support without breaking the all tasks lsit
        file = Path(GLib.get_user_data_dir()+'/tasks.json')
        if(file.is_file()):
            file = open(GLib.get_user_data_dir()+'/tasks.json') #directory where lists are stored
            data = json.load(file)
            name =''
            i = 0
            for x in data['tasks']:
                if(data['tasks'][i]['complete'] == "True"):
                    self.add_agenda_item(data['tasks'][i])

                i += 1

    def display_all_tasks(self, widget):
        self.currList = 0
        self.clear_tasklist()
        self.load_all_tasks()
        self.leaflet.set_visible_child(self.taskView)
        self.taskEntry.set_sensitive(True)

    def display_completed_tasks(self, widget):
        self.clear_tasklist()
        self.load_completed_tasks()
        self.leaflet.set_visible_child(self.taskView)
        self.taskEntry.set_sensitive(False)

    def clear_tasklist(self):
        count = self.taskcount
        for x in range(count):
            task = self.taskList.get_row_at_index(0)
            self.taskList.remove(task)
            self.taskcount -= 1

    def resize_stuff(self):
        print(self.get_allocation().height)
        if(self.get_allocation().height < 615):
            self.ttRevealer.set_reveal_child(False)
            self.taskWindowTitle.set_title("Tasks")
        else:
            self.ttRevealer.set_reveal_child(True)
            self.taskWindowTitle.set_title("Hacer")

        GLib.timeout_add(200, self.resize_stuff)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Hacer'
        self.props.version = "0.1.0"
        self.props.authors = ['José Hunter']
        self.props.copyright = '2022 José Hunter'
        self.props.logo_icon_name = 'com.github.halfmexican.hacer'
        self.props.modal = True
        self.set_transient_for(parent)
