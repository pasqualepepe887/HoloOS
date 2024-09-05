import tkinter as tk
import os

class FileDialog(tk.Frame):
    def __init__(self, parent, extension, export_path, on_export_path_change):
        super().__init__(parent)
        self.extension = extension
        self.export_path = export_path
        self.on_export_path_change = on_export_path_change  # Aggiungi il callback
        self.current_path = os.path.expanduser("~")
        
        self.folder_entry = tk.Entry(self, bg="black", fg="white")
        self.folder_entry.pack(fill="x")
        self.folder_entry.insert(0, self.current_path)
        self.folder_entry.bind("<KeyRelease>", self.on_entry_change)
        
        self.file_listbox = tk.Listbox(self, width=50, height=15, bg="black", fg="white")
        self.file_listbox.pack(fill="both", expand=True)
        self.file_listbox.bind("<Double-1>", self.on_item_double_click)
        
        self.selected_file_label = tk.Label(self, text="No file selected", anchor="w", bg="black", fg="white", bd=5)
        self.selected_file_label.pack(fill="x")
        
        self.update_file_list(self.current_path)

    def on_entry_change(self, event):
        self.update_file_list(self.folder_entry.get())
        
    def update_file_list(self, path=None):
        if path is None:
            path = self.folder_entry.get()
        
        if os.path.isdir(path):
            self.current_path = path
            
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, path)
            
            self.file_listbox.delete(0, tk.END)
            self.file_listbox.insert(tk.END, "..")  
            
            items = os.listdir(path)
            items.sort()  # Sort items alphabetically
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    self.file_listbox.insert(tk.END, item)
                elif item.lower().endswith(self.extension):
                    self.file_listbox.insert(tk.END, item)
        else:
            print(f"Invalid directory: {path}")
    
    def on_item_double_click(self, event):
        try:
            selected_item_index = self.file_listbox.curselection()[0]
            selected_item = self.file_listbox.get(selected_item_index)
            print(f"Selected: {selected_item}")
            if selected_item == "..":
                parent_path = os.path.dirname(self.current_path)
                self.update_file_list(parent_path)
                self.current_path = parent_path
            else:
                selected_path = os.path.join(self.current_path, selected_item)
                if os.path.isdir(selected_path):
                    self.update_file_list(selected_path)
                    self.current_path = selected_path
                else:
                    self.selected_file_label.config(text=selected_path)
                    self.export_path = selected_path
                    self.on_export_path_change(selected_path)  # Chiama il callback
        except IndexError:
            # No item selected, ignore double-click
            print("No item selected")
            pass
