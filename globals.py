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

SCREEN_HEIGHT = Gdk.Screen().height()

try:
    from sugar3.activity import activity
    from sugar3.graphics import style

    BUNDLE_PATH = activity.get_bundle_path()
    DIVIDED_HEIGHT = (SCREEN_HEIGHT - style.GRID_CELL_SIZE) / 3
except:
    BUNDLE_PATH = os.path.abspath(".")
    DIVIDED_HEIGHT = (SCREEN_HEIGHT - 50) / 3

IMGSIZE = DIVIDED_HEIGHT * 0.80
data = json.load(open(os.path.join(BUNDLE_PATH, 'activity.json'), 'r'))

SPEED = data['configs']['speed'] * 1000
