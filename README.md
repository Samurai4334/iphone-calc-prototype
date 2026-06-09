# iPhone Calc Prototype

A compact desktop calculator built with Python and Tkinter. The interface is inspired by the iPhone calculator, with circular buttons, orange operator controls, keyboard input, and a small window that is easy to run locally.

## Features

- Clickable calculator buttons
- Keyboard input for numbers and operators
- Addition, subtraction, multiplication, and division
- Clear, percentage, positive/negative toggle, and decimal input
- Per-operand input limit so numbers do not overflow the display
- Scientific notation for very large or tiny results
- Repeated equals does not change the completed result
- Compact prototype window layout

## Project Structure

```text
iphone-calc-prototype/
├── simple_calculator.py
├── README.md
├── CODE_WALKTHROUGH.md
├── REFACTORING_NOTES.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- Tkinter

No external Python packages are required. The `requirements.txt` file is included for GitHub/project convention, but it does not install any third-party packages.

Tkinter ships with many Python installations. On some systems, it must be installed separately through the operating system package manager.

## Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd iphone-calc-prototype
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Python package requirements:

```bash
pip install -r requirements.txt
```

Run the calculator:

```bash
python3 simple_calculator.py
```

On Windows, use this if `python3` is not available:

```powershell
python simple_calculator.py
```

## macOS Tkinter Notes

If you see this error:

```text
ModuleNotFoundError: No module named '_tkinter'
```

your Python installation does not have Tkinter support.

For Homebrew Python 3.11:

```bash
brew install python-tk@3.11
```

For Homebrew Python 3.13:

```bash
brew install python-tk@3.13
```

Then run:

```bash
python3 simple_calculator.py
```

## Linux Tkinter Notes

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3-tk
```

Fedora:

```bash
sudo dnf install python3-tkinter
```

Arch Linux:

```bash
sudo pacman -S tk
```

## Windows Tkinter Notes

If Tkinter is missing on Windows, reinstall Python from the official Python installer and make sure **tcl/tk and IDLE** is selected during installation.

## VS Code

Open `simple_calculator.py` and run it with the Python extension or from the integrated terminal:

```bash
python3 simple_calculator.py
```

This repository intentionally does not include `.vscode/settings.json`, because interpreter paths are machine-specific. If the VS Code play button uses the wrong Python interpreter, select the correct interpreter from:

```text
Command Palette -> Python: Select Interpreter
```

Choose the same Python that successfully runs the calculator from your terminal.

## Screenshots

Add screenshots before publishing a polished GitHub page.

Suggested files:

```text
screenshots/
├── calculator-home.png
└── calculator-result.png
```

## Future Improvements

- Add button press animations
- Replace `eval`-style expression handling with a dedicated expression parser if advanced expressions are added
- Add memory buttons
- Add unit tests for calculator logic
- Package the app as a standalone executable
