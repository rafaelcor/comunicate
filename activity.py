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
import os

from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Gdk
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.toolbarbox import ToolbarBox

from globals import data, BUNDLE_PATH, IMGSIZE
from option import Option, OptionButton

SEPARATION = data['configs']['separation']
MAX_PER_LINE = data['configs']['max_per_line']
LINES = data['configs']['lines']


class ComunicateActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        self.build_toolbar()

        self.evbox = Gtk.EventBox()
        self.evbox.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.evbox.connect('button-press-event', self.button_pressed)
        self.canvasbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.evbox.add(self.canvasbox)
        self.set_canvas(self.evbox)
        self.canvasbox.show()
        self.evbox.show()

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

        GObject.timeout_add(1000, self.update_selection)
        self.fill_board()
        self.selected = 0
        self.phrases = []

    def button_pressed(self, widget, event=None):
        logging.error(self.selected)
        if self.selected - 1 == -1:
            logging.error('Remove!')
            self.sentence.remove(self.phrases[-1])
            del(self.phrases[-1])
        else:
            option = Option(self.buttons[self.selected - 1].opt)
            self.phrases.append(option)
            self.sentence.pack_start(option, False, False, SEPARATION)

    def update_selection(self):
        if self.selected == -1:
            self.delbtn.select()
        else:
            self.buttons[self.selected].select()
        self.selected += 1
        if self.selected == len(self.buttons):
            self.selected = -1
        GObject.timeout_add(1000, self.update_selection)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        self.removable = []

    def fill_board(self):
        self.buttons = []
        for i in self.removable:
            self.canvasbox.remove(i)

        elem = 0
        box = None
        for i in data['boards'][0]['options']:
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
            if elem == 3:
                elem = 0
