import json
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip

from code_data import letters, numbers, symbols

BLUE = "#62CDFF"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    new_letters = [choice(letters) for letter in range(randint(8, 10))]
    new_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    new_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = new_letters + new_symbols + new_numbers
    shuffle(password_list)

    password = "".join(password_list)

    input_password.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ----------------------------------- #
def save():
    website_name = input_website.get()
    email_name = input_email.get()
    password_name = input_password.get()
    new_data = {website_name: {"email": email_name, "password": password_name}}

    if len(website_name) == 0 or len(password_name) == 0 or len(email_name) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    else:
        is_ok_to_save = messagebox.askokcancel(
            title="Alert",
            message=f"These are details entered: \nWebsite: {website_name} \nEmail: {email_name} \nPassword:{password_name} \nIs it ok to save?",
        )

        if is_ok_to_save:
            try:
                with open(
                    "data.json",
                    mode="r",
                ) as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(
                    "data.json",
                    mode="w",
                ) as data_file:
                    # Write new data to data file
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updating old data with new data- łączę dwa słowniki data i new_data w jedno
                data.update(new_data)

                with open(
                    "data.json",
                    mode="w",
                ) as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                input_website.delete(0, END)
                # input_email.delete(0,END)
                input_password.delete(0, END)


# ---------------------------- FIND PASSWORD  ---------------------------------------#
def find_password():
    try:
        with open(
            "data.json",
            mode="r",
        ) as data_file:
            data = json.load(data_file)
            website_name = input_website.get()
            website_email = data[website_name]["email"]
            website_password = data[website_name]["password"]
    except KeyError:
        messagebox.showinfo(
            title="Error", message=f"No details for the {website_name} exists"
        )
    except FileNotFoundError:
        messagebox.showinfo(title="Alert", message="No data file found")
    else:
        messagebox.showinfo(
            title=website_name,
            message=f"Email: {website_email}\nPassword: {website_password}",
        )


# ---------------------------- UI SETUP ----------------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
logo_image = PhotoImage(
    file="logo.png"
)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels:
website_label = Label(text="Website: ", bg="white", fg="black")
website_label.config(padx=5, pady=5)
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username: ", bg="white", fg="black")
email_username_label.config(padx=5, pady=5)
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password", bg="white", fg="black")
password_label.config(padx=5, pady=5)
password_label.grid(column=0, row=3)

# Inputs:
input_website = Entry(
    width=17,
    bd=1,
    bg="white",
    fg="black",
    highlightthickness=1,
    highlightbackground="white",
    highlightcolor=BLUE,
)
input_website.grid(column=1, row=1)
input_website.focus()


input_email = Entry(
    width=34,
    bd=1,
    bg="white",
    fg="black",
    highlightthickness=1,
    highlightbackground="white",
    highlightcolor=BLUE,
)
input_email.grid(column=1, row=2, columnspan=2)
input_email.insert(0, "someoneemail@gmail.com")

input_password = Entry(
    width=17,
    bd=1,
    bg="white",
    fg="black",
    highlightthickness=1,
    highlightbackground="white",
    highlightcolor=BLUE,
)
input_password.grid(column=1, row=3)


# Buttons:
generate_password_button = Button(
    text="Generate Password", highlightbackground="white", command=generate_password
)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", highlightbackground="white", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(
    text="Search", highlightbackground="white", command=find_password
)
search_button.grid(column=2, row=1)

window.mainloop()
