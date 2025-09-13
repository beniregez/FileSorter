import os
import shutil
from tkinter import Tk, filedialog, Button, Label, Listbox, END, Frame, Entry, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime

class FileSorterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("FileSorter")
        self.geometry("600x550")

        self.label = Label(self, text="Drag & Drop files here or choose a directory")
        self.label.pack(pady=20)

        self.listbox = Listbox(self, width=80, height=10)
        self.listbox.pack(pady=10)

        # Source dirctory with label and button
        self.input_folder_var = StringVar()
        input_frame = Frame(self)
        input_frame.pack(pady=5)
        self.input_entry = Entry(input_frame, textvariable=self.input_folder_var, width=50)
        self.input_entry.pack(side="left", padx=10)
        self.select_button = Button(input_frame, text="Choose source directory", command=self.select_folder)
        self.select_button.pack(side="left")

        # Output directory with label and button
        self.output_folder_var = StringVar()
        output_frame = Frame(self)
        output_frame.pack(pady=5)
        self.output_entry = Entry(output_frame, textvariable=self.output_folder_var, width=50)
        self.output_entry.pack(side="left", padx=10)
        self.output_button = Button(output_frame, text="Choose output directory", command=self.select_output_folder)
        self.output_button.pack(side="left")

        # Buttons for sorting mode
        self.sort_by = 'created'  # Default to sort by creation date
        self.button_frame = Frame(self)
        self.button_frame.pack(pady=10)

        self.created_button = Button(self.button_frame, text="By date of creation", command=lambda: self.set_sort_method('created'))
        self.created_button.pack(side="left", padx=5)
        self.modified_button = Button(self.button_frame, text="By date of change", command=lambda: self.set_sort_method('modified'))
        self.modified_button.pack(side="left", padx=5)
        self.update_button_highlight()

        # Dateien sortieren Button
        self.process_button = Button(self, text="Sort files", command=self.sort_files, bg="darkblue", fg="white")
        self.process_button.pack(pady=10)

        # Weitere Dateien sortieren Button
        self.reset_button = Button(self, text="Sort more files", command=self.reset_program)
        self.reset_button.pack(pady=10)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop)
        
        self.files = []
        self.output_folder = None

    def drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file):
                self.files.append(file)
                self.listbox.insert(END, file)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_var.set(folder)
            for root, _, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    self.files.append(filepath)
                    self.listbox.insert(END, filepath)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Choose output directory")
        if folder:
            self.output_folder_var.set(folder)
            self.output_folder = folder

    def set_sort_method(self, method):
        self.sort_by = method
        self.update_button_highlight()

    def update_button_highlight(self):
        if self.sort_by == 'created':
            self.created_button.config(relief="solid", bd=2)
            self.modified_button.config(relief="flat")
        else:
            self.modified_button.config(relief="solid", bd=2)
            self.created_button.config(relief="flat")

    def sort_files(self):
        if not self.files:
            self.label.config(text="Keine Dateien zum Sortieren")
            return

        if not self.output_folder:
            self.label.config(text="No output directory selected")
            return

        for file in self.files:
            try:
                if self.sort_by == 'created':
                    time = os.path.getctime(file)
                else:
                    time = os.path.getmtime(file)
                
                date = datetime.fromtimestamp(time)
                month_folder = os.path.join(self.output_folder, date.strftime("%Y-%m"))
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder, exist_ok=True)
                target_path = os.path.join(month_folder, os.path.basename(file))
                if not os.path.exists(target_path):
                    shutil.copy2(file, month_folder)
            except Exception as e:
                print(f"Error processing {file}: {e}")
        
        self.label.config(text="Files sorted successfully!")

    def reset_program(self):
        self.files.clear()
        self.listbox.delete(0, END)
        self.label.config(text="Drag files here or select a folder")

if __name__ == "__main__":
    app = FileSorterApp()
    app.mainloop()
