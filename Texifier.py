import tkinter as tk
from tkinter import ttk, scrolledtext, Canvas, Scrollbar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk

class LatexGenerator:
    def __init__(self, root):
        """
        Initialize the LaTeX Code Generator application.
        """
        self.root = root
        self.root.title("LaTeX Code Generator")
        self.configure_styles()

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=0)  # Input area
        self.root.grid_rowconfigure(1, weight=1)  # Tabs
        self.root.grid_rowconfigure(2, weight=0)  # Generate button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Input area for LaTeX code
        self.input_area = scrolledtext.ScrolledText(self.root, width=50, height=8, bg='#444444', fg='white', insertbackground='white', font=("Helvetica", 10))
        self.input_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

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
        self.canvas = Canvas(self.preview_frame)
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
        self.root.option_add("*TButton*Foreground", "white")
        self.root.option_add("*TButton*Background", "#555555")
        self.root.option_add("*TButton*ActiveBackground", "#777777")
        self.root.option_add("*TButton*Relief", "flat")
        self.root.option_add("*TFrame*Background", "#2e2e2e")
        self.root.option_add("*TLabel*Foreground", "white")

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
        # Frame for input and buttons (Math tab)
        self.math_frame = ttk.Frame(self.math_tab)
        self.math_frame.pack(fill='both', expand=True)

        # Sections for math buttons
        self.create_sections(self.math_frame)

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
            ("binom", "\\binom{}{}"), ("√", "\\sqrt{}"), ("sum", "\\sum"),
            ("prod", "\\prod"), ("∫", "\\int"), ("∮", "\\oint")
        ]
        self.create_buttons(constructs_frame, constructs, special=True)

        # Delimiters section
        delimiters_frame = self.create_label_frame("Delimiters", parent_frame)
        delimiters = [
            ("(", "("), (")", ")"), ("[", "["), ("]", "]"), ("{", "\\{"), ("}", "\\}"),
            ("|", "|"), ("||", "\\|\\|"), ("<", "<"), (">", ">")
        ]
        self.create_buttons(delimiters_frame, delimiters)

        # Arrow symbols section
        arrows_frame = self.create_label_frame("Arrows", parent_frame)
        arrows = [
            ("←", "\\leftarrow"), ("→", "\\rightarrow"), ("↑", "\\uparrow"), ("↓", "\\downarrow"),
            ("↔", "\\leftrightarrow"), ("⇐", "\\Leftarrow"), ("⇒", "\\Rightarrow"), ("⇑", "\\Uparrow"),
            ("⇓", "\\Downarrow"), ("⇔", "\\Leftrightarrow")
        ]
        self.create_buttons(arrows_frame, arrows)

        # Miscellaneous symbols section
        misc_frame = self.create_label_frame("Miscellaneous", parent_frame)
        misc_symbols = [
            ("∅", "\\emptyset"), ("∇", "\\nabla"), ("ℕ", "\\mathbb{N}"),
            ("ℤ", "\\mathbb{Z}"), ("ℚ", "\\mathbb{Q}"), ("ℝ", "\\mathbb{R}"), ("ℂ", "\\mathbb{C}")
        ]
        self.create_buttons(misc_frame, misc_symbols)

    def create_label_frame(self, text, parent_frame):
        """
        Create a labeled frame within the parent frame.
        """
        frame = ttk.LabelFrame(parent_frame, text=text)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        return frame

    def create_buttons(self, frame, items, special=False):
        """
        Create buttons within the specified frame for each item.
        """
        button_width = 5
        button_height = 2
        for i, (text, symbol) in enumerate(items):
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
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, latex_code, fontsize=12, ha='center', va='center')
        ax.axis('off')
    
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
    
        img = ImageTk.PhotoImage(data=buffer.read())
    
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
        # Add the new preview image
        preview_label = ttk.Label(self.scrollable_frame, image=img)
        preview_label.image = img
        preview_label.pack(padx=5, pady=5)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = LatexGenerator(root)
    root.mainloop()