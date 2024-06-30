from tkinter import *
import string
import random

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")

        # Create the label and entry for password length
        self.length_label = Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=5, pady=5)

        self.length_entry = Entry(master, width=10)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create the checkboxes for password options
        self.include_uppercase = BooleanVar()
        self.include_lowercase = BooleanVar()
        self.include_numbers = BooleanVar()
        self.include_special = BooleanVar()

        self.uppercase_checkbox = Checkbutton(master, text="Include Uppercase", variable=self.include_uppercase)
        self.uppercase_checkbox.grid(row=1, column=0, padx=5, pady=5)

        self.lowercase_checkbox = Checkbutton(master, text="Include Lowercase", variable=self.include_lowercase)
        self.lowercase_checkbox.grid(row=1, column=1, padx=5, pady=5)

        self.numbers_checkbox = Checkbutton(master, text="Include Numbers", variable=self.include_numbers)
        self.numbers_checkbox.grid(row=2, column=0, padx=5, pady=5)

        self.special_checkbox = Checkbutton(master, text="Include Special Characters", variable=self.include_special)
        self.special_checkbox.grid(row=2, column=1, padx=5, pady=5)

        # Create the generate button
        self.generate_button = Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Create the password display label
        self.password_label = Label(master, text="")
        self.password_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def generate_password(self):
        # Get the desired password length from the user
        try:
            length = int(self.length_entry.get())
        except ValueError:
            self.password_label.config(text="Please enter a valid number.")
            return

        # Define the character sets based on the selected options
        characters = ""
        if self.include_uppercase.get():
            characters += string.ascii_uppercase
        if self.include_lowercase.get():
            characters += string.ascii_lowercase
        if self.include_numbers.get():
            characters += string.digits
        if self.include_special.get():
            characters += string.punctuation

        # Generate the password
        if characters:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_label.config(text=f"Your password is: {password}")
        else:
            self.password_label.config(text="Please select at least one character type.")

root = Tk()
#root.geometry("400x100")
password_generator = PasswordGenerator(root)
root.mainloop()
