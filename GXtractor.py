import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from tkinterdnd2 import TkinterDnD, DND_ALL

class FileExtractorApp:
    def __init__(self, root):
        self.root = root
        if not isinstance(root, TkinterDnD.Tk):
            messagebox.showwarning("DND Root Issue", "Replacing Tkinter root with TkinterDnD.Tk for drag and drop functionality.")
            self.root = TkinterDnD.Tk()
            self.root.title("GXtractor (Use to copy file out from multiple folder and put them all in 1) MADE BY NHoangLong69 on Github")
            self.root.geometry("800x750")
            self.root.resizable(True, True)
            self.root.configure(bg="#f0f0f0")
        else:
            self.root.title("GXtractor (Use to copy file out from multiple folder and put them all in 1) MADE BY NHoangLong69 on Github")
            self.root.geometry("800x750")
            self.root.resizable(True, True)
            self.root.configure(bg="#f0f0f0")

        try:
            icon_path = "C:/Users/Sapling/Downloads/logo.png"
            self.icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, self.icon_image)
        except tk.TclError:
            messagebox.showwarning("Icon Warning", f"Could not load icon from '{icon_path}'. Please ensure the file exists at this exact path.")

        self.selected_items = []
        self.output_directory = ""

        self.item_selection_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
        self.item_selection_frame.pack(pady=15, padx=20, fill="x")

        self.instruction_label = tk.Label(self.item_selection_frame,
                                           text="Select source folders or drag and drop them below:",
                                           font=("Inter", 10, "bold"),
                                           bg="#f0f0f0", fg="#333333")
        self.instruction_label.pack(pady=10, padx=10)

        self.add_folder_contents_button = tk.Button(self.item_selection_frame,
                                                     text="Select Source Folder",
                                                     command=self.add_folder_contents,
                                                     font=("Inter", 10, "bold"),
                                                     bg="#4CAF50", fg="white",
                                                     activebackground="#45a049",
                                                     activeforeground="white",
                                                     cursor="hand2",
                                                     relief="raised",
                                                     bd=3,
                                                     padx=10,
                                                     pady=5)
        self.add_folder_contents_button.pack(pady=5)

        self.dnd_frame = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief="solid")
        self.dnd_frame.pack(pady=10, padx=20, fill="x", ipady=20)

        self.dnd_label = tk.Label(self.dnd_frame,
                                       text="Drag & Drop multiple folders here",
                                       font=("Inter", 10, "italic"),
                                       bg="#e0e0e0", fg="#666666")
        self.dnd_label.pack(expand=True)

        self.dnd_frame.drop_target_register(DND_ALL)
        self.dnd_frame.dnd_bind('<<Drop>>', self.handle_dnd_drop)
        self.dnd_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.dnd_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)

        self.list_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.list_label = tk.Label(self.list_frame,
                                        text="Selected Folders for Extraction:",
                                        font=("Inter", 9, "bold"),
                                        bg="#f0f0f0", fg="#333333")
        self.list_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.item_listbox = tk.Listbox(self.list_frame,
                                        height=8,
                                        font=("Inter", 9),
                                        bg="white", fg="#333333",
                                        selectbackground="#a6d9ff",
                                        selectforeground="black",
                                        bd=1,
                                        relief="solid")
        self.item_listbox.pack(pady=5, padx=10, fill="both", expand=True)

        self.list_scrollbar = tk.Scrollbar(self.item_listbox, orient="vertical", command=self.item_listbox.yview)
        self.list_scrollbar.pack(side="right", fill="y")
        self.item_listbox.config(yscrollcommand=self.list_scrollbar.set)

        self.clear_button = tk.Button(self.list_frame,
                                           text="Clear Selected Items",
                                           command=self.clear_items,
                                           font=("Inter", 9),
                                           bg="#f44336", fg="white",
                                           activebackground="#d32f2f",
                                           activeforeground="white",
                                           cursor="hand2",
                                           relief="raised",
                                           bd=2,
                                           padx=8,
                                           pady=3)
        self.clear_button.pack(pady=5, padx=10, anchor="e")

        self.output_dir_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
        self.output_dir_frame.pack(pady=15, padx=20, fill="x")

        self.output_dir_label_text = tk.Label(self.output_dir_frame,
                                                   text="Destination Directory:",
                                                   font=("Inter", 10, "bold"),
                                                   bg="#f0f0f0", fg="#333333")
        self.output_dir_label_text.pack(pady=(10, 5), padx=10, anchor="w")

        self.output_dir_display = tk.Label(self.output_dir_frame,
                                                text="Not selected",
                                                font=("Inter", 9, "italic"),
                                                bg="#f0f0f0", fg="#555555",
                                                wraplength=550,
                                                justify="left",
                                                relief="sunken",
                                                bd=1,
                                                padx=5,
                                                pady=3)
        self.output_dir_display.pack(pady=(0, 5), padx=10, fill="x")

        self.select_output_button = tk.Button(self.output_dir_frame,
                                              text="Choose Destination Directory",
                                              command=self.select_output_directory,
                                              font=("Inter", 10, "bold"),
                                              bg="#FFC107", fg="#333333",
                                              activebackground="#FFA000",
                                              activeforeground="#333333",
                                              cursor="hand2",
                                              relief="raised",
                                              bd=3,
                                              padx=10,
                                              pady=5)
        self.select_output_button.pack(pady=5)

        self.extract_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
        self.extract_frame.pack(pady=15, padx=20, fill="x")

        self.extract_button = tk.Button(self.extract_frame,
                                         text="Extract All Files to Destination",
                                         command=self.extract_files,
                                         font=("Inter", 11, "bold"),
                                         bg="#2196F3", fg="white",
                                         activebackground="#1976D2",
                                         activeforeground="white",
                                         cursor="hand2",
                                         relief="raised",
                                         bd=4,
                                         padx=15,
                                         pady=8)
        self.extract_button.pack(pady=10)

        self.status_label = tk.Label(self.root,
                                           text="",
                                           font=("Inter", 9, "italic"),
                                           bg="#f0f0f0", fg="#555555")
        self.status_label.pack(pady=10)

    def on_drag_enter(self, event):
        self.dnd_frame.config(bg="#c0c0c0")
        return 'copy'

    def on_drag_leave(self, event):
        self.dnd_frame.config(bg="#e0e0e0")
        return 'copy'

    def handle_dnd_drop(self, event):
        self.dnd_frame.config(bg="#e0e0e0")

        dropped_paths_raw = self.root.tk.splitlist(event.data)

        for path in dropped_paths_raw:
            cleaned_path = os.path.normpath(path)

            if os.path.isdir(cleaned_path):
                if cleaned_path not in self.selected_items:
                    self.selected_items.append(cleaned_path)
                    self.item_listbox.insert(tk.END, f"[FOLDER] {cleaned_path}")
                    self.status_label.config(text=f"Added source folder: {cleaned_path}")
                else:
                    self.status_label.config(text=f"Folder already added: {cleaned_path}")
            else:
                messagebox.showwarning("Invalid Drop", f"Only folders can be dropped here. '{os.path.basename(cleaned_path)}' is not a folder.")
                self.status_label.config(text=f"Skipped non-folder item: {os.path.basename(cleaned_path)}")

    def add_folder_contents(self):
        folder_path = filedialog.askdirectory(title="Select Source Folder to Extract Contents From")
        if folder_path:
            if folder_path not in self.selected_items:
                self.selected_items.append(folder_path)
                self.item_listbox.insert(tk.END, f"[FOLDER] {folder_path}")
                self.status_label.config(text=f"Added source folder: {folder_path}")
            else:
                self.status_label.config(text="Folder already added.")
        else:
            self.status_label.config(text="No folder selected.")

    def clear_items(self):
        self.selected_items = []
        self.item_listbox.delete(0, tk.END)
        self.status_label.config(text="Selected items cleared.")

    def select_output_directory(self):
        output_path = filedialog.askdirectory(title="Select Destination Directory")
        if output_path:
            self.output_directory = output_path
            self.output_dir_display.config(text=self.output_directory, fg="#000000")
            self.status_label.config(text=f"Destination set to: {self.output_directory}")
        else:
            self.status_label.config(text="Not selected", fg="#555555")
            self.output_directory = ""
            self.status_label.config(text="No destination directory selected.")

    def extract_files(self):
        if not self.selected_items:
            messagebox.showwarning("No Items Selected", "Please add at least one folder before extracting.")
            return

        if not self.output_directory:
            messagebox.showwarning("No Destination Selected", "Please select a destination directory.")
            return

        self.status_label.config(text="Starting extraction...", fg="#007BFF")
        self.root.update_idletasks()

        total_extracted = 0
        error_count = 0
        conflicts_resolved = 0

        for item_path in self.selected_items:
            actual_item_path = item_path.replace("[FOLDER] ", "")

            if not os.path.isdir(actual_item_path):
                messagebox.showerror("Invalid Path", f"Source is not a valid folder or does not exist: {actual_item_path}")
                error_count += 1
                continue

            for root_dir, _, files in os.walk(actual_item_path):
                for file_name in files:
                    source_file_path = os.path.join(root_dir, file_name)
                    dest_file_path = os.path.join(self.output_directory, file_name)

                    try:
                        base_name, extension = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(dest_file_path):
                            dest_file_path = os.path.join(
                                self.output_directory, f"{base_name}_{counter}{extension}"
                            )
                            counter += 1
                            conflicts_resolved += 1

                        shutil.copy2(source_file_path, dest_file_path)
                        total_extracted += 1

                    except Exception as e:
                        error_count += 1
                        print(f"Error copying {source_file_path}: {e}")

        if total_extracted > 0:
            final_message = f"Extraction complete! {total_extracted} file(s) extracted to {self.output_directory}."
            if conflicts_resolved > 0:
                final_message += f" ({conflicts_resolved} filename conflicts resolved)."
            if error_count > 0:
                final_message += f" {error_count} error(s) occurred."
            messagebox.showinfo("Extraction Complete", final_message)
            self.status_label.config(text=final_message, fg="#28a745")
        elif error_count > 0:
            final_message = f"Extraction finished with {error_count} error(s). No new files extracted."
            messagebox.showerror("Extraction Finished with Errors", final_message)
            self.status_label.config(text=final_message, fg="red")
        else:
            final_message = "No files found to extract from the selected items."
            messagebox.showinfo("Extraction Complete", final_message)
            self.status_label.config(text=final_message, fg="#555555")

if __name__ == "__main__":
    app_root = TkinterDnD.Tk()
    file_extractor = FileExtractorApp(app_root)
    app_root.mainloop()