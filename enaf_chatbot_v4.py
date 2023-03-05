import requests
import tkinter as tk
import webbrowser
import json
import functools
import tkinter.simpledialog as simpledialog
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

def open_link(event, link, auth_required):
    if auth_required:
        # Get the authentication details from the user using a password dialog box
        username = simpledialog.askstring(title="Login", prompt="Enter your username:")
        password = simpledialog.askstring(title="Login", prompt="Enter your password:", show="*")

        # Make the request with the authentication headers
        response = requests.get(link, auth=(username, password), verify=True)
        content = response.content.decode("utf-8")

        # Open the content in a new window
        window = tk.Toplevel()
        text_widget = tk.Text(window)
        text_widget.pack()
        text_widget.insert(tk.END, content)

    else:
        # Open the link in the user's default web browser
        webbrowser.open_new(link)

def email_link(event, link):
    # Get the user's email address using a simpledialog
    email_address = simpledialog.askstring(title="Email Link", prompt="Enter your email address:")

    # Check if the email address is valid using a regular expression
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
        result_label.config(text="Invalid email address")
        return

    # Create the email message
    message = MIMEMultipart()
    message["From"] = "noreply@example.com"
    message["To"] = email_address
    message["Subject"] = "Form Link"
    body = f"Here is the link to the form: {link}"
    message.attach(MIMEText(body, "plain"))

    # Send the email using the Gmail SMTP server
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('your-email@gmail.com', 'your-password')
        server.send_message(message)
        server.quit()
        result_label.config(text="Link emailed to " + email_address)
    except:
        result_label.config(text="Error sending email")

def search_button_clicked():
    user_input = input_entry.get()

    # Validate user input to prevent SQL injection and XSS attacks
    if not re.match(r"^[a-zA-Z0-9\s]+$", user_input):
        result_label.config(text="Invalid input detected")
        return

    form_name, form_link, auth_required = search_for_form(user_input)
    if form_name and form_link:
        # Use https instead of http in the URLs of the eNAF forms
        form_link = form_link.replace('http://', 'https://')
        
        result_label.config(text=f"Here's the {form_name} form! Click {form_link} to access the form.")
        link_label = tk.Label(result_label, text=form_link, fg="blue", cursor="hand2")
        link_label.pack(side="left")
        link_label.bind("<Button-1>", functools.partial(open_link, link=form_link, auth_required=auth_required))
    else:
        result_label.config(text="Contact Help Desk XXX-XXX-XXXX")

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
 
       
       
