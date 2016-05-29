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

import json
import os

from gi.repository import Gdk

screen = Gdk.Screen.get_default()
SCREEN_HEIGHT = screen.height()

try:
    from sugar3.activity import activity
    from sugar3.graphics import style

    BUNDLE_PATH = activity.get_bundle_path()
    DIVIDED_HEIGHT = (SCREEN_HEIGHT - style.GRID_CELL_SIZE) / 3
except:
    BUNDLE_PATH = os.path.abspath(".")
    DIVIDED_HEIGHT = (SCREEN_HEIGHT - 50) / 3

DATA_FILE_SRC = 'activity.json'
data = json.load(open(os.path.join(BUNDLE_PATH, DATA_FILE_SRC), 'r'))

FONT_FAMILY = data['configs']['font-family']
FONT_SIZE = data['configs']['font-size']

IMGSIZE = DIVIDED_HEIGHT * 0.90 - FONT_SIZE * 4

SPEED = data['configs']['speed'] * 1000

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileNew' />
      <menuitem action='FileOpen' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditPreferences' />
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNew' />
    <toolitem action='FileOpen' />
    <toolitem action='FileQuit' />
  </toolbar>
</ui>
"""
