# main_rbr.py
# Chris Shepherd, Codethink Ltd, 2021-01-18

import os
import tkinter as tk
from tkinter import filedialog, messagebox

import rbrDatabase


# ------------------------------------------------------------------------------
# GUI which runs recursive scanning of folders, creation of .xml database
class gui:
    def choose_folder(self, message):
        return filedialog.askdirectory(title=message)

    # ------------------------------------------------------------------------------

    def folders_in_out(self):
        in_out = ["", ""]
        root_folder = self.choose_folder("Select root folder for your music")
        if root_folder:
            if os.path.isdir(root_folder):
                in_out[0] = root_folder
                out_folder = self.choose_folder("Select location for XML output")
                if out_folder:
                    if os.path.isdir(out_folder):
                        in_out[1] = out_folder
                    else:
                        messagebox.showinfo("Warning", "Path doesn't exist, exiting")
            else:
                messagebox.showinfo("Warning", "Path doesn't exist, exiting")
        return in_out

    # ------------------------------------------------------------------------------

    def create_db_and_print(
        self, file_name_user, root_folder, out_folder, show_warning
    ):
        db_main = rbrDatabase.rbrDatabase()
        db_main.add_recursively(root_folder, show_warning)
        if file_name_user == "":
            file_name_user = "rbr_db"
        out_file = os.path.join(out_folder, file_name_user) + ".xml"
        db_main.write_pretty(out_file)
        messagebox.showinfo("info", "Done! Database file : " + out_file)

    # ------------------------------------------------------------------------------

    def run(self, entry_db_name, show_warning):
        file_name_user = entry_db_name.get()
        in_out = self.folders_in_out()
        if in_out[0] and in_out[1]:
            self.create_db_and_print(file_name_user, in_out[0], in_out[1], show_warning)

    # ------------------------------------------------------------------------------

    def __init__(self):

        # Create the GUI: buttons activate browsers for collection / output .xml folder
        self.root_tk = tk.Tk()
        self.root_tk.title("Rekordbox Recovery Tool")

        self.root_folder = ""

        info_message = "Rekordbox Recovery Tool, Chris Shepherd, 2022\n"
        info = tk.Label(self.root_tk, text=info_message)
        info.pack()

        instructions = tk.Label(
            self.root_tk,
            text=(
                "Enter name for output database, e.g. entering 'foo' creates 'foo.xml'. \
                        If left blank, will be named 'rbr_db.xml'"
            ),
        )
        instructions.pack()

        # Text entry for database name
        self.entry_db_name = tk.Entry(self.root_tk, width=20)
        self.entry_db_name.pack()

        # Checkbox for warning messages
        self.show_warning = tk.IntVar()
        check_warn = tk.Checkbutton(
            self.root_tk,
            text="Print compatibility warnings to console",
            variable=self.show_warning,
        )
        check_warn.pack()

        # "Run" button
        run_text = tk.StringVar()
        run_text.set("RUN")
        run_button = tk.Button(
            self.root_tk,
            textvariable=run_text,
            command=lambda: self.run(self.entry_db_name, self.show_warning.get()),
        )
        run_button.pack()

        # "Close" button
        close_text = tk.StringVar()
        close_text.set("Close")
        close_button = tk.Button(
            self.root_tk,
            textvariable=close_text,
            command=lambda: self.root_tk.destroy(),
        )
        close_button.pack()

        self.root_tk.mainloop()


my_gui = gui()
