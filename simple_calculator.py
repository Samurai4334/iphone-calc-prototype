"""An iPhone-style calculator built with Python and Tkinter.

This file contains the complete application:
- the Tkinter window
- the custom-drawn calculator buttons
- the calculator state
- the arithmetic logic
- the event handlers for mouse clicks and keyboard input
"""

import tkinter as tk


class CalculatorApp:
    """Represent the full calculator application.

    A class is useful here because the calculator has state that changes over
    time. For example, it needs to remember the number currently being typed,
    the previous number, and the pending operator.
    """

    # Window dimensions. These keep the UI small and phone-like instead of
    # expanding to fill the whole laptop screen.
    WINDOW_WIDTH = 330
    WINDOW_HEIGHT = 520
    WINDOW_TITLE = "Mini Calculator"

    # Display positioning and font sizes. Keeping these as constants avoids
    # hard-coded "magic numbers" inside the drawing methods.
    DISPLAY_X_PADDING = 22
    DISPLAY_Y = 76
    DISPLAY_FONT_FAMILY = "Helvetica"
    DISPLAY_FONT_LARGE = 52
    DISPLAY_FONT_MEDIUM = 46
    DISPLAY_FONT_SMALL = 40
    DISPLAY_FONT_EXTRA_SMALL = 34

    # Button geometry. These values control the circular keypad layout.
    BUTTON_DIAMETER = 62
    BUTTON_GAP = 11
    BUTTON_LEFT = 24
    BUTTON_TOP = 132
    BUTTON_TEXT_OFFSET_FOR_ZERO = 34
    BUTTON_FONT_SIZE = 25
    BUTTON_OUTLINE_WIDTH = 2

    # Color constants. Keeping colors in one place makes the UI easier to tune.
    BACKGROUND_COLOR = "#2c2c2e"
    NUMBER_BUTTON_COLOR = "#333333"
    UTILITY_BUTTON_COLOR = "#a5a5a5"
    OPERATOR_BUTTON_COLOR = "#ff9f0a"
    BUTTON_OUTLINE_COLOR = "#2f2f31"
    WHITE_TEXT = "#ffffff"
    BLACK_TEXT = "#000000"

    # Button labels. Named constants reduce typo risk and make logic easier to
    # read than raw strings repeated throughout the class.
    CLEAR_LABEL = "C"
    SIGN_LABEL = "+/-"
    PERCENT_LABEL = "%"
    DECIMAL_LABEL = "."
    EQUALS_LABEL = "="
    ZERO_LABEL = "0"

    OPERATOR_LABELS = {"/", "*", "-", "+"}
    UTILITY_LABELS = {CLEAR_LABEL, SIGN_LABEL, PERCENT_LABEL}
    KEYBOARD_INPUTS = "0123456789.+-*/%"

    # This layout list is the calculator keypad. Each inner list is one row.
    BUTTON_LAYOUT = [
        [CLEAR_LABEL, SIGN_LABEL, PERCENT_LABEL, "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        [ZERO_LABEL, DECIMAL_LABEL, EQUALS_LABEL],
    ]

    # Display limits. They prevent long numbers from spilling out of the screen.
    MAX_DISPLAY_CHARS = 9
    MAX_INPUT_DIGITS = 9

    def __init__(self):
        """Create the window, initialize state, draw the UI, and bind events."""
        # `Tk()` creates the main application window.
        self.window = tk.Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.configure(bg=self.BACKGROUND_COLOR)
        self.window.attributes("-topmost", True)

        self._reset_calculator_state()

        # The canvas is a drawing surface. We use it instead of ordinary Tk
        # buttons because it lets us draw circular buttons and a pill-shaped 0.
        self.drawing_area = tk.Canvas(
            self.window,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.drawing_area.pack(fill="both", expand=True)

        self._draw_calculator()
        self._bind_keyboard_shortcuts()
        self.window.update_idletasks()

    def _reset_calculator_state(self):
        """Reset the internal calculator values without redrawing the UI.

        This helper removes duplication between `__init__`, `clear`, and
        `_show_error`. It keeps all state defaults in one place.
        """
        # Calculator state:
        # - current_operand is the number currently shown/being typed.
        # - left_operand is the first number after an operator is pressed.
        # - selected_operator is the operator waiting for a second number.
        # - is_waiting_for_next_operand tells us the next digit should start a new number.
        # - has_just_evaluated prevents repeated equals from recalculating.
        self.current_operand = "0"
        self.left_operand = None
        self.selected_operator = None
        self.is_waiting_for_next_operand = False
        self.display_text = "0"
        self.has_just_evaluated = False
        self.button_items = []

    def _draw_calculator(self):
        """Draw the calculator display and all button shapes on the canvas."""
        # The display is right-aligned, just like a real calculator.
        self.display_text_item = self.drawing_area.create_text(
            self.WINDOW_WIDTH - self.DISPLAY_X_PADDING,
            self.DISPLAY_Y,
            text=self.display_text,
            fill=self.WHITE_TEXT,
            anchor="e",
            font=(self.DISPLAY_FONT_FAMILY, self._get_display_font_size()),
        )

        button_step = self.BUTTON_DIAMETER + self.BUTTON_GAP

        # Loop through every label in the layout and draw its matching button.
        for row_index, row in enumerate(self.BUTTON_LAYOUT):
            column_index = 0
            for button_label in row:
                button_bounds = self._get_button_bounds(row_index, column_index, button_label)
                shape_item_ids, text_x, text_anchor = self._draw_button_shape(
                    button_label, button_bounds
                )

                # The label text is a separate canvas item placed on top of the
                # button shape.
                text_item_id = self.drawing_area.create_text(
                    text_x,
                    (button_bounds["top"] + button_bounds["bottom"]) / 2,
                    text=button_label,
                    fill=self._get_button_text_color(button_label),
                    anchor=text_anchor,
                    font=(self.DISPLAY_FONT_FAMILY, self.BUTTON_FONT_SIZE),
                )

                # Register both the shape and the label as clickable.
                self._make_canvas_items_clickable(button_label, (*shape_item_ids, text_item_id))
                column_index += 2 if button_label == self.ZERO_LABEL else 1

    def _get_button_bounds(self, row_index, column_index, button_label):
        """Return the screen coordinates for one button.

        A small dictionary is beginner-friendly here because the returned values
        can be read by name: `left`, `top`, `right`, and `bottom`.
        """
        button_step = self.BUTTON_DIAMETER + self.BUTTON_GAP
        is_zero_button = button_label == self.ZERO_LABEL
        button_width = self.BUTTON_DIAMETER * 2 + self.BUTTON_GAP if is_zero_button else self.BUTTON_DIAMETER

        left = self.BUTTON_LEFT + column_index * button_step
        top = self.BUTTON_TOP + row_index * button_step

        return {
            "left": left,
            "top": top,
            "right": left + button_width,
            "bottom": top + self.BUTTON_DIAMETER,
        }

    def _draw_button_shape(self, button_label, bounds):
        """Draw one button shape and return its canvas item IDs.

        The 0 key is a pill; every other key is a circle.
        """
        if button_label == self.ZERO_LABEL:
            shape_item_ids = self._create_pill_button(
                bounds["left"],
                bounds["top"],
                bounds["right"],
                bounds["bottom"],
                radius=self.BUTTON_DIAMETER / 2,
                fill=self._get_button_color(button_label),
            )
            text_x = bounds["left"] + self.BUTTON_TEXT_OFFSET_FOR_ZERO
            text_anchor = "w"
        else:
            shape_item_ids = (
                self.drawing_area.create_oval(
                    bounds["left"],
                    bounds["top"],
                    bounds["right"],
                    bounds["bottom"],
                    fill=self._get_button_color(button_label),
                    outline=self.BUTTON_OUTLINE_COLOR,
                    width=self.BUTTON_OUTLINE_WIDTH,
                ),
            )
            text_x = (bounds["left"] + bounds["right"]) / 2
            text_anchor = "center"

        return shape_item_ids, text_x, text_anchor

    def _create_pill_button(self, left, top, right, bottom, radius, fill):
        """Create a pill-shaped button from simple canvas pieces.

        Tkinter Canvas does not have a built-in rounded rectangle primitive.
        This method builds one from two circles and one rectangle.
        """
        left_circle = self.drawing_area.create_oval(
            left,
            top,
            left + radius * 2,
            bottom,
            fill=fill,
            outline=self.BUTTON_OUTLINE_COLOR,
            width=self.BUTTON_OUTLINE_WIDTH,
        )
        right_circle = self.drawing_area.create_oval(
            right - radius * 2,
            top,
            right,
            bottom,
            fill=fill,
            outline=self.BUTTON_OUTLINE_COLOR,
            width=self.BUTTON_OUTLINE_WIDTH,
        )
        middle = self.drawing_area.create_rectangle(
            left + radius,
            top,
            right - radius,
            bottom,
            fill=fill,
            outline=fill,
        )
        return (left_circle, right_circle, middle)

    def _make_canvas_items_clickable(self, button_label, item_ids):
        """Make a button's shape and label respond to mouse clicks."""
        self.button_items.append((button_label, item_ids))

        for item_id in item_ids:
            # tag_bind connects a canvas item to an event handler. Here, a
            # mouse click calls `handle_input()` with the button's label.
            self.drawing_area.tag_bind(
                item_id,
                "<Button-1>",
                lambda _event, value=button_label: self.handle_input(value),
            )
            self.drawing_area.tag_bind(
                item_id,
                "<Enter>",
                lambda _event: self.drawing_area.config(cursor="hand2"),
            )
            self.drawing_area.tag_bind(
                item_id,
                "<Leave>",
                lambda _event: self.drawing_area.config(cursor=""),
            )

    def _bind_keyboard_shortcuts(self):
        """Connect keyboard keys to calculator actions."""
        # Key bindings make the GUI feel natural: number keys type numbers,
        # Enter evaluates, Backspace deletes, and Escape clears.
        self.window.bind("<Key>", self._handle_keyboard_input)
        self.window.bind("<Return>", lambda _event: self.handle_input(self.EQUALS_LABEL))
        self.window.bind("<BackSpace>", lambda _event: self.delete_last_character())
        self.window.bind("<Escape>", lambda _event: self.clear())

    def _get_button_color(self, button_label):
        """Return the background color for a button label."""
        if button_label in self.OPERATOR_LABELS or button_label == self.EQUALS_LABEL:
            return self.OPERATOR_BUTTON_COLOR
        if button_label in self.UTILITY_LABELS:
            return self.UTILITY_BUTTON_COLOR
        return self.NUMBER_BUTTON_COLOR

    def _get_button_text_color(self, button_label):
        """Return the text color for a button label."""
        if button_label in self.UTILITY_LABELS:
            return self.BLACK_TEXT
        return self.WHITE_TEXT

    def _handle_keyboard_input(self, event):
        """Convert a keyboard event into the same action as a button click."""
        if event.char in self.KEYBOARD_INPUTS:
            self.handle_input(event.char)

    def handle_input(self, button_value):
        """Route one button value to the correct calculator operation."""
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

    def enter_digit_decimal_or_operator(self, button_value):
        """Handle digit, decimal point, and operator input.

        Despite the method name, the calculator does not display the whole
        expression. It displays only the current operand, which is closer to how
        simple physical calculators work.
        """
        if self.display_text == "Error":
            self.clear()

        # Operators are handled separately because they store the first number
        # and prepare the calculator to accept the second number.
        if button_value in self.OPERATOR_LABELS:
            self.select_operator(button_value)
            return

        # After a completed result or after an operator, the next digit starts
        # a fresh operand instead of appending to the previous display.
        if self.has_just_evaluated or self.is_waiting_for_next_operand:
            self._start_new_operand()

        if button_value == self.DECIMAL_LABEL:
            self._append_decimal_point()
        elif not self._has_reached_input_limit():
            self._append_digit(button_value)

        self.update_display(self.current_operand)

    def _start_new_operand(self):
        """Prepare the calculator to type a new operand."""
        self.current_operand = "0"
        self.has_just_evaluated = False
        self.is_waiting_for_next_operand = False

    def _append_decimal_point(self):
        """Append a decimal point if the current operand does not have one."""
        if self.DECIMAL_LABEL not in self.current_operand:
            self.current_operand += self.DECIMAL_LABEL

    def _append_digit(self, digit):
        """Append one digit, replacing the initial zero when appropriate."""
        if self.current_operand == self.ZERO_LABEL:
            self.current_operand = digit
        else:
            self.current_operand += digit

    def select_operator(self, operator):
        """Store the selected operator and prepare for the second operand."""
        # If the user enters `2 + 3 +`, calculate `2 + 3` first, then store the
        # next `+` as the new pending operator.
        if self.selected_operator and not self.is_waiting_for_next_operand:
            self.evaluate()

        if self.display_text == "Error":
            self.clear()
            return

        # Store the first number and the operator. The display clears to 0 so
        # the second operand can use the full screen.
        self.left_operand = float(self.current_operand)
        self.selected_operator = operator
        self.is_waiting_for_next_operand = True
        self.has_just_evaluated = False
        self.update_display("0")

    def clear(self):
        """Reset all calculator state back to the initial value."""
        self._reset_calculator_state()
        self._refresh_display()

    def delete_last_character(self):
        """Delete the latest typed character from the current operand."""
        if self.is_waiting_for_next_operand or self.has_just_evaluated:
            return

        self.current_operand = self.current_operand[:-1] or self.ZERO_LABEL
        self.has_just_evaluated = False
        self.update_display(self.current_operand)

    def toggle_sign(self):
        """Switch the current operand between positive and negative."""
        try:
            if self.current_operand:
                self.current_operand = self._format_number(-float(self.current_operand))
                self.has_just_evaluated = False
                self.update_display(self.current_operand)
        except ValueError:
            self._show_error()

    def convert_to_percent(self):
        """Convert the current operand into a percentage."""
        try:
            if self.current_operand:
                self.current_operand = self._format_number(float(self.current_operand) / 100)
                self.has_just_evaluated = False
                self.update_display(self.current_operand)
        except ValueError:
            self._show_error()

    def evaluate(self):
        """Calculate the pending operation and show the result."""
        # Pressing equals repeatedly after a result should not change anything.
        if self.has_just_evaluated:
            return

        # If there is no complete operation yet, just keep showing the current
        # number.
        if self.left_operand is None or self.selected_operator is None:
            self.update_display(self.current_operand)
            return

        try:
            result = self._calculate(
                self.left_operand,
                self.selected_operator,
                float(self.current_operand),
            )
        except ZeroDivisionError:
            self._show_error()
            return

        self.current_operand = self._format_number(result)
        self.left_operand = None
        self.selected_operator = None
        self.is_waiting_for_next_operand = False
        self.has_just_evaluated = True
        self.update_display(self.current_operand, is_result=True)

    def update_display(self, value, is_result=False):
        """Update the visible display text while keeping it inside bounds."""
        self.display_text = value or self.ZERO_LABEL

        if len(self.display_text) > self.MAX_DISPLAY_CHARS:
            if is_result:
                # Final results can be shown in scientific notation.
                self.display_text = self._format_scientific(float(value))
            else:
                # Typed operands are capped so they do not overflow the screen.
                self.display_text = self.display_text[: self.MAX_DISPLAY_CHARS]

        self._refresh_display()

    def _has_reached_input_limit(self):
        """Return True when the current operand has reached its digit limit."""
        visible_digits = self.current_operand.replace("-", "").replace(".", "")
        return len(visible_digits) >= self.MAX_INPUT_DIGITS

    def _refresh_display(self):
        """Redraw the calculator result text."""
        self.drawing_area.itemconfig(
            self.display_text_item,
            text=self.display_text,
            font=(self.DISPLAY_FONT_FAMILY, self._get_display_font_size()),
        )

    def _get_display_font_size(self):
        """Return a display font size based on the current text length."""
        text_length = len(self.display_text)
        if text_length <= 6:
            return self.DISPLAY_FONT_LARGE
        if text_length <= 8:
            return self.DISPLAY_FONT_MEDIUM
        if text_length <= 10:
            return self.DISPLAY_FONT_SMALL
        return self.DISPLAY_FONT_EXTRA_SMALL

    def _show_error(self):
        """Show an error message and reset the calculator's internal state."""
        self._reset_calculator_state()
        self.display_text = "Error"
        self._refresh_display()

    def _format_number(self, value):
        """Convert a number to display text without unnecessary `.0` endings."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def _format_scientific(self, value):
        """Format very large or tiny results using calculator-style notation."""
        scientific = f"{value:.5e}"
        mantissa, exponent = scientific.split("e")
        mantissa = mantissa.rstrip("0").rstrip(".")
        exponent_number = int(exponent)
        return f"{mantissa}e{exponent_number:+d}"

    def _calculate(self, first_number, operator, second_number):
        """Apply one arithmetic operation to two numbers."""
        if operator == "+":
            return first_number + second_number
        if operator == "-":
            return first_number - second_number
        if operator == "*":
            return first_number * second_number
        if operator == "/":
            if second_number == 0:
                raise ZeroDivisionError
            return first_number / second_number
        return second_number

    def run(self):
        """Start Tkinter's event loop.

        `mainloop()` keeps the window open and waits for user events like
        clicks, key presses, and window-close actions.
        """
        self.window.mainloop()


if __name__ == "__main__":
    # This block runs only when the file is executed directly:
    # `python3 simple_calculator.py`
    CalculatorApp().run()
