import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as tkfont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import BBCodeFormatter

class LineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index(f"{i}+1line")

class CodeArtifactDisplay(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.line_numbers = LineNumbers(self, width=30)
        self.line_numbers.grid(row=0, column=0, sticky="nsew")

        self.code_display = tk.Text(self, wrap=tk.NONE, font=("Consolas", 10))
        self.code_display.grid(row=0, column=1, sticky="nsew")

        self.code_display.bind("<KeyRelease>", self.on_key_release)
        self.code_display.bind("<ButtonRelease>", self.on_key_release)

        self.line_numbers.attach(self.code_display)

        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.code_display.yview)
        scrollbar_y.grid(row=0, column=2, sticky="ns")
        self.code_display.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.code_display.xview)
        scrollbar_x.grid(row=1, column=1, sticky="ew")
        self.code_display.configure(xscrollcommand=scrollbar_x.set)

    def on_key_release(self, event):
        self.line_numbers.redraw()

    def set_content(self, content, content_type):
        self.code_display.delete(1.0, tk.END)
        if content_type == "code":
            self.apply_syntax_highlighting(content)
        else:
            self.code_display.insert(tk.END, content)
        self.line_numbers.redraw()

    def apply_syntax_highlighting(self, code):
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = BBCodeFormatter(style='monokai')
        highlighted_code = highlight(code, lexer, formatter)

        self.code_display.tag_configure("bold", font=("Consolas", 10, "bold"))
        self.code_display.tag_configure("italic", font=("Consolas", 10, "italic"))
        self.code_display.tag_configure("keyword", foreground="#66D9EF")
        self.code_display.tag_configure("string", foreground="#E6DB74")
        self.code_display.tag_configure("comment", foreground="#75715E")
        self.code_display.tag_configure("function", foreground="#A6E22E")

        for line in highlighted_code.split('\n'):
            for segment in line.split('['):
                if ']' in segment:
                    style, text = segment.split(']', 1)
                    if 'b' in style:
                        self.code_display.insert(tk.END, text, "bold")
                    elif 'i' in style:
                        self.code_display.insert(tk.END, text, "italic")
                    elif 'color="#66D9EF"' in style:
                        self.code_display.insert(tk.END, text, "keyword")
                    elif 'color="#E6DB74"' in style:
                        self.code_display.insert(tk.END, text, "string")
                    elif 'color="#75715E"' in style:
                        self.code_display.insert(tk.END, text, "comment")
                    elif 'color="#A6E22E"' in style:
                        self.code_display.insert(tk.END, text, "function")
                    else:
                        self.code_display.insert(tk.END, text)
                else:
                    self.code_display.insert(tk.END, segment)
            self.code_display.insert(tk.END, '\n')

class ArtifactWindow(ThemedTk):
    def __init__(self, parent, title, content, content_type):
        super().__init__(theme="equilux")
        self.title(title)
        self.geometry("800x600")
        
        self.parent = parent
        self.content = content
        self.content_type = content_type
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_header(main_frame)
        self.create_content_display(main_frame)
        self.create_button_area(main_frame)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="Generated Code Artifact", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        ttk.Label(header_frame, text=f"Type: {self.content_type}", font=("Helvetica", 12)).pack(side=tk.RIGHT)

    def create_content_display(self, parent):
        self.code_artifact_display = CodeArtifactDisplay(parent)
        self.code_artifact_display.pack(fill=tk.BOTH, expand=True)
        self.code_artifact_display.set_content(self.content, self.content_type)

    def create_button_area(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        copy_button = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT)

        close_button = ttk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.RIGHT)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.content)
        self.update()

        copy_label = ttk.Label(self, text="Copied to clipboard!", foreground="green")
        copy_label.pack(pady=5)
        self.after(2000, copy_label.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    artifact_window = ArtifactWindow(root, "Code Artifact", "", "code")
    artifact_window.mainloop()