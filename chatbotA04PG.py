import requests
import tkinter as tk
import webbrowser
import json
import functools

with open('forms.json') as f:
    forms_data = json.load(f)

def search_for_form(input_text):
    for form in forms_data['forms']:
        if 'search_terms' in form:
            for term in form['search_terms']:
                if term in input_text.lower():
                    return form['name'], form['link'], form.get('auth')
        else:
            return None, None, None
    return None, None, None

def open_link(event, auth_required):
    link = event.widget.cget("text")
    if auth_required:
        # Get the authentication details from the user
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Make the request with the authentication headers
        response = requests.get(link, auth=(username, password))
        content = response.content.decode("utf-8")

        # Open the content in a new window
        window = tk.Toplevel()
        text_widget = tk.Text(window)
        text_widget.pack()
        text_widget.insert(tk.END, content)

    else:
        # Open the link in the user's default web browser
        webbrowser.open_new(link)

def search_button_clicked():
    user_input = input_entry.get()
    form_name, form_link, auth_required = search_for_form(user_input)
    if form_name and form_link:
        result_label.config(text=f"Here's the {form_name} form! Click {form_link} to access the form.")
        link_label = tk.Label(result_label, text=form_link, fg="blue", cursor="hand2")
        link_label.pack(side="left")
        link_label.bind("<Button-1>", functools.partial(open_link, auth_required=auth_required))
    else:
        result_label.config(text="Sorry, I couldn't find a matching eNAF form, please reach out to the AHCAIT Help Desk for assistance.")

def clear_button_clicked():
    input_entry.delete(0, tk.END)
    result_label.config(text="")

def on_input_keypress(event):
    if event.keysym == "Return":
        search_button_clicked()

window = tk.Tk()
window.geometry("600x300")

input_label = tk.Label(window, text="Enter your query:")
input_label.pack()

input_entry = tk.Entry(window)
input_entry.pack()
input_entry.bind("<Key>", on_input_keypress)

search_button = tk.Button(window, text="Search", command=search_button_clicked)
search_button.pack()

clear_button = tk.Button(window, text="Clear", command=clear_button_clicked)
clear_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
