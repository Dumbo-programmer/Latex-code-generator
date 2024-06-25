import tkinter as tk
from tkinter import scrolledtext, Canvas, Scrollbar, Frame
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from io import BytesIO

class LatexGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX Code Generator")
        self.root.configure(bg='#2e2e2e')  # Dark background

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Frame for input and buttons
        self.input_frame = Frame(root, bg='#2e2e2e')
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.input_frame.grid_columnconfigure(0, weight=1)
        for i in range(8):
            self.input_frame.grid_rowconfigure(i, weight=1)

        # Input area for LaTeX code
        self.input_area = scrolledtext.ScrolledText(self.input_frame, width=50, height=8, bg='#444444', fg='white', insertbackground='white', font=("Helvetica", 10))
        self.input_area.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')

        # Sections for buttons
        self.create_sections()

        # Button to generate LaTeX preview
        self.generate_button = tk.Button(self.input_frame, text="Generate Preview", command=self.generate_preview, bg='#555555', fg='white', activebackground='#777777', relief='flat', height=2, width=20)
        self.generate_button.grid(row=7, column=0, columnspan=6, padx=10, pady=20, sticky='nsew')

        # Frame for LaTeX preview with scrollbar
        self.preview_frame = Frame(root, bg='#2e2e2e')
        self.preview_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.canvas = Canvas(self.preview_frame, bg='#2e2e2e')
        self.scrollbar = Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg='#2e2e2e')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

    def create_sections(self):
        # Symbols section
        symbols_frame = self.create_label_frame("Symbols", 1)
        symbols = [
            ("α", "\\alpha"), ("β", "\\beta"), ("γ", "\\gamma"), ("δ", "\\delta"),
            ("√", "\\sqrt{}"), ("∫", "\\int"), ("∑", "\\sum"), ("∞", "\\infty")
        ]
        self.create_buttons(symbols_frame, symbols)

        # Trig functions section
        trig_frame = self.create_label_frame("Trig Functions", 2)
        trig_functions = [
            ("sin", "\\sin"), ("cos", "\\cos"), ("tan", "\\tan"), 
            ("csc", "\\csc"), ("sec", "\\sec"), ("cot", "\\cot"),
            ("asin", "\\arcsin"), ("acos", "\\arccos"), ("atan", "\\arctan")
        ]
        self.create_buttons(trig_frame, trig_functions)

        # Other functions section
        functions_frame = self.create_label_frame("Other Functions", 3)
        functions = [
            ("log", "\\log"), ("ln", "\\ln"), ("exp", "\\exp"),
            ("floor", "\\lfloor{}\\rfloor"), ("ceil", "\\lceil{}\\rceil")
        ]
        self.create_buttons(functions_frame, functions, special=True)

        # Numbers section
        numbers_frame = self.create_label_frame("Numbers", 4)
        numbers = [(str(i), str(i)) for i in range(10)]
        self.create_buttons(numbers_frame, numbers)

        # Other constructs section
        others_frame = self.create_label_frame("Other Constructs", 5)
        others = [
            ("a/b", "\\frac{a}{b}"), ("x²", "^{}"), ("x₁", "_{}")
        ]
        self.create_buttons(others_frame, others, special=True)

    def create_label_frame(self, text, row):
        frame = tk.LabelFrame(self.input_frame, text=text, bg='#2e2e2e', fg='white')
        frame.grid(column=0, row=row, columnspan=6, padx=10, pady=5, sticky='nsew')
        for i in range(6):
            frame.grid_columnconfigure(i, weight=1)
        return frame

    def create_buttons(self, frame, items, special=False):
        button_width = 6
        button_height = 2
        for i, (text, symbol) in enumerate(items):
            button_frame = tk.Frame(frame, bg='#2e2e2e')
            button_frame.grid(column=i % 6, row=i // 6, padx=5, pady=5, sticky='nsew')
            button = tk.Button(button_frame, text=text, command=lambda s=symbol: self.insert_symbol(s) if not special or text != "a/b" else self.insert_fraction(s), bg='#555555', fg='white', activebackground='#777777', relief='flat', width=button_width, height=button_height)
            if special and ("floor" in text or "ceil" in text):
                button.configure(command=lambda s=symbol: self.insert_floor_ceil(s))
            button.pack(fill='both', expand=True, padx=5, pady=5)

    def insert_symbol(self, symbol):
        pos = self.input_area.index(tk.INSERT)
        if "{}" in symbol:
            self.input_area.insert(pos, symbol)
            self.input_area.mark_set(tk.INSERT, f"{pos}+{len(symbol) - 1}c")
        else:
            self.input_area.insert(tk.INSERT, symbol)

    def insert_fraction(self, symbol):
        pos = self.input_area.index(tk.INSERT)
        self.input_area.insert(pos, symbol)
        self.input_area.mark_set(tk.INSERT, f"{pos}+6c")

    def insert_floor_ceil(self, symbol):
        pos = self.input_area.index(tk.INSERT)
        self.input_area.insert(pos, symbol)
        self.input_area.mark_set(tk.INSERT, f"{pos}+7c")

    def generate_preview(self):
        latex_code = self.input_area.get("1.0", tk.END)
        # Encapsulate each line with $$ for multiline display
        lines = latex_code.splitlines()
        latex_code = "\n".join([f"${line.strip()}$" for line in lines])
        self.render_latex(latex_code)

    def render_latex(self, latex_code):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"{latex_code.strip()}", horizontalalignment='center', verticalalignment='center', fontsize=20)
        ax.axis('off')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        img = ImageTk.PhotoImage(img)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        preview_label = tk.Label(self.scrollable_frame, image=img, bg='#2e2e2e')
        preview_label.image = img
        preview_label.pack()

        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = LatexGenerator(root)
    root.mainloop()
