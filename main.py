from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD FINDER ------------------------------- #
def find_password():
    try:
        with open("data.json") as file:
            passwords = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="No Data File Found")
    else:
        if web_entry.get() in passwords:
            messagebox.showinfo(
                title=f"{web_entry.get()}",
                message=f"Here's your details: "
                        f"\nemail: {passwords[web_entry.get()]['email']} "
                        f"\npassword: {passwords[web_entry.get()]['password']}"
            )
        else:
            messagebox.showwarning(title="Error", message=f"No details for {web_entry.get()} exists yet!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # To do this in the easy way
    password_letters = [choice(letters) for let in range(randint(8, 10))]
    password_symbols = [choice(symbols) for sym in range(randint(2, 4))]
    password_numbers = [choice(numbers) for num in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    my_password = "".join(password_list)

    password_entry.insert(0, my_password)
    pyperclip.copy(my_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        web_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get(),
        }
    }
    if len(web_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showwarning(title="Oops", message="Please, make sure you don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file_path:
                #Reading old data
                data = json.load(file_path)
        except FileNotFoundError:
            with open("data.json", "w") as file_path:
                # Saving updated data
                json.dump(new_data, file_path, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as file_path:
                #Saving updated data
                json.dump(data, file_path, indent=4)

        is_okay = messagebox.askokcancel(
            title=f"{web_entry.get()}",
            message=f"These are the details entered! \nEmail: {email_entry.get()} "
                    f"\nPassword: {password_entry.get()} \n\nIs it okay to save?"
        )
        if is_okay:
            web_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Okiki Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
website.grid(column=0, row=1)

web_entry = Entry(width=32)
web_entry.grid(column=1, row=1)
web_entry.focus()

search = Button(text="Search", width=15, command=find_password)
search.grid(column=2, row=1)

email = Label(text="Email/Username:")
email.grid(column=0, row=2)

email_entry = Entry(width=51)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "email@gmail.com")

password = Label(text="Password:")
password.grid(column=0, row=3)

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

pass_button = Button(text="Generate Password", command=password_generator)
pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)



window.mainloop()