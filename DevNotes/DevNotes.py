import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import json

# --- CONFIGURATION ---
APP_TITLE = "DevNotes — Programming Notebook"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DevNotes_Data")
DATA_FILE = os.path.join(DATA_DIR, "notes.json")
FONT_SIZES = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "22", "24"]

DEFAULT_LANGUAGES = ["Python", "JavaScript", "TypeScript", "HTML/CSS", "C#", "C++", "Java", "SQL"]

# --- COLOR PALETTE ---
THEMES = {
    "light": {
        "bg": "#F3F4F6",             # Light gray background
        "theory_bg": "#FFFFFF",      # White paper for theory
        "code_bg": "#1E1E1E",        # Dark background for code (IDE style)
        "code_fg": "#D4D4D4",        # Light gray text for code
        "text": "#1F2937",           # Dark gray text for notes
        "accent": "#3B82F6",         # Blue accent
        "danger": "#EF4444",         # Red for delete actions
        "border": "#E5E7EB"
    },
    "dark": {
        "bg": "#111827",             # Dark app background
        "theory_bg": "#1F2937",      # Dark gray notes background
        "code_bg": "#0D1117",        # Very dark code background (GitHub style)
        "code_fg": "#E6EDF3",        # Light text for code
        "text": "#F9FAFB",           # Light text for notes
        "accent": "#3B82F6",         # Blue accent
        "danger": "#EF4444",         # Red for delete actions
        "border": "#374151"
    }
}

class DevNotes(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x750")
        
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Dictionary storing references to text widgets for each language tab
        self.text_widgets = {}
        self._auto_save_job = None
        
        # Load user data and settings before building the UI
        self.raw_data = self._load_raw_data()
        settings = self.raw_data.get("_settings", {})
        
        self.current_theme = settings.get("theme", "dark")
        self.current_font_size = settings.get("font_size", 11)
        self.languages = settings.get("languages", DEFAULT_LANGUAGES.copy())
        
        ctk.set_appearance_mode(self.current_theme)
        
        self.setup_ui()
        self.restore_text_content()
        
        # Restore previously active tab
        active_tab = settings.get("active_tab")
        if active_tab in self.languages:
            self.tabview.set(active_tab)
            
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _load_raw_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def setup_ui(self):
        t = THEMES[self.current_theme]
        self.configure(fg_color=t["bg"])

        # ================= TOP BAR =================
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.top_bar.pack(side="top", fill="x", padx=20, pady=(10, 0))
        
        # App Title
        self.lbl_title = ctk.CTkLabel(self.top_bar, text="DevNotes", font=("Segoe UI", 20, "bold"), text_color=t["text"])
        self.lbl_title.pack(side="left")
        
        # Save Status Indicator
        self.lbl_status = ctk.CTkLabel(self.top_bar, text="All changes saved.", font=("Segoe UI", 11, "italic"), text_color=t["accent"])
        self.lbl_status.pack(side="left", padx=20)

        # Theme Toggle Button
        self.btn_theme = ctk.CTkButton(
            self.top_bar, text="Light Mode" if self.current_theme == "dark" else "Dark Mode", 
            width=80, height=30, font=("Segoe UI", 12, "bold"), 
            fg_color=t["theory_bg"], text_color=t["text"], command=self.toggle_theme
        )
        self.btn_theme.pack(side="right")

        # Font Size Selector
        self.font_size_var = ctk.StringVar(value=str(self.current_font_size))
        self.font_selector = ctk.CTkOptionMenu(
            self.top_bar, values=FONT_SIZES, variable=self.font_size_var, width=70, height=30,
            fg_color=t["theory_bg"], text_color=t["text"], button_color=t["border"], button_hover_color=t["accent"],
            command=self.change_font_size
        )
        self.font_selector.pack(side="right", padx=(10, 15))

        self.lbl_font = ctk.CTkLabel(self.top_bar, text="Font Size:", font=("Segoe UI", 12, "bold"), text_color=t["text"])
        self.lbl_font.pack(side="right")

        # Add Language Tab Button
        self.btn_add_tab = ctk.CTkButton(
            self.top_bar, text="+ Add Language", width=110, height=30, font=("Segoe UI", 12, "bold"),
            fg_color="transparent", border_width=1, border_color=t["accent"], text_color=t["accent"],
            command=self.add_new_language
        )
        self.btn_add_tab.pack(side="right", padx=(0, 20))

        # ================= TABVIEW =================
        self.tabview = ctk.CTkTabview(
            self, fg_color=t["theory_bg"], border_color=t["border"], border_width=1,
            segmented_button_selected_color=t["accent"], segmented_button_selected_hover_color=t["accent"]
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        # Create tabs based on the loaded languages list
        for lang in self.languages:
            tab = self.tabview.add(lang)
            self.build_language_tab(tab, lang, t)

    def build_language_tab(self, parent_tab, lang, theme):
        # Main container splitting the tab into two columns
        container = ctk.CTkFrame(parent_tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        container.columnconfigure(0, weight=1)  # Theory column
        container.columnconfigure(1, weight=1)  # Code column

        # --- LEFT SIDE: THEORY & CONCEPTS ---
        theory_frame = ctk.CTkFrame(container, fg_color="transparent")
        theory_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        lbl_theory = ctk.CTkLabel(theory_frame, text="📝 Concepts & Theory", font=("Segoe UI", 14, "bold"), text_color=theme["text"])
        lbl_theory.pack(anchor="w", pady=(0, 5))
        
        txt_theory = tk.Text(
            theory_frame, bg=theme["theory_bg"], fg=theme["text"], insertbackground=theme["text"],
            font=("Segoe UI", self.current_font_size), wrap="word", relief="flat", highlightthickness=1, 
            highlightbackground=theme["border"], padx=15, pady=15
        )
        txt_theory.pack(fill="both", expand=True)
        txt_theory.bind("<KeyRelease>", self.schedule_auto_save)

        # --- RIGHT SIDE: CODE SNIPPETS ---
        code_frame = ctk.CTkFrame(container, fg_color="transparent")
        code_frame.grid(row=0, column=1, sticky="nsew")
        
        code_header = ctk.CTkFrame(code_frame, fg_color="transparent")
        code_header.pack(fill="x", pady=(0, 5))
        
        lbl_code = ctk.CTkLabel(code_header, text="/> Code Snippets", font=("Consolas", 14, "bold"), text_color=theme["accent"])
        lbl_code.pack(side="left")
        
        # Copy Code Button
        btn_copy = ctk.CTkButton(
            code_header, text="📋 Copy Code", width=80, height=24, font=("Segoe UI", 11, "bold"),
            fg_color="transparent", border_width=1, border_color=theme["accent"], text_color=theme["accent"],
            command=lambda c=lang: self.copy_code_to_clipboard(c)
        )
        btn_copy.pack(side="right")
        
        # Delete Tab Button
        btn_delete = ctk.CTkButton(
            code_header, text="🗑 Delete Tab", width=80, height=24, font=("Segoe UI", 11, "bold"),
            fg_color="transparent", border_width=1, border_color=theme["danger"], text_color=theme["danger"],
            command=lambda c=lang: self.delete_language(c)
        )
        btn_delete.pack(side="right", padx=(0, 10))

        txt_code = tk.Text(
            code_frame, bg=theme["code_bg"], fg=theme["code_fg"], insertbackground=theme["code_fg"],
            font=("Consolas", self.current_font_size), wrap="none", relief="flat", highlightthickness=1, 
            highlightbackground=theme["border"], padx=15, pady=15
        )
        txt_code.pack(fill="both", expand=True)
        
        # Handle Tab key (inserts 4 spaces instead of changing focus)
        txt_code.bind("<Tab>", self.insert_tab_spaces)
        txt_code.bind("<KeyRelease>", self.schedule_auto_save)

        # Add horizontal scrollbar for code snippet area
        scroll_x = ctk.CTkScrollbar(code_frame, orientation="horizontal", command=txt_code.xview, height=12)
        scroll_x.pack(fill="x")
        txt_code.configure(xscrollcommand=scroll_x.set)

        # Save references for later access and theming
        self.text_widgets[lang] = {
            "theory": txt_theory,
            "code": txt_code,
            "lbl_theory": lbl_theory,
            "lbl_code": lbl_code,
            "btn_copy": btn_copy,
            "btn_delete": btn_delete
        }

    # ==================== DYNAMIC TAB MANAGEMENT ====================
    def add_new_language(self):
        """Prompts the user to enter a new programming language and creates a tab for it."""
        dialog = ctk.CTkInputDialog(text="Enter the name of the programming language:", title="Add New Tab")
        new_lang = dialog.get_input()
        
        if new_lang:
            new_lang = new_lang.strip()
            if new_lang and new_lang not in self.languages:
                self.languages.append(new_lang)
                tab = self.tabview.add(new_lang)
                self.build_language_tab(tab, new_lang, THEMES[self.current_theme])
                self.tabview.set(new_lang)
                self.schedule_auto_save()
            elif new_lang in self.languages:
                self.tabview.set(new_lang)

    def delete_language(self, lang):
        """Deletes a language tab and removes its data after user confirmation."""
        if messagebox.askyesno("Delete Tab", f"Are you sure you want to delete the '{lang}' tab and all its notes?\nThis action cannot be undone."):
            self.languages.remove(lang)
            self.tabview.delete(lang)
            del self.text_widgets[lang]
            self.schedule_auto_save()

    # ==================== HELPER FUNCTIONS ====================
    def insert_tab_spaces(self, event):
        """Converts Tab key press into 4 spaces in the code editors."""
        event.widget.insert("insert", "    ")
        self.schedule_auto_save()
        return "break"

    def copy_code_to_clipboard(self, lang):
        """Copies the contents of the specified language's code editor to the clipboard."""
        code_content = self.text_widgets[lang]["code"].get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(code_content)
        self.lbl_status.configure(text=f"Copied {lang} code to clipboard!")
        self.after(3000, lambda: self.lbl_status.configure(text="All changes saved."))

    def change_font_size(self, new_size):
        """Updates the font size across all text areas."""
        self.current_font_size = int(new_size)
        for lang, widgets in self.text_widgets.items():
            widgets["theory"].configure(font=("Segoe UI", self.current_font_size))
            widgets["code"].configure(font=("Consolas", self.current_font_size))
        self.schedule_auto_save()

    def toggle_theme(self):
        """Switches between Dark and Light mode and updates widget colors."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme)
        t = THEMES[self.current_theme]
        
        # Update main backgrounds and top bar
        self.configure(fg_color=t["bg"])
        self.lbl_title.configure(text_color=t["text"])
        self.lbl_font.configure(text_color=t["text"])
        
        self.btn_theme.configure(
            text="Light Mode" if self.current_theme == "dark" else "Dark Mode",
            fg_color=t["theory_bg"], text_color=t["text"]
        )
        self.font_selector.configure(
            fg_color=t["theory_bg"], text_color=t["text"], button_color=t["border"], button_hover_color=t["accent"]
        )
        self.tabview.configure(fg_color=t["theory_bg"], border_color=t["border"])
        
        # Update dynamically generated tabs
        for lang, widgets in self.text_widgets.items():
            widgets["lbl_theory"].configure(text_color=t["text"])
            widgets["lbl_code"].configure(text_color=t["accent"])
            
            widgets["btn_copy"].configure(border_color=t["accent"], text_color=t["accent"])
            widgets["btn_delete"].configure(border_color=t["danger"], text_color=t["danger"])
            
            widgets["theory"].configure(
                bg=t["theory_bg"], fg=t["text"], insertbackground=t["text"], highlightbackground=t["border"]
            )
            widgets["code"].configure(
                bg=t["code_bg"], fg=t["code_fg"], insertbackground=t["code_fg"], highlightbackground=t["border"]
            )
        self.schedule_auto_save()

    # ==================== SAVE & LOAD SYSTEM ====================
    def restore_text_content(self):
        """Injects text content into the text areas from the loaded JSON data."""
        for lang in self.languages:
            if lang in self.raw_data and lang in self.text_widgets:
                self.text_widgets[lang]["theory"].insert("1.0", self.raw_data[lang].get("theory", ""))
                self.text_widgets[lang]["code"].insert("1.0", self.raw_data[lang].get("code", ""))

    def schedule_auto_save(self, event=None):
        """Triggers a save attempt 800ms after the user stops typing."""
        if self._auto_save_job is not None:
            self.after_cancel(self._auto_save_job)
        self.lbl_status.configure(text="Saving...", text_color=THEMES[self.current_theme]["text"])
        self._auto_save_job = self.after(800, self.save_data)

    def save_data(self):
        """Compiles all notes, code, active languages, and settings into a JSON file."""
        self._auto_save_job = None
        data = {}
        
        for lang in self.languages:
            data[lang] = {
                "theory": self.text_widgets[lang]["theory"].get("1.0", "end-1c"),
                "code": self.text_widgets[lang]["code"].get("1.0", "end-1c")
            }
        
        # Save user preferences alongside notes
        try:
            active_t = self.tabview.get()
        except ValueError:
            active_t = self.languages[0] if self.languages else ""

        data["_settings"] = {
            "theme": self.current_theme,
            "font_size": self.current_font_size,
            "languages": self.languages,
            "active_tab": active_t
        }

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.lbl_status.configure(text="All changes saved.", text_color=THEMES[self.current_theme]["accent"])
        except Exception:
            self.lbl_status.configure(text="Error saving data!", text_color=THEMES[self.current_theme]["danger"])

    def on_close(self):
        """Ensures all data is saved securely right before the app window closes."""
        if self._auto_save_job is not None:
            self.after_cancel(self._auto_save_job)
        self.save_data()
        self.destroy()

if __name__ == "__main__":
    app = DevNotes()
    app.mainloop()