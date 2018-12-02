from typing import List

import gi
import cairo
import life_list

# -*- coding: utf-8 -*-
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib


class MyWindow(Gtk.Window):
    L_SIZE = 20
    S_SIZE = L_SIZE / 8
    RUN = True
    STOP = False
    FPS = 500

    def __init__(self, title="lifegame"):
        Gtk.Window.__init__(self, title=title)
        self.state = self.RUN
        self.column = 20
        self.row = 20
        self.frame_rate = self.FPS
        self.dwarea = Gtk.DrawingArea()
        self.dwarea.set_size_request(640,480)
        self.l1 = Gtk.Label(label="column")
        self.l2 = Gtk.Label(label="row")
        self.e1 = Gtk.Entry()
        self.e2 = Gtk.Entry()
        self.e1.set_text(str(self.column))
        self.e2.set_text(str(self.row))
        self.button1 = Gtk.Button(label="foooo")
        self.button2 = Gtk.Button(label="start")
        self.button3 = Gtk.Button(label="stop")

        self.button1.connect("clicked", self.on_button_clicked1)
        self.button2.connect("clicked", self.on_button_clicked2)
        self.button3.connect("clicked", self.on_button_clicked3)
        self.vbox1 = Gtk.VBox()
        self.vbox2 = Gtk.VBox()
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox(spacing=6)
        self.vbox3 = Gtk.VBox()
        self.vbox4 = Gtk.VBox()
        self.adj = Gtk.Adjustment(self.frame_rate, 100, 800, 5, 10, 0)
        self.scale_bar = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment = self.adj)
        self.scale_bar.connect("value-changed", self.scale_moved)
        self.vbox1.add(self.l1)
        self.vbox1.add(self.e1)
        self.vbox2.add(self.l2)
        self.vbox2.add(self.e2)
        self.hbox1.add(self.vbox1)
        self.hbox1.add(self.vbox2)
        self.vbox3.add(self.hbox1)
        self.vbox3.add(self.button1)
        self.add(self.vbox3)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def tick(self):
        if self.state:
            self.cells.next_gen()
            self.queue_draw()
        return True

    def on_button_clicked1(self, *args):
        self.column = int(self.e1.get_text())
        self.row = int(self.e2.get_text())
        #       self.vbox3.set_visible(False)
        self.cells = life_list.Cell(self.column, self.row, )
        self.remove(self.vbox3)
        self.hbox2.add(self.button2)
        self.hbox2.add(self.button3)
        self.vbox4.add(self.dwarea)
        self.vbox4.add(self.hbox2)
        self.vbox4.add(self.scale_bar)
        self.add(self.vbox4)
        self.dwarea.connect('draw', self.draw)
        self.dwarea.set_size_request( (self.column + 2) * self.L_SIZE, (self.row + 2) * self.L_SIZE)
#        self.set_size_request(640, 480)
        self.time_id = GLib.timeout_add(self.frame_rate, self.tick)
        self.show_all()

    def on_button_clicked2(self, *args):
        self.state = self.RUN

    def on_button_clicked3(self, *args):
        self.state = self.STOP

    def scale_moved(self,*args):
        self.frame_rate = int(self.scale_bar.get_value())
        GLib.source_remove(self.time_id)
        self.time_id = GLib.timeout_add(self.frame_rate, self.tick)

    def draw(self, da, ctx):
        base_x = self.L_SIZE
        base_y = self.L_SIZE
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(self.S_SIZE)
        ctx.set_tolerance(0.1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        self.draw_map(ctx, base_x, base_y)
        self.draw_cell(ctx, base_x + self.S_SIZE / 2, base_y + self.S_SIZE / 2)

    def draw_map(self, ctx, x, y):
        for i in range(self.row):
            for j in range(self.column):
                s_x = x + j * self.L_SIZE
                s_y = y + i * self.L_SIZE
                ctx.rectangle(s_x, s_y, self.L_SIZE, self.L_SIZE)
                ctx.stroke()


    def draw_cell(self, ctx, x, y):
        for i in range(self.row):
            for j in range(self.column):
                s_x = x + j * self.L_SIZE
                s_y = y + i * self.L_SIZE
                if self.cells.dead_or_alive(j, i):
                    ctx.set_source_rgb(0, 255, 0)
                    ctx.rectangle(s_x, s_y, self.L_SIZE - self.S_SIZE, self.L_SIZE - self.S_SIZE)
                    ctx.fill()






app = MyWindow("Life_Game")

Gtk.main()
