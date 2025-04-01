# Three-Address Code Generator

## Overview

The Three-Address Code (TAC) Generator is a Python application that translates high-level code into Three-Address Code, which is an intermediate representation used in compiler design. This tool supports basic constructs such as assignments, if-else statements, and while loops. The application provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Features

- **Assignment Statements**: Handles simple assignments and binary operations.
- **If-Else Statements**: Supports nested if-else structures with short-circuit evaluation.
- **While Loops**: Manages while loops with multiple conditions.
- **GUI**: User-friendly interface for inputting code and viewing the generated TAC.

## Requirements

- Python 3.x
- Tkinter (usually included with Python standard library)

## Installation

1. Clone the repository or download the source code.
2. Ensure you have Python installed on your system.

## Usage

1. Run the script using Python:
   ```bash
   python tac_generator.py
   ```
2. Enter your high-level code in the input text area.
3. Click the "Generate TAC" button to see the generated Three-Address Code in the output text area.

## Code Structure

- **Global Variables**:
  - `temp_var_count`: Counter for temporary variables.
  - `instruction_count`: Counter for instructions.
  - `instructions`: List to store generated TAC instructions.

- **Functions**:
  - `new_temp()`: Generates a new temporary variable.
  - `print_instruction(instruction)`: Appends a TAC instruction to the list with an instruction number.
  - `generate_tac(code)`: Generates TAC for the given input code.
  - `generate_tac_gui()`: GUI event handler to generate TAC from input.

- **GUI Setup**:
  - Uses Tkinter to create a simple interface with input and output text areas and a button to generate TAC.

## Example

Input Code:
```plaintext
if (a > b && c < d) {
    x = a + b
} else {
    x = c - d
}
while (e > f && g < h) {
    y = e * f
}
```

Generated TAC:
```plaintext
1) if a > b goto 3
2) goto 6
3) if c < d goto 5
4) goto 6
5) t0 = a + b
6) x = t0
7) goto 8
8) t1 = c - d
9) x = t1
10) if e > f goto 12
11) goto 14
12) if g < h goto 14
13) goto 15
14) t2 = e * f
15) y = t2
16) goto 10
END
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

```