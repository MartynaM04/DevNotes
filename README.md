# 💻 DevNotes

> *A minimalist, developer-focused notebook built with Python and CustomTkinter.*

DevNotes is designed to keep your programming theory and code snippets logically separated but visible at a glance. It serves as a dedicated workspace for learning new languages, storing reference code, and keeping your technical thoughts organized without the visual clutter of a full-fledged IDE or the formatting limitations of a basic text editor.

---

## Key Features

* **Split Workspace Configuration**
  Every programming language tab is divided into two distinct zones: a "Concepts & Theory" section utilizing a clean, prose-friendly font, and a "Code Snippets" section strictly utilizing a monospace font.
* **Developer-First Editor Mechanics**
  The code area intercepts the `Tab` key to insert exactly 4 spaces, preserving your formatting. A built-in "Copy Code" button allows for instant clipboard transfer of your snippets for testing.
* **Dynamic Tab Management**
  Add or remove specific programming language tabs on the fly to match your current learning path or tech stack.
* **Debounced Auto-Save**
  The application continuously and silently saves your progress in the background shortly after you stop typing. Your notes are never lost.
* **Customizable Interface**
  Toggle instantly between Dark and Light modes. Adjust the global font size directly from the top bar to suit your screen size and eye comfort.
* **Local & Portable Storage**
  All your notes, code snippets, and application preferences are saved locally in a single JSON file, making data backup and migration completely frictionless.

---

**1. Clone this repository to your local machine:**
```bash
git clone https://github.com/MartynaM04/DevNotes.git
cd DevNotes
```

**2. Install the required dependencies.** 
*DevNotes requires Python 3.8+ and the CustomTkinter library:*
```bash
pip install customtkinter
```

**3. Run the application:**
```bash
python devnotes.py
```

---

## Building a Standalone Executable

If you prefer to run DevNotes as a standalone application (`.exe`) without opening a Python environment, you can compile it using PyInstaller:

**1. Install PyInstaller:**
```bash
pip install pyinstaller
```

**2. Compile the application with the required UI assets:**
```bash
python -m PyInstaller --noconsole --onefile --collect-all customtkinter devnotes.py
```

**3. Locate your executable:**
Navigate to the newly created `dist` folder to find your compiled, ready-to-run `.exe` file.

---

## Technical Stack

* **Language:** Python
* **GUI Framework:** CustomTkinter
* **Persistence:** JSON

---

## License

Distributed under the MIT License.
