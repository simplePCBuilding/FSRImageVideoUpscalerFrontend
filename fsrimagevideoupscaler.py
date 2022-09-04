###########################################################
#
# FSRImageVideoUpscalerFrontend written in GTK+
#
# This code is licensed under the GPL V3 License!
# Developed 2022 by Janis Hutz
#
###########################################################

import gi
import bin.handler
import multiprocessing

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


handler = bin.handler.Handler()


class HomeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test")
        self.filechooserdialog = Gtk.FileChooserDialog(title="Choose input file", action=Gtk.FileChooserAction.OPEN)
        self.filechooserdialog_save = Gtk.FileChooserDialog(title="Choose output file", action=Gtk.FileChooserAction.SAVE)

        # Spawn box
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        # Create filechooser button
        self.filechoosebutton = Gtk.Button(label="Choose Input File")
        self.filechoosebutton.connect("clicked", self.filechooser_clicked)
        self.box.pack_start(self.filechoosebutton, True, True, 10)

        # Create output filechooser button
        self.opfchooserbutton = Gtk.Button(label="Choose Output File")
        self.opfchooserbutton.connect("clicked", self.opfilechooser_clicked)
        self.box.pack_start(self.opfchooserbutton, True, True, 10)

        # Create start button
        self.start_button = Gtk.Button(label="Start upscaling")
        self.start_button.connect("clicked", self.start_clicked)
        self.box.pack_start(self.start_button, True, True, 10)

    def filechooser_clicked(self, widget):
        self.filechooserdialog = Gtk.FileChooserDialog(title="Choose input file", action=Gtk.FileChooserAction.OPEN)
        self.filechooserdialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.response = self.filechooserdialog.run()
        if self.response == Gtk.ResponseType.OK:
            print("ok, selected file:", self.filechooserdialog.get_filename())
        elif self.response == Gtk.ResponseType.CANCEL:
            print("cancel")
        self.filechooserdialog.destroy()

    def opfilechooser_clicked(self, widget):
        self.filechooserdialog_save = Gtk.FileChooserDialog(title="Choose output file", action=Gtk.FileChooserAction.SAVE)
        Gtk.FileChooser.set_do_overwrite_confirmation(self.filechooserdialog_save, True)
        Gtk.FileChooser.set_filename(self.filechooserdialog_save, "Test")
        self.filechooserdialog_save.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        self.response = self.filechooserdialog_save.run()
        if self.response == Gtk.ResponseType.OK:
            print("ok, selected file:", self.filechooserdialog_save.get_filename())
        elif self.response == Gtk.ResponseType.CANCEL:
            print("cancel")
        self.filechooserdialog_save.destroy()

    def start_clicked(self, widget):
        print(str(Gtk.FileChooser.get_filename(self.filechooserdialog)))
        if str(Gtk.FileChooser.get_filename(self.filechooserdialog)) != "" and str(Gtk.FileChooser.get_filename(self.filechooserdialog_save)) != "":
            self.scaler = multiprocessing.Process(name="scaler",
                                                  target=handler.handler,
                                                  args=("./bin/lib/FidelityFX_CLI.exe",
                                                        "/mnt/storage/SORTED/Videos/OBS_Rec/Behalten/2019-12-19 18-21-36.mp4",
                                                        "default",
                                                        "Quality",
                                                        "./test.mp4",
                                                        "./bin/lib/ffmpeg.exe")
                                                  )
            self.scaler.start()
        else:
            print("no file specified")


win = HomeWindow()
win.set_default_size(800, 600)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()