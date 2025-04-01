import re
import tkinter as tk
from tkinter import scrolledtext

# Global counters and storage
temp_var_count = 0
instruction_count = 1
instructions = []

def new_temp():
    """Generate a new temporary variable."""
    global temp_var_count
    temp_var = f"t{temp_var_count}"
    temp_var_count += 1
    return temp_var

def print_instruction(instruction):
    """Append generated TAC instruction to the list with an instruction number."""
    global instruction_count
    instructions.append(f"{instruction_count}) {instruction}")
    instruction_count += 1

def generate_tac(code):
    """
    Generate Three-Address Code (TAC) for the given input code.
    Handles assignments, if-else statements, while loops, and nested structures.
    """
    global instruction_count, instructions, temp_var_count
    # Reset global counters for each generation run
    temp_var_count = 0
    instruction_count = 1
    instructions = []
    
    lines = code.strip().split("\n")
    stack = []  # Stack to manage control flow labels

    for line in lines:
        line = line.strip()
        if line.startswith("if"):
            # Extract condition between parentheses
            condition = re.search(r"if\s*\((.*?)\)", line).group(1)
            # Split condition on &&
            conditions = re.split(r'\s*&&\s*', condition)
            # Create labels for else and end
            label_else = instruction_count + len(conditions) * 2  # After all condition checks
            label_end = label_else + 1  # After else block or empty then block
            stack.append(label_else)  # Save else label for later use
            
            # Generate TAC for each condition with short-circuit evaluation
            for i, cond in enumerate(conditions):
                next_check = instruction_count + 2  # Next condition or then block
                if i == len(conditions) - 1:
                    # Last condition: if true, goto then (or end if empty); else goto else
                    print_instruction(f"if {cond} goto {label_else}")
                else:
                    # Intermediate condition: if true, goto next condition; else goto else
                    print_instruction(f"if {cond} goto {next_check}")
                print_instruction(f"goto {label_end}")
        
        elif line.startswith("while"):
            # Extract condition between parentheses
            condition = re.search(r"while\s*\((.*?)\)", line).group(1)
            # Mark the beginning of the loop with a label
            loop_start = instruction_count
            # Split the condition into parts
            conditions = re.split(r'\s*&&\s*', condition)
            # Create labels for loop body and exit
            label_body = instruction_count + len(conditions) * 2
            label_exit = label_body + 1
            # Generate TAC for each condition
            for i, cond in enumerate(conditions):
                next_check = instruction_count + 2
                if i == len(conditions) - 1:
                    print_instruction(f"if {cond} goto {label_body}")
                else:
                    print_instruction(f"if {cond} goto {next_check}")
                print_instruction(f"goto {label_exit+1}")
            stack.append((loop_start, label_exit))
        
        elif line == "} else {":
            # End of if-part; start of else-part
            else_label = stack.pop()
            label_end = instruction_count + 1
            print_instruction(f"goto {label_end}")
            stack.append(label_end)
        
        elif line == "}":
            # End of a block
            if stack:
                top = stack.pop()
                if isinstance(top, tuple):
                    # End of a while loop block
                    loop_start, exit_label = top
                    print_instruction(f"goto {loop_start}")
        
        elif "=" in line:
            # Handle assignment statements
            var, expr = line.split("=")
            var = var.strip()
            expr = expr.strip()
            # Check if the expression is a binary operation
            tokens = re.split(r'(\+|\-|\*|/)', expr)
            if len(tokens) == 3:
                operand1 = tokens[0].strip()
                operator = tokens[1].strip()
                operand2 = tokens[2].strip()
                temp_var = new_temp()
                print_instruction(f"{temp_var} = {operand1} {operator} {operand2}")
                print_instruction(f"{var} = {temp_var}")
            else:
                print_instruction(f"{var} = {expr}")

    print_instruction("END")
    return "\n".join(instructions)

def generate_tac_gui():
    """GUI event handler to generate TAC from input."""
    input_code = input_text.get("1.0", tk.END).strip()
    if input_code:
        tac_output = generate_tac(input_code)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, tac_output)
        output_text.config(state=tk.DISABLED)

# GUI Setup using tkinter
root = tk.Tk()
root.title("Three-Address Code Generator")
root.geometry("600x500")

input_label = tk.Label(root, text="Enter Code (If-Else & Loops):", font=("Arial", 12))
input_label.pack()

input_text = scrolledtext.ScrolledText(root, height=10, width=70)
input_text.pack()

generate_button = tk.Button(root, text="Generate TAC", command=generate_tac_gui, font=("Arial", 12))
generate_button.pack(pady=5)

output_label = tk.Label(root, text="Generated Three-Address Code:", font=("Arial", 12))
output_label.pack()

output_text = scrolledtext.ScrolledText(root, height=10, width=70)
output_text.pack()
output_text.config(state=tk.DISABLED)

root.mainloop()