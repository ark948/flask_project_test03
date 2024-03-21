# this file is just to demonstrate the use of current_app instead of app
# use current_app when there is no global app variable available
# from flask import current_app

from flask_mail import Message
from app import mail
from flask import current_app, render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[flask_app] Reset your password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token)
               )
    
def send_verfiy_email_request_email(user):
    token = user.get_verify_email_token()
    send_email('[flask_app] Please verify your email',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/verify_email.txt', user=user, token=token),
               html_body=render_template('email/verify_email.html', user=user, token=token)
               )