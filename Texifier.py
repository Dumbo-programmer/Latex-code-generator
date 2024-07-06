import tkinter as tk
from tkinter import ttk, scrolledtext, Canvas, Scrollbar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk
import subprocess
from pdf2image import convert_from_path
import os

class LatexGenerator:
    def __init__(self, root):
        """
        Initialize the LaTeX Code Generator application.
        """
        self.root = root
        self.root.title("LaTeX Code Generator")
        self.configure_styles()
        self.root.configure(bg="black")

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=0)  # Input area
        self.root.grid_rowconfigure(1, weight=1)  # Tabs
        self.root.grid_rowconfigure(2, weight=0)  # Generate button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Input area for LaTeX code
        self.input_area = scrolledtext.ScrolledText(self.root, width=50, height=8, bg='#444444', fg='white', insertbackground='white', font=("Helvetica", 10))
        self.input_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Button to save LaTeX code as .tex file
        self.save_button = ttk.Button(self.root, text="Save .tex", command=self.save_tex_file)
        self.save_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Tab 1: Objects
        self.objects_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.objects_tab, text='Objects')

        # Tab 2: Math
        self.math_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.math_tab, text='Math')

        # Initialize content for both tabs
        self.create_objects_tab()
        self.create_math_tab()

        # Button to generate LaTeX preview
        self.generate_button = ttk.Button(self.root, text="Generate Preview", command=self.generate_preview)
        self.generate_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        # Frame for LaTeX preview with scrollbar
        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.canvas = Canvas(self.preview_frame, bg='#444444')
        self.scrollbar = Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

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

    def configure_styles(self):
        """
        Configure the styles for the application.
        """
        style = ttk.Style()

        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")
        style.configure("TButton",
                        foreground="#11FFE3",
                        background="#3700B3",
                        borderwidth=1,
                        focuscolor="none")
        style.map("TButton",
                  background=[("active", "#6200EE")])

        style.configure("TFrame", background="black")
        style.configure("TLabel", foreground="#11FFE3", background="#121212")
        style.configure("TNotebook", background="#121212", foreground="#11FFE3", borderwidth=0)
        style.configure("TNotebook.Tab", background="#121212", foreground="#11FFE3", lightcolor="#121212", borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", "#3700B3")],
                  foreground=[("selected", "#11FFE3")])

    def create_objects_tab(self):
        """
        Create content for the Objects tab.
        """
        # Frame for input and buttons (Objects tab)
        self.objects_frame = ttk.Frame(self.objects_tab)
        self.objects_frame.pack(fill='both', expand=True)

        # Placeholder for object-specific buttons (e.g., images)
        objects_frame = self.create_label_frame("Objects", self.objects_frame)
        objects = [
            ("Image", "\\includegraphics[width=\\linewidth]{image.png}"),
            ("Table", "\\begin{tabular}{|c|c|}\n\\hline\nCell1 & Cell2 \\\\\n\\hline\nCell3 & Cell4 \\\\\n\\hline\n\\end{tabular}"),
        ]
        self.create_buttons(objects_frame, objects)

    def create_math_tab(self):
        """
        Create content for the Math tab.
        """
        # Create a canvas and scrollbars for the math tab
        canvas = Canvas(self.math_tab)
        v_scrollbar = Scrollbar(self.math_tab, orient="vertical", command=canvas.yview)
        h_scrollbar = Scrollbar(self.math_tab, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Create sections for math buttons within the scrollable frame
        self.create_sections(scrollable_frame)

    def create_sections(self, parent_frame):
        """
        Create sections for various math buttons.
        """
        # Symbols section
        symbols_frame = self.create_label_frame("Symbols", parent_frame)
        symbols = [
            ("α", "\\alpha"), ("β", "\\beta"), ("γ", "\\gamma"), ("δ", "\\delta"),
            ("ε", "\\epsilon"), ("η", "\\eta"), ("Δ", "\\Delta"), ("θ", "\\theta"),
            ("λ", "\\Lambda"), ("π", "\\pi"), ("Π", "\\Pi"), ("φ", "\\phi"),
            ("√", "\\sqrt{}"), ("∫", "\\int"), ("∮", "\\oint"), ("∬", "\\iint"),
            ("∑", "\\sum"), ("∞", "\\infty"), ("x", "x")
        ]
        self.create_buttons(symbols_frame, symbols)

        # Trig functions section
        trig_frame = self.create_label_frame("Trig Functions", parent_frame)
        trig_functions = [
            ("sin", "\\sin"), ("cos", "\\cos"), ("tan", "\\tan"), 
            ("csc", "\\csc"), ("sec", "\\sec"), ("cot", "\\cot"),
            ("asin", "\\arcsin"), ("acos", "\\arccos"), ("atan", "\\arctan")
        ]
        self.create_buttons(trig_frame, trig_functions)

        # Other functions section
        functions_frame = self.create_label_frame("Other Functions", parent_frame)
        functions = [
            ("log", "\\log"), ("ln", "\\ln"), ("exp", "\\exp"),
            ("floor", "\\lfloor{}\\rfloor"), ("ceil", "\\lceil{}\\rceil")
        ]
        self.create_buttons(functions_frame, functions, special=True)

        # Binary operations section
        binary_ops_frame = self.create_label_frame("Binary Operations", parent_frame)
        binary_ops = [
            ("+", "+"), ("-", "-"), ("*", "*"), ("/", "/"), ("⋅", "\\cdot"),
            ("×", "\\times"), ("÷", "\\div"), ("±", "\\pm"), ("∓", "\\mp")
        ]
        self.create_buttons(binary_ops_frame, binary_ops)

        # Relation symbols section
        relation_symbols_frame = self.create_label_frame("Relation Symbols", parent_frame)
        relation_symbols = [
            ("=", "="), ("≠", "\\neq"), ("<", "<"), (">", ">"), ("≤", "\\leq"), ("≥", "\\geq"),
            ("≈", "\\approx"), ("≡", "\\equiv"), ("∼", "\\sim")
        ]
        self.create_buttons(relation_symbols_frame, relation_symbols)

        # Numbers section
        numbers_frame = self.create_label_frame("Numbers", parent_frame)
        numbers = [(str(i), str(i)) for i in range(10)]
        self.create_buttons(numbers_frame, numbers)

        # LaTeX constructs section
        constructs_frame = self.create_label_frame("Math Constructs", parent_frame)
        constructs = [
            ("a/b", "\\frac{a}{b}"), ("x²", "^{2}"), ("x₁", "_{1}"),
            ("binom", "\\binom{}{}"), ("matrix", "\\begin{pmatrix}\n \\end{pmatrix}"),
            ("aligned", "\\begin{aligned}\n \\end{aligned}")
        ]
        self.create_buttons(constructs_frame, constructs, special=True)

    def create_label_frame(self, label_text, parent_frame):
        """
        Create a labeled frame for organizing buttons.
        """
        label_frame = ttk.LabelFrame(parent_frame, text=label_text)
        label_frame.pack(fill='x', expand=True, padx=5, pady=5)
        return label_frame

    def create_buttons(self, frame, symbols, special=False):
        """
        Create buttons for LaTeX symbols and constructs.
        """
        for i, (text, symbol) in enumerate(symbols):
            button = ttk.Button(frame, text=text, command=lambda s=symbol: self.insert_symbol(s) if not special else self.insert_special(s))
            button.grid(column=i % 6, row=i // 6, padx=5, pady=5)

    def insert_symbol(self, symbol):
        """
        Insert a LaTeX symbol at the current cursor position in the input area.
        """
        self.input_area.insert(tk.INSERT, symbol)

    def insert_special(self, symbol):
        """
        Insert a special LaTeX construct at the current cursor position in the input area.
        """
        self.input_area.insert(tk.INSERT, symbol + "{}")
        self.input_area.mark_set("insert", "{}".format(len(symbol) + 1))

    def save_tex_file(self):
        """
        Save the current LaTeX input as a .tex file in a directory.
        """
        latex_code = self.input_area.get("1.0", tk.END).strip()

        if not latex_code:
            messagebox.showwarning("Empty Input", "Please enter some LaTeX code.")
            return

        try:
            # Ask user for directory to save the file
            filename = tk.filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("TeX files", "*.tex")])
            if filename:
                with open(filename, 'w') as f:
                    f.write(latex_code)
                messagebox.showinfo("File Saved", f"LaTeX code saved successfully as {filename}")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("File Save Error", "Failed to save LaTeX code.")

    def generate_preview(self):
        """
        Generate and display the preview of the LaTeX code.
        """
        latex_code = self.input_area.get("1.0", tk.END).strip()
        
        if not latex_code:
            messagebox.showwarning("Empty Input", "Please enter some LaTeX code.")
            return
        
        # Encapsulate each line with $$ for multiline display
        lines = latex_code.splitlines()
        wrapped_lines = [f"${line.strip()}$" for line in lines]
        wrapped_latex_code = "\n".join(wrapped_lines)

        try:
            self.render_latex(wrapped_latex_code)
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Rendering Error", "Failed to render LaTeX code.")

    def render_latex(self, latex_code):
        """
        Render LaTeX code and display it as an image.
        """
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Check if the code contains a table environment
        if latex_code.strip().startswith("\\begin{tabular}") and latex_code.strip().endswith("\\end{tabular}"):
            # Create a temporary LaTeX file with the provided content
            temp_tex_filename = "temp.tex"
            with open(temp_tex_filename, 'w') as f:
                f.write(r"""\documentclass{article}
                            \usepackage{array}
                            \usepackage{graphicx}
                            \begin{document}
                            \thispagestyle{empty}
                            """ + latex_code + r"""
                            \end{document}""")
            
            # Compile the LaTeX file to generate a PDF
            subprocess.call(["pdflatex", "-interaction=nonstopmode", temp_tex_filename])
            
            # Convert the generated PDF to an image
            pages = convert_from_path(temp_tex_filename.replace(".tex", ".pdf"))
            if pages:
                page = pages[0]
                img = ImageTk.PhotoImage(page)

                # Display the image
                preview_label = ttk.Label(self.scrollable_frame, image=img)
                preview_label.image = img
                preview_label.pack(padx=5, pady=5)

                # Clean up temporary files
                os.remove(temp_tex_filename)
                os.remove(temp_tex_filename.replace(".tex", ".pdf"))
            else:
                messagebox.showerror("Rendering Error", "Failed to render LaTeX table.")
        else:
            # Render as text with matplotlib (for symbols and equations)
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, latex_code, fontsize=12, ha='center', va='center')
            ax.axis('off')

            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            plt.close(fig)
            buffer.seek(0)

            img = ImageTk.PhotoImage(data=buffer.read())

            # Add the new preview image
            preview_label = ttk.Label(self.scrollable_frame, image=img)
            preview_label.image = img
            preview_label.pack(padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = LatexGenerator(root)
    root.mainloop()
