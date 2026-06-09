# Refactoring Notes

This file explains the professional cleanup decisions made in `simple_calculator.py`.

The goal was not to make the project more complicated. The goal was to make the code easier to read, easier to maintain, and still friendly for a beginner.

## 1. Clearer State Variable Names

Before:

```python
self.current_input = "0"
self.stored_value = None
self.pending_operator = None
self.waiting_for_operand = False
self.just_evaluated = False
```

After:

```python
self.current_operand = "0"
self.left_operand = None
self.selected_operator = None
self.is_waiting_for_next_operand = False
self.has_just_evaluated = False
```

Why:

The calculator works with operands and operators. Names like `current_operand` and `left_operand` explain the calculator model more clearly than generic names like `current_input` and `stored_value`.

Boolean names now read like true/false questions:

```python
if self.has_just_evaluated:
```

That is easier to understand than:

```python
if self.just_evaluated:
```

## 2. Clearer UI Variable Names

Before:

```python
self.root = tk.Tk()
self.canvas = tk.Canvas(...)
self.display_id = self.canvas.create_text(...)
```

After:

```python
self.window = tk.Tk()
self.drawing_area = tk.Canvas(...)
self.display_text_item = self.drawing_area.create_text(...)
```

Why:

`window` is more beginner-friendly than `root`, even though `root` is common in Tkinter examples.

`drawing_area` explains what a `Canvas` is doing.

`display_text_item` explains that the value is the canvas item ID for the display text.

## 3. Better Function Names

Before:

```python
press(value)
add_to_expression(value)
set_operator(operator)
backspace()
percent()
```

After:

```python
handle_input(button_value)
enter_digit_decimal_or_operator(button_value)
select_operator(operator)
delete_last_character()
convert_to_percent()
```

Why:

The old names worked, but some were vague.

`add_to_expression` was especially misleading because the calculator does not display a full expression. It displays one operand at a time.

The new names describe the user action more directly.

## 4. Constants Instead Of Magic Numbers

Before:

```python
diameter = 62
gap = 11
left = 24
top = 132
font=("Helvetica", 25)
```

After:

```python
BUTTON_DIAMETER = 62
BUTTON_GAP = 11
BUTTON_LEFT = 24
BUTTON_TOP = 132
BUTTON_FONT_SIZE = 25
```

Why:

Named constants explain what the numbers mean. They also make future visual changes easier because the important settings are grouped near the top of the class.

## 5. Button Labels As Constants

Before:

```python
if value == "C":
    self.clear()
elif value == "=":
    self.evaluate()
elif value == "+/-":
    self.toggle_sign()
```

After:

```python
if button_value == self.CLEAR_LABEL:
    self.clear()
elif button_value == self.EQUALS_LABEL:
    self.evaluate()
elif button_value == self.SIGN_LABEL:
    self.toggle_sign()
```

Why:

Constants reduce repeated raw strings. If a label changes later, it can be updated in one place.

## 6. Removed Repeated State Reset Code

Before:

```python
self.current_input = "0"
self.stored_value = None
self.pending_operator = None
self.waiting_for_operand = False
self.display_value = "0"
self.just_evaluated = False
```

Similar reset code appeared in more than one method.

After:

```python
def _reset_calculator_state(self):
    self.current_operand = "0"
    self.left_operand = None
    self.selected_operator = None
    self.is_waiting_for_next_operand = False
    self.display_text = "0"
    self.has_just_evaluated = False
    self.button_items = []
```

Why:

Resetting state in one helper avoids duplication and makes the default app state easy to find.

## 7. Split Button Drawing Into Smaller Helpers

Before:

`_draw_interface` calculated button positions, drew shapes, drew text, and registered clicks all in one large method.

After:

```python
_draw_calculator()
_get_button_bounds(...)
_draw_button_shape(...)
_create_pill_button(...)
_make_canvas_items_clickable(...)
```

Why:

Each helper now has one job:

- calculate button coordinates
- draw one button shape
- create the pill-shaped zero button
- connect canvas items to click events

This makes the drawing code easier to scan.

## 8. Split Operand Entry Into Smaller Helpers

Before:

`add_to_expression` handled operators, fresh operands, decimals, input limits, and digit appending in one method.

After:

```python
enter_digit_decimal_or_operator(...)
_start_new_operand()
_append_decimal_point()
_append_digit(...)
```

Why:

This keeps the input rules readable. A beginner can now inspect each small helper and understand one behavior at a time.

## 9. Kept A Single-File App

Decision:

The project still uses one main Python file.

Why:

For a beginner calculator project, splitting into many modules would add complexity before it adds much value. The code is now organized by methods and constants, which is enough for this project size.

## 10. Functionality Was Preserved

The refactor was intended to preserve behavior:

- button clicks still work
- keyboard input still works
- repeated equals still does not change the result
- long operands are still limited
- huge results still use scientific notation
- division by zero still shows `Error`

The code was verified after refactoring.
