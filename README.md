Chatbot for users to find the correct form to request permissions. This is a  work in progress!

# enaf_chatbot_V4 changes -The updated version includes several changes and additions:

    The code now imports tkinter.simpledialog to use the askstring function to display a simple password dialog box for authentication.
    The code imports re to validate user input using regular expressions to prevent SQL injection and XSS attacks.
    The code imports smtplib and the necessary modules from email.mime to allow the user to email a link to the form.
    The open_link function now takes the link argument directly instead of getting it from the widget, and it now validates the SSL certificate of the server by setting the verify parameter of the requests.get function to True.
    The email_link function uses the askstring function to get the user's email address and validates it using a regular expression. It then creates an email message using MIMEMultipart and sends it using the Gmail SMTP server.
    The search_button_clicked function now validates user input using regular expressions before searching for the form, and it replaces http with https in the URLs of the eNAF forms. It also displays a message to contact the help desk if no matching form is found.
    The result label now displays an error message if the email address is invalid or if there is an error sending the email.

These changes make the program more secure and user-friendly by adding authentication, input validation, and email functionality.

