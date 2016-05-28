#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Rafael Cordano <rafael.cordano@gmail.com>
# Copyright (C) 2016 Ezequiel Pereira <eze2307@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gtk
from globals import data
import json

class Editor(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.treestore = Gtk.TreeStore(str, int, int)
        self.build_tree()

        renderer = Gtk.CellRendererText()
        renderer.connect("edited", self.item_edit)
        renderer.set_property('editable', True)
        column = Gtk.TreeViewColumn("Opciones", renderer, text=0)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)

        self.treeview = Gtk.TreeView(self.treestore)
        self.treeview.append_column(column)
        
        self.treeview.connect("cursor-changed", self.tree_selection)

        buttonAddElement = Gtk.Button("Agregar Elemento")
        buttonAddGroup = Gtk.Button("Agregar Grupo")
        buttonRemoveElement = Gtk.Button("Eliminar Elemento")
        buttonRemoveGroup = Gtk.Button("Eliminar Grupo")
        
        treeScrolledWindow = Gtk.ScrolledWindow()
        treeScrolledWindow.add(self.treeview)
        treeScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                      Gtk.PolicyType.AUTOMATIC)
        
        treebox = Gtk.VBox()
        treebox.pack_start(treeScrolledWindow, True, True, 0)
        treebox.pack_start(buttonAddElement, False, False, 0)
        treebox.pack_start(buttonAddGroup, False, False, 0)
        treebox.pack_start(buttonRemoveGroup, False, False, 0)
        treebox.pack_start(buttonRemoveElement, False, False, 0)
        
        buttonAddElement.connect("clicked", self.addElement)
        buttonAddGroup.connect("clicked", self.addGroup)
        buttonRemoveElement.connect("clicked", self.removeElement)
        buttonRemoveGroup.connect("clicked", self.addElement)

        self.image = Gtk.Image()
        edit = Gtk.Button.new_from_icon_name("document-edit",
                                             Gtk.IconSize.BUTTON)
        edit.set_valign(Gtk.Align.START)
        edit.set_halign(Gtk.Align.END)
        edit.connect("clicked", self.editImage)
        overlay = Gtk.Overlay()
        overlay.add(self.image)
        overlay.add_overlay(edit)
        self.speak_check = Gtk.CheckButton("¿Agregar?")
        self.speak_check.connect("toggled", self.toggleSpeak)

        labelbox = Gtk.VBox()
        labelbox.pack_start(overlay, False, False, 0)
        labelbox.pack_start(self.speak_check, False, False, 0)

        self.box = Gtk.HPaned()
        self.box.pack1(treebox, False, False)
        self.box.pack2(labelbox, True, False)
        
        self.add(self.box)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.treeview.grab_focus()

    def get_board(self, title):
        for board in data["boards"]:
            if board['id'] == title:
                return board

    def build_tree(self, name=0, parent=None):
        board = self.get_board(name)
        for index in xrange(0, len(board["options"])):
            option = board["options"][index]
            if option["board"] != None:
                handle = self.treestore.append(
                    parent, [option["title"], name, index])
                if option["board"] != 0:
                    self.build_tree(option["board"], handle)

    def tree_selection(self, widget):
        model, tree_iter = widget.get_selection().get_selected()
        name = model.get_value(tree_iter,0)
        board = model.get_value(tree_iter,1)
        index = model.get_value(tree_iter,2)
        data = self.get_board(board)["options"][index]
        self.image.set_from_file("images/" + data["image"])
        self.speak_check.set_active(data["add"])

    def item_edit(self, widget, path, text):
        board = self.get_board(self.treestore[path][1])
        board["options"][self.treestore[path][2]]["title"] = text
        self.treestore[path][0] = text
        self.save()
    
    def editImage(self, widget):
        filterImage = Gtk.FileFilter()
        filterImage.set_name("Image files")
        filterImage.add_mime_type("image/*")
        
        
        chooser = Gtk.FileChooserDialog(title=None,
                                        action=Gtk.FileChooserAction.OPEN,
                                        buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        chooser.add_filter(filterImage)
        
        
        
        if chooser.run() == Gtk.ResponseType.OK:
            #get_filename()
            model, tree_iter = self.treeview.get_selection().get_selected()
            board = model.get_value(tree_iter,1)
            index = model.get_value(tree_iter,2)
            data = self.get_board(board)["options"][index]
            data["image"] = chooser.get_filename().split("images/")[1]
            self.save()
            self.image.set_from_file("images/" + data["image"])
        
        chooser.close()
            
    
    def addElement(self, widget):
        pass
    
    def addGroup(self, widget):
        pass
    
    def removeElement(self, widget):  
        pass
    
    def removeGroup(self, widget):
        pass
    
    def toggleSpeak(self, widget):
        model, tree_iter = self.treeview.get_selection().get_selected()
        board = model.get_value(tree_iter,1)
        index = model.get_value(tree_iter,2)
        data = self.get_board(board)["options"][index]
        data["add"] = widget.get_active()
        self.save()
    
    def save(self):
        save_file = open("activity.json", "w")
        json.dump(data, save_file)
    
    def minimizeJSON(self):
        pass

Editor()
Gtk.main()
