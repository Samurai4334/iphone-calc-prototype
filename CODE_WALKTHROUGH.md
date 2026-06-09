# Code Walkthrough

This walkthrough explains how `simple_calculator.py` works from top to bottom. It is written for beginners who are learning how a small GUI program is structured.

## Big Picture

The project is a desktop calculator built with Python and Tkinter.

Tkinter is Python's built-in GUI toolkit. A GUI toolkit gives you tools to create windows, draw interface elements, and respond to user actions like mouse clicks and keyboard input.

This calculator has three major parts:

1. The window and visual interface
2. The calculator state
3. The event-handling and arithmetic logic

## File Structure

```text
iphone-calc-prototype/
├── simple_calculator.py
├── README.md
├── CODE_WALKTHROUGH.md
├── REFACTORING_NOTES.md
├── requirements.txt
└── .gitignore
```

`simple_calculator.py` is the actual application.

`CODE_WALKTHROUGH.md` is this learning guide.

`REFACTORING_NOTES.md` explains the cleanup decisions and shows before/after examples.

`README.md` explains how to run the project.

`requirements.txt` is included for project convention, but the app has no external pip dependencies.

`.gitignore` keeps generated files like `__pycache__/` and `.venv/` out of Git.

## Importing Tkinter

The app starts with:

```python
import tkinter as tk
```

This imports Tkinter and gives it the shorter name `tk`.

Using `tk.Canvas` and `tk.Tk` is easier to read than writing `tkinter.Canvas` and `tkinter.Tk` every time.

## The `CalculatorApp` Class

The calculator is organized into one class:

```python
class CalculatorApp:
```

A class is a good fit because the app needs to remember information while it runs.

For example, it remembers:

- the number currently being typed
- the first number in a calculation
- the operator selected by the user
- whether the app is waiting for the second number
- what text is currently shown on the display

Without a class, these values would need to be passed around many functions manually.

## Constants

Near the top of the class, there are constants:

```python
WINDOW_WIDTH = 330
WINDOW_HEIGHT = 520
BACKGROUND_COLOR = "#2c2c2e"
NUMBER_BUTTON_COLOR = "#333333"
UTILITY_BUTTON_COLOR = "#a5a5a5"
OPERATOR_BUTTON_COLOR = "#ff9f0a"
MAX_DISPLAY_CHARS = 9
MAX_INPUT_DIGITS = 9
```

These values control the look and limits of the calculator.

They are written in uppercase because they are meant to behave like fixed settings.

Examples:

- `WINDOW_WIDTH` and `WINDOW_HEIGHT` control the window size.
- `BACKGROUND_COLOR` controls the main background color.
- `OPERATOR_BUTTON_COLOR` controls the orange operator buttons.
- `MAX_INPUT_DIGITS` prevents typed numbers from becoming too long.

## How The Window Is Created

The window is created inside `__init__`:

```python
self.window = tk.Tk()
```

`tk.Tk()` creates the main application window.

Then the code configures the window:

```python
self.window.title(self.WINDOW_TITLE)
self.window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
self.window.resizable(False, False)
self.window.configure(bg=self.BACKGROUND_COLOR)
self.window.attributes("-topmost", True)
```

Each line has a job:

- `title(...)` sets the window title.
- `geometry(...)` sets the size.
- `resizable(False, False)` prevents resizing.
- `configure(bg=...)` sets the background color.
- `attributes("-topmost", True)` keeps the window visible above other windows.

## Calculator State Variables

The calculator stores its current state in these variables:

```python
self.current_operand = "0"
self.left_operand = None
self.selected_operator = None
self.is_waiting_for_next_operand = False
self.display_text = "0"
self.has_just_evaluated = False
self.button_items = []
```

Here is what each one means:

`current_operand`

The number currently being typed or displayed.

`left_operand`

The first number in an operation. If the user presses `8 +`, then `8` is stored here.

`selected_operator`

The operator waiting to be applied. It can be `+`, `-`, `*`, or `/`.

`is_waiting_for_next_operand`

This becomes `True` after an operator is pressed. It tells the calculator that the next digit should start the second number.

`display_text`

The exact text currently visible on the calculator display.

`has_just_evaluated`

This becomes `True` after `=` is pressed. It prevents repeated equals from changing the result.

`button_items`

This stores information about the drawn button objects. It is useful for keeping track of the UI items.

## How Tkinter Works

Tkinter programs are event-driven.

That means the program does not run from top to bottom and then end. Instead, it creates a window and waits for events.

Events include:

- clicking a button
- pressing a keyboard key
- moving the mouse over a button
- closing the window

The function that starts this waiting loop is:

```python
self.window.mainloop()
```

The app stays open while `mainloop()` is running.

## Why This App Uses A Canvas

The code creates a canvas:

```python
self.drawing_area = tk.Canvas(...)
```

A canvas is a drawing area.

This app uses a canvas instead of normal Tkinter buttons because the design needs circular buttons and a pill-shaped `0` button. A canvas lets us draw circles, rectangles, and text manually.

The canvas is added to the window with:

```python
self.drawing_area.pack(fill="both", expand=True)
```

`pack(...)` is one of Tkinter's layout managers. It tells Tkinter where to place a widget inside the window.

## How The Display Is Created

The display text is created with:

```python
self.display_text_item = self.drawing_area.create_text(...)
```

This draws text on the canvas.

Important settings:

- `anchor="e"` right-aligns the text.
- `fill=self.WHITE_TEXT` makes the text white.
- `font=(...)` controls the font and size.

The calculator stores the returned ID in `self.display_text_item`. Later, the app uses that ID to update the display instead of creating new text every time.

## How Buttons Are Created

The button layout is stored as a list of rows:

```python
BUTTON_LAYOUT = [
    ["C", "+/-", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]
```

This is a clean way to describe a keypad.

The code loops over this layout in `_draw_calculator`.

For each label, the app:

1. calculates the button coordinates with `_get_button_bounds`
2. draws the button with `_draw_button_shape`
3. draws the text label
4. makes the button clickable with `_make_canvas_items_clickable`

Normal buttons are drawn with:

```python
self.drawing_area.create_oval(...)
```

The `0` button is wider, so it is drawn with `_create_pill_button(...)`.

## How The Pill-Shaped Zero Button Works

Tkinter Canvas does not have a built-in rounded rectangle command.

So `_create_pill_button(...)` builds the shape from three pieces:

1. a left circle
2. a right circle
3. a middle rectangle

Together, those pieces look like one rounded pill.

## How Button Clicks Are Handled

Every button has a shape and a text label.

The code makes both clickable by calling:

```python
self._make_canvas_items_clickable(button_label, item_ids)
```

Inside that method, this line connects a click event to the calculator:

```python
self.drawing_area.tag_bind(item_id, "<Button-1>", ...)
```

`<Button-1>` means left mouse click.

When a click happens, the app calls:

```python
self.handle_input(value)
```

The value is the button label, such as `"7"`, `"+"`, or `"="`.

## How Keyboard Input Is Handled

Keyboard bindings are created in `_bind_keyboard_shortcuts`:

```python
self.window.bind("<Key>", self._handle_keyboard_input)
self.window.bind("<Return>", lambda _event: self.handle_input(self.EQUALS_LABEL))
self.window.bind("<BackSpace>", lambda _event: self.delete_last_character())
self.window.bind("<Escape>", lambda _event: self.clear())
```

This means:

- normal keys go to `_handle_keyboard_input`
- Enter presses equals
- Backspace deletes one character
- Escape clears the calculator

`_handle_keyboard_input` checks whether the typed key is allowed:

```python
if event.char in self.KEYBOARD_INPUTS:
    self.handle_input(event.char)
```

This is good design because keyboard input and mouse input both go through the same `handle_input(...)` method.

## The `handle_input` Router

The `handle_input` method decides what kind of input happened:

```python
if button_value == self.CLEAR_LABEL:
    self.clear()
elif button_value == self.EQUALS_LABEL:
    self.evaluate()
elif button_value == self.SIGN_LABEL:
    self.toggle_sign()
elif button_value == self.PERCENT_LABEL:
    self.convert_to_percent()
else:
    self.enter_digit_decimal_or_operator(button_value)
```

This method is like a traffic controller.

It does not do all the work itself. It routes each button to the correct helper method.

## How Number Input Works

Number and decimal input is handled in `enter_digit_decimal_or_operator`.

Important behaviors:

- If an operator was just pressed, the next digit starts a new operand.
- If a result was just calculated, typing a number starts a new calculation.
- Only one decimal point is allowed.
- Input stops at `MAX_INPUT_DIGITS`.

This keeps the display from overflowing.

## How Operators Work

When the user presses `+`, `-`, `*`, or `/`, the code calls:

```python
self.select_operator(button_value)
```

That method stores:

- the first number in `left_operand`
- the operator in `selected_operator`

Then it clears the display to `0` so the second number can be entered cleanly.

Example:

```text
8 + 5 =
```

After pressing `8 +`:

- `left_operand` is `8`
- `selected_operator` is `+`
- the display resets to `0`

Then `5` becomes the second operand.

## How Calculations Are Performed

When the user presses `=`, the app calls `evaluate`.

`evaluate` checks whether there is enough information to calculate:

- first number
- operator
- second number

Then it calls:

```python
self._calculate(self.left_operand, self.selected_operator, float(self.current_operand))
```

`_calculate` contains the arithmetic:

```python
if operator == "+":
    return first_number + second_number
```

It does the same for subtraction, multiplication, and division.

Division by zero raises an error and displays `Error`.

## How The Display Is Updated

The visible display is updated through:

```python
self.update_display(...)
```

This method:

1. stores the new display text
2. checks whether the text is too long
3. uses scientific notation for large final results
4. refreshes the canvas text

The actual canvas update happens in `_refresh_display`:

```python
self.drawing_area.itemconfig(self.display_text_item, text=self.display_text)
```

`itemconfig` changes an existing canvas item.

That is better than drawing new display text over and over.

## Scientific Notation

If a final result is too large to fit, the app displays it in scientific notation.

Example:

```text
999999999 * 999999999 = 1e+18
```

This keeps the number readable inside a small display.

## How The Application Starts

At the bottom of the file:

```python
if __name__ == "__main__":
    CalculatorApp().run()
```

This means:

Only start the app if this file is run directly.

When you run:

```bash
python3 simple_calculator.py
```

Python creates a `CalculatorApp` object and calls `run()`.

## How The Application Exits

The app exits when the user closes the window.

Closing the window ends Tkinter's `mainloop()`, and then the Python program finishes.

## High-Level Flow

Here is the main flow:

```text
Run file
↓
Create CalculatorApp
↓
Create Tkinter window
↓
Create canvas drawing area
↓
Draw display and buttons
↓
Bind mouse and keyboard events
↓
Start Tkinter mainloop
↓
User clicks/types
↓
handle_input(...) routes the action
↓
Calculator state changes
↓
Display updates
```

## Why The Project Is Designed This Way

This structure keeps the project beginner-friendly:

- one Python file for the actual app
- one class to keep state organized
- named constants for UI values and labels
- helper methods for each responsibility
- comments and docstrings explaining why each part exists
- no external packages

That makes it easier to understand before moving on to larger projects with multiple files, tests, and packaging.
