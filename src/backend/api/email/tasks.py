import os
from flask import render_template
from flask_mail import Message

from api import app, celery
from api.email import mail

@celery.task
def deliver_email(template, subject, name, email, link):
    """
    Send a contact e-mail.
    :param email: E-mail address of the visitor
    :type user_id: str
    :param message: E-mail message
    :type user_id: str
    :return: None
    """
    msg = Message(
        subject=subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )

    try:
        with app.app_context():
            msg.html = render_template(template, link=link, name=name)
            mail.send(msg)
    except TimeoutError:
        with app.app_context():
            msg.html = render_template(template, link=link, name=name)
            mail.send(msg)
