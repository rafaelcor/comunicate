#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Daniel Francis
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

import logging

from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Gtk

from espeak import BaseAudioGrab
from globals import data, SPEED
from option import Option, OptionButton

SEPARATION = data['configs']['separation']
MAX_PER_LINE = data['configs']['max_per_line']
LINES = data['configs']['lines']


confirm = {
    'title': 'confirm',
    'options': [
        {
            'title': 'Sí',
            'image': './VARIOS/si.png',
            'board': None
        },
        {
            'title': 'No',
            'image': './VARIOS/no.png',
            'board': None
        }
    ]
}


class Canvas(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        s, color = Gdk.Color.parse(data['configs']['bgcolor'])
        self.modify_bg(Gtk.StateType.NORMAL, color)
        self.confirm = False
        self.speech = BaseAudioGrab()
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.button_pressed)
        self.canvasbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.canvasbox)
        self.canvasbox.show()
        self.show()

        # Top part
        top = Gtk.Box()
        self.sentence = Gtk.Box()
        self.sentence.show()
        top.pack_start(self.sentence, True, True, 0)
        self.delbtn = OptionButton({'title': 'Borrar',
                                    'image': 'OPUESTOS/no.png'})
        top.pack_start(self.delbtn,
                       False, True, 0)

        top.show()
        self.canvasbox.pack_start(top, True, True, 0)

        GObject.timeout_add(SPEED, self.update_selection)
        self.removable = []
        self.boards = [data['boards'][0]]
        self.fill_board(data['boards'][0])
        self.phrases = []

    def get_board(self, title):
        for board in data["boards"]:
            if board['id'] == title:
                return board

    def button_pressed(self, widget, event=None):
        selection = self.selected - 1
        if selection == -1:
            self.sentence.remove(self.phrases[-1])
            del(self.phrases[-1])
            del(self.boards[-1])
            self.fill_board(self.boards[-1])
        else:
            if selection == -2:
                opt = self.buttons[-1].opt
            else:
                opt = self.buttons[selection].opt
            if self.confirm:
                if opt["title"] == 'Sí':
                    self.speak()
                self.confirm = False
                self.fill_board(data['boards'][0])
                self.clear_sentence()
                return
            option = Option(opt)
            #self.phrases.append(option)
            #self.sentence.pack_start(option, False, False, SEPARATION) #### SEE

            if opt["add"]:
                self.phrases.append(option)
                self.sentence.pack_start(option, False, False, SEPARATION) #### SEE
                print opt["board"]
            if opt["board"] is not None:
                self.fill_board(self.get_board(opt["board"]))

            else:
                self.fill_board(confirm)
                self.confirm = True

    def speak(self):
        msg = ''
        for phrase in self.phrases:
            msg += phrase.option['title']
        self.speech.speak(None, msg)

    def clear_sentence(self):
        for phrase in self.phrases:
            self.sentence.remove(phrase)
            phrase.destroy()
        self.phrases = []

    def update_selection(self):
        if self.selected == -1:
            self.delbtn.select()
        else:
            self.buttons[self.selected].select()
        self.selected += 1
        if self.selected == len(self.buttons):
            self.selected = -1
        GObject.timeout_add(SPEED, self.update_selection)

    def fill_board(self, board):
        if len(self.boards) == 0:
            self.boards = [board]
        if self.boards[-1] != board:
            self.boards.append(board)
        self.selected = -1
        self.buttons = []
        for i in self.removable:
            self.canvasbox.remove(i)
        self.removable = []

        elem = 0
        box = None
        for i in board['options']:
            if elem == 0:
                box = Gtk.Box()
                box.show()
                self.canvasbox.pack_start(box, True, True, SEPARATION)
                self.removable.append(box)
            option = OptionButton(i)
            option.connect('clicked', self.button_pressed)
            self.buttons.append(option)
            box.pack_start(option, True, True, SEPARATION)
            elem += 1
            if elem == MAX_PER_LINE:
                elem = 0


if __name__ == "__main__":
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)
    canvas = Canvas()
    window.add(canvas)
    window.maximize()
    window.show()
    Gtk.main()
