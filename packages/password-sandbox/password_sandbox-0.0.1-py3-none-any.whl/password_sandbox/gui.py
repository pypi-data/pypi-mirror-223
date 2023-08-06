import tkinter as tk
from tkinter import *
import secrets
import string

def generate_password():
    # Create a new window
    window = tk.Toplevel()
    window.title("Generate Password")
    window.geometry("275x150")
    window.resizable(False, False)
    root.eval(f'tk::PlaceWindow {str(window)} center')

    # Create a label and entry for the length
    length_label = tk.Label(window, text="Number of characters:")
    length_label.pack(pady=10)
    length_entry = tk.Entry(window)
    length_entry.pack()

    # Generate the password when this button is clicked
    def generate():
        # Check if the length is numeric
        number_of_characters = length_entry.get()
        if not number_of_characters.isdigit():
            error_label.config(text="Error: Please enter a numeric value")
            return
        else:
            error_label.config(text="")
        number_of_characters = int(number_of_characters)
        # Generate the password
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(number_of_characters))
        # Create a new window for the password
        password_window = tk.Toplevel()
        password_window.title("Generated Password")
        root.eval(f'tk::PlaceWindow {str(password_window)} center')
        password_window.geometry("275x100")
        # Display the password
        password_label = tk.Label(password_window, text=f"Your password is:\n{password}")
        password_label.pack(pady=10)
        # Copy the password to the clipboard when this button is clicked
        def copy_password():
            password_window.clipboard_clear()
            password_window.clipboard_append(password)
        copy_button = tk.Button(password_window, text="Copy to Clipboard", command=copy_password)
        copy_button.pack(pady=10)

    # Create a button to generate the password
    generate_button = tk.Button(window, text="Generate Password", command=generate)
    generate_button.pack(pady=10)
    error_label = tk.Label(window, text="", fg="red")
    error_label.pack(pady=10)
    window.mainloop()

def test_password_strength():
    def test():
        try:
            import zxcvbn
        except ModuleNotFoundError:
            result_label.config(text="The zxcvbn module is not installed. You can install it by running 'pip install zxcvbn-python' in the terminal.")
            return

        password = password_entry.get()

        if password == "":
            result_label.config(text="Error: Please enter a password", fg="red")
            return
        else:
            result = zxcvbn.zxcvbn(password)
            result_label.config(text="Your password is strong.", fg="green")
            time_to_crack = result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
            time_label.config(text=f"Estimated time to crack password: {time_to_crack}")

            if result['score'] < 3:
                result_label.config(text="Your password is weak.", fg="red")
                feedback = result['feedback']['warning']
                suggestions = " ".join(result['feedback']['suggestions'])
                feedback_label.config(text=f"Password strength feedback:\n{feedback}")
                suggestions_label.config(text=f"Password suggestions:\n{suggestions}")
            else:
                feedback_label.config(text="")
                suggestions_label.config(text="")
    window = tk.Toplevel()
    window.title("Test Password Strength")
    window.resizable(False, False)
    root.eval(f'tk::PlaceWindow {str(window)} center')
    password_entry = tk.Entry(window)
    password_entry.pack(padx=10, pady=10)
    test_button = tk.Button(window, text="Test Password Strength", command=test)
    test_button.pack(pady=10, padx=80)
    result_label = tk.Label(window, text="")
    result_label.pack()
    time_label = tk.Label(window, text="")
    time_label.pack()
    feedback_label = tk.Label(window, text="")
    feedback_label.pack()
    suggestions_label = tk.Label(window, text="")
    suggestions_label.pack(padx=10, pady=10)
    window.mainloop()
    
# Add an About window
def show_about_window():
    window = tk.Toplevel()
    window.title("About")
    window.geometry("275x110")
    window.resizable(False, False)
    root.eval(f'tk::PlaceWindow {str(window)} center')
    about_label = tk.Label(window, text="Password Manager\nVersion 1.0.0\n\nCreated by: Thibault Savenkoff\n\n© 2023 Thibault Savenkoff")
    about_label.pack(padx=10, pady=10)
    window.mainloop()

def about():
    show_about_window()

root = tk.Tk()
root.title("Password Manager")
root.geometry("275x130")
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)

menubar = Menu(root)
root.config(menu=menubar)

about_menu = Menu(menubar, tearoff=False)

about_menu.add_command(
    label='About',
    command=about,
)

menubar.add_cascade(
    label="File",
    menu=about_menu,
    underline=0
)

label = tk.Label(root, text="Select an option:")
label.pack(padx=10, pady=5)

button_a = tk.Button(root, text="Generate a random password", command=generate_password)
button_a.pack(padx=10, pady=5)

button_b = tk.Button(root, text="Test the strength of your password", command=test_password_strength)
button_b.pack(padx=10, pady=5)

root.mainloop()