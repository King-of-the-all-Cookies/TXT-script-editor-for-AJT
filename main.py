import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import re

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Text Editor")

        self.text_area = tk.Text(master)
        self.text_area.pack(expand=True, fill="both", side=tk.LEFT)

        self.original_text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.original_text_area.pack(expand=True, fill="both", side=tk.RIGHT)
        self.original_text_area.config(state=tk.DISABLED)

        self.save_button = tk.Button(master, text="Save File", command=self.save_file)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.pack()

        self.filename = None
        self.original_lines = []
        self.displayed_lines = []

    def save_file(self):
        if self.filename:
            new_lines = []
            displayed_text_lines = self.text_area.get("1.0", tk.END).splitlines()
            displayed_line_index = 0

            for original_line in self.original_lines:
                parts = original_line.split("<", 1)
                if len(parts) > 0 and not parts[0].startswith("<"):
                    if displayed_line_index < len(displayed_text_lines):
                        new_lines.append(displayed_text_lines[displayed_line_index] + "<" + parts[1] if len(parts) > 1 else "")
                        displayed_line_index += 1
                else:
                    new_lines.append(original_line)

            with open(self.filename, "w") as f:
                f.write("\n".join(new_lines))
        else:
            self.save_file_as()

    def save_file_as(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if self.filename:
            self.save_file()

    def load_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt")
        if self.filename:
            with open(self.filename, "r") as f:
                self.original_lines = f.read().splitlines()
                self.text_area.delete("1.0", tk.END)
                self.original_text_area.config(state=tk.NORMAL)
                self.original_text_area.delete("1.0", tk.END)
                self.original_text_area.config(state=tk.DISABLED)
                self.displayed_lines = []

                for line in self.original_lines:
                    clean_line = ""
                    inside_tag = False
                    for char in line:
                        if char == "<":
                            inside_tag = True
                        elif char == ">":
                            inside_tag = False
                        elif not inside_tag:
                            clean_line += char
                    self.text_area.insert(tk.END, clean_line.strip() + "\n")
                    self.displayed_lines.append(clean_line.strip())
                    self.original_text_area.config(state=tk.NORMAL)
                    self.original_text_area.insert(tk.END, line + "\n")
                    self.original_text_area.config(state=tk.DISABLED)

    def highlight_changes(self):
        self.original_text_area.config(state=tk.NORMAL)
        self.original_text_area.tag_remove("red", "1.0", tk.END)

        displayed_text_lines = self.text_area.get("1.0", tk.END).splitlines()
        displayed_line_index = 0

        for i, original_line in enumerate(self.original_lines):
            parts = original_line.split("<", 1)
            if len(parts) > 0 and not parts[0].startswith("<"):
                if displayed_line_index < len(displayed_text_lines):
                    if parts[0].strip() != displayed_text_lines[displayed_line_index]:
                        start_index = f"{i + 1}.0"
                        end_index = f"{i + 1}.0"
                        end_index = f"{i + 1}.{len(parts[0])}"
                        self.original_text_area.tag_add("red", start_index, end_index)
                        self.original_text_area.tag_config("red", foreground="red")
                    displayed_line_index += 1

        self.original_text_area.config(state=tk.DISABLED)

    def update_highlight(self, event=None):
        self.highlight_changes()

root = tk.Tk()
editor = TextEditor(root)
root.bind("<KeyRelease>", editor.update_highlight)
root.mainloop()
