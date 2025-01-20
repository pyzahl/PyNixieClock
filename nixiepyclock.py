#!/usr/bin/env python


#/* 
# * Copyright (C) 20250120 Percy Zahl
# *
# * Authors: Percy Zahl
# * https://github.com/pyzahl
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
# */
#
# Credits for the Nixie tube renderings to:
# https://grabcad.com/library/in-8-nixie-tube-1

import sys
import math
import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject, GLib, Gdk
#from threading import Timer
import cairo

scale   = 0.2
opacity = 0.75

print ("\nPyNixieClock [scale=0.2 [opcaity=0.75]]\n")

if len(sys.argv) > 1:
    scale = float(sys.argv[1])
    print (scale)

if len(sys.argv) > 2:
    opacity = float(sys.argv[2])
    print (opacity)



class NixieTube(Gtk.DrawingArea):
    def __init__(self, widget_scale=0.2):

        if scale > 0 and scale < 10:
            self.cairo_scale=scale
        else:
            self.cairo_scale=widget_scale
        super(NixieTube, self).__init__()
        self.set_size_request(185*self.cairo_scale, 538*self.cairo_scale)

        self.colon = False
        self.set_reading(-1)
        self.set_draw_func(self.draw)
  
    def draw(self, widget, cr, width, height):

        #cr.set_operator(cairo.OPERATOR_CLEAR)
        # Makes the mask fill the entire window
        #cr.rectangle(0.0, 0.0, width, height)
        # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
        #cr.fill()
        # Set the compositing operator back to the default
        #cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.rectangle(0.0, 0.0, width, height)
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.scale(self.cairo_scale, self.cairo_scale)
        cr.set_source_surface (self.nixiesurface)
        cr.paint()
        cr.stroke()
        if self.colon:
            cr.set_source_rgba( 1,0.91, 0,0.9) #ffe900  1,0.91, 0
            cr.set_line_width(4.7)
            cr.arc (185/2-5, 538/2+30, 15, 0, 2*math.pi);
            cr.stroke();
            cr.set_source_rgba(0.98, 0.34, 0.07, 0.3) #f95611   0.98, 0.34, 0.07
            cr.set_line_width(5.7)
            cr.arc (185/2-5, 538/2+30, 20, 0, 2*math.pi);
            cr.fill();

            cr.set_source_rgba( 1,0.91, 0,0.9) #ffe900  1,0.91, 0
            cr.set_line_width(4.7)
            cr.arc (185/2-5, 538/2-50, 15, 0, 2*math.pi);
            cr.stroke();
            cr.set_source_rgba(0.98, 0.34, 0.07, 0.3) #f95611   0.98, 0.34, 0.07
            cr.set_line_width(5.7)
            cr.arc (185/2-5, 538/2-50, 20, 0, 2*math.pi);
            cr.fill();

 
        return False

    def add_colon (self, flg):
        self.colon = flg
        self.queue_draw()

    def set_reading (self, value):
        self.cur_value = value
        if value > 9:
            tube="nixie-c.png"
        else:
            tube="nixie-{:1d}.png".format(self.cur_value)
        if os.path.isfile(tube):
            self.nixiesurface = cairo.ImageSurface.create_from_png (tube)
        else:
            tube="nixie-{:1d}.png".format(-1)
            if os.path.isfile(tube):
                self.nixiesurface = cairo.ImageSurface.create_from_png (tube)
        
        self.queue_draw()


class NixieClock():

    def __init__(self, app):
        x=0
        
        # … create a new window…
        win = Gtk.ApplicationWindow(application=app, title='Py Nixie Clock')
        if scale < 0.4:
            win.set_decorated(False)

        win.set_opacity(opacity)
            
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        
        # … with a button in it…
        grid = Gtk.Grid()
        grid.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        win.set_child (grid)

        btn = Gtk.Button(label='Good-by Nixies!')
        # … which closes the window when clicked
        btn.connect('clicked', lambda x: win.close())

        grid.add_css_class('nxgrid')

        # Add the CSS provider to the style context
        style_context = grid.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        style_context.add_class("nxgrid")
        
        #grid.set_column_spacing(0)

        self.timelabel = Gtk.Label()
        self.timelabel.set_markup("<span font_desc='24'>00:00:00</span>")
        if scale > 0.4:
            grid.attach(self.timelabel, 1,1, 2,1)
            grid.attach(btn, 8,1, 1,1)

        self.NxH10 = NixieTube()
        grid.attach(self.NxH10, 1,3, 1,1)
        self.NxH01 = NixieTube()
        grid.attach(self.NxH01, 2,3, 1,1)

        #self.c1 = Gtk.Label()
        #self.c1.set_markup("<span font_desc='140'>:</span>")
        self.c1 = NixieTube()
        self.c1.set_reading(10)
        #self.c1.add_colon(True)
        grid.attach(self.c1, 3,3, 1,1)

        self.NxM10 = NixieTube()
        grid.attach(self.NxM10, 4,3, 1,1)
        self.NxM01 = NixieTube()
        grid.attach(self.NxM01, 5,3, 1,1)

        #self.c2 = Gtk.Label()
        #self.c2.set_markup("<span font_desc='140'>:</span>")
        self.c2 = NixieTube()
        self.c2.set_reading(10)
        #self.c2.add_colon(True)
        grid.attach(self.c2, 6,3, 1,1)

        self.NxS10 = NixieTube()
        grid.attach(self.NxS10, 7,3, 1,1)
        self.NxS01 = NixieTube()
        grid.attach(self.NxS01, 8,3, 1,1)

        
        win.present()

        # Update the time every second
        GLib.timeout_add(1000, self.update_time)

    def update_time(self):
        # Get the current time and format it
        current_time = GLib.DateTime.new_now_local()
        time_string = current_time.format("%H:%M:%S")
        c=11*(current_time.get_second()%2)-1
       
        self.NxH10.set_reading (int(current_time.get_hour()/10))
        self.NxH01.set_reading (current_time.get_hour()%10)
        self.c1.set_reading(c)
        self.NxM10.set_reading (int(current_time.get_minute()/10))
        self.NxM01.set_reading (current_time.get_minute()%10)
        self.c2.set_reading(c)
        self.NxS10.set_reading (int(current_time.get_second()/10))
        self.NxS01.set_reading (current_time.get_second()%10)
        
        # Update the label
        self.timelabel.set_markup(f"<span font_desc='24'>{time_string}</span>")

        # Return True to keep the timeout running
        return True



# When the application is launched…
def on_activate(app):
    clock =  NixieClock(app)

    
# Create a new application
app = Gtk.Application(application_id='com.example.GtkApplication')
app.connect('activate', on_activate)

# Run the application
app.run(None)
