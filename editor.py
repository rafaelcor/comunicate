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

from gi.repository import Gtk, Gdk
from globals import data as Gdata
from globals import UI_INFO
import json

class Editor(Gtk.Window):
    def __init__(self):
        self.data = Gdata # Gdata
        Gtk.Window.__init__(self)
        
        mainVbox = Gtk.VBox()
        
        #menu things
        action_group = Gtk.ActionGroup("my_actions")
        
        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        menusBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        menusBox.pack_start(menubar, False, False, 0)

        toolbar = uimanager.get_widget("/ToolBar")
        menusBox.pack_start(toolbar, False, False, 0)
        #
        mainVbox.pack_start(menusBox, False, False, 0)
        
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
        buttonRemoveGroup.connect("clicked", self.removeElement)

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
        
        mainVbox.pack_start(self.box, False, False, 0)
        
        self.add(mainVbox)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.treeview.grab_focus()
     
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager
    
    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "Archivo", None, None)
        action_group.add_action(action_filemenu)

        action_filenew = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenew)

        action_fileopen = Gtk.Action("FileOpen", None, None, Gtk.STOCK_OPEN)
        action_fileopen.connect("activate", self.on_menu_open)
        action_group.add_action(action_fileopen)

        #action_group.add_actions([
         #   ("FileNew", None, "New File", None, "Create new foo",
          #   self.on_menu_new),
           # ("FileOpen", None, "Open File", None, "Create new goo",
            # self.on_menu_open),
        #])

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def add_edit_menu_actions(self, action_group):
        action_group.add_actions([
            ("EditMenu", None, "Editar"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             None),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             None),
            ("EditPreferences", None, "Preferencias", "<control><alt>S", None,
             None)
        ])
    
    def on_menu_new(self, widget):
        pass

    def on_menu_open(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.data = json.load(open(dialog.get_filename(), 'r'))
            self.build_tree()
            #TODO: refresh treeview on open file
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
        pass

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()
    
    def on_menu_preferences(self, widget):
		pass
    
    def get_board(self, title):
        for board in self.data["boards"]:
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
        self.data = self.get_board(board)["options"][index]
        self.image.set_from_file("images/" + self.data["image"])
        self.speak_check.set_active(self.data["add"])

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
            self.data = self.get_board(board)["options"][index]
            self.data["image"] = chooser.get_filename().split("images/")[1]
            self.save()
            self.image.set_from_file("images/" + self.data["image"])
        
        chooser.close()

    def addElement(self, widget):
        addElementWindow = Gtk.Dialog("Crear elemento", self, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        elementsGrid = Gtk.Grid()
        
        labelText = Gtk.Label("Texto: ")
        entryText = Gtk.Entry()
        
        filterImage = Gtk.FileFilter()
        filterImage.set_name("Image files")
        filterImage.add_mime_type("image/*")
        
        labelImage = Gtk.Label("IMG: ")
        buttonChooseImage = Gtk.FileChooserButton("title")
        buttonChooseImage.add_filter(filterImage)
        
        checkButtonShow = Gtk.CheckButton("Mostrar en el resultado??")
        
        elementsGrid.add(labelText)
        elementsGrid.attach(entryText, 1, 0, 1, 1)
        elementsGrid.attach_next_to(labelImage, labelText, Gtk.PositionType.BOTTOM, 1, 1)
        elementsGrid.attach_next_to(buttonChooseImage, labelImage, Gtk.PositionType.RIGHT, 1, 1)
        elementsGrid.attach(checkButtonShow, 0, 2, 2, 1)
        
        addElementWindow.get_content_area().add(elementsGrid)
        addElementWindow.show_all()
        print dir(addElementWindow)
        if addElementWindow.run() == Gtk.ResponseType.OK:
            model, tree_iter = self.treeview.get_selection().get_selected()
            board = model.get_value(tree_iter,1)
            options = self.get_board(board)["options"]
            options.append({
                "image": buttonChooseImage.get_filename().split("images/")[1],
                "title": entryText.get_text(),
                "add": checkButtonShow.get_active(),
                "board": board
            })
            self.treestore.clear()
            self.build_tree()
        
        addElementWindow.close()
        
    def addGroup(self, widget):
        pass
    
    def removeElement(self, widget):
        
        model, tree_iter = self.treeview.get_selection().get_selected()
        board = model.get_value(tree_iter, 1)
        index = model.get_value(tree_iter, 2)
        title = self.get_board(board)["options"][index]["title"]
        
        #print .get_children()

        removeElementWindow = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, u"¿Realmente desea elminar " + title + "?")
        
        if removeElementWindow.run() == Gtk.ResponseType.YES:
            del self.get_board(board)["options"][index]
            #TODO: fix cursor on remove
            self.treestore.clear()
            self.build_tree()
            self.save()
            
        
        removeElementWindow.close()
    
    def toggleSpeak(self, widget):
        model, tree_iter = self.treeview.get_selection().get_selected()
        board = model.get_value(tree_iter,1)
        index = model.get_value(tree_iter,2)
        self.data = self.get_board(board)["options"][index]
        self.data["add"] = widget.get_active()
        self.save()
    
    def save(self):
        save_file = open("activity.json", "w")
        json.dump(self.data, save_file)
    

Editor()
Gtk.main()
