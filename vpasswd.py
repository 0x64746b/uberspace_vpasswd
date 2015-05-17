#!/usr/bin/env python
# coding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import imaplib
import logging

from flask import flash, Flask, redirect, render_template, request, url_for
from flask_wtf import Form
import pexpect
from wtforms import TextField, PasswordField, ValidationError, validators


app = Flask(__name__)
app.config.from_object('config')


logging.basicConfig(
    filename=app.config['LOG_FILE'],
    level=app.config['LOG_LEVEL']
)


class PasswordChangeForm(Form):

    def correct_domain(form, field):
        suffix = '@' + app.config['DOMAIN']
        if not field.data.endswith(suffix):
            raise ValidationError('Adresse muss auf "{}" enden'.format(suffix))

    email = TextField(
        'E-Mail',
        [
            validators.Email('Ungültige E-Mail-Adresse'),
            correct_domain,
        ]
    )

    current_password = PasswordField(
        'Aktuelles Passwort',
        [
            validators.Required('Du musst Dein aktuelles Passwort angeben'),
        ]
    )

    new_password = PasswordField(
        'Neues Passwort',
        [
            validators.Length(
                min=16,
                message='Dein neues Passwort muss mindestens 16 Zeichen lang'
                        ' sein',
            ),
            validators.EqualTo(
                'confirmed_password',
                message='Passwörter stimmen nicht überein'
            )
        ]
    )

    confirmed_password = PasswordField('Wiederholung')


@app.route('/', methods=['GET', 'POST'])
def change_password():
    form = PasswordChangeForm(request.form)
    domain = app.config['DOMAIN']

    if request.method == 'POST' and form.validate():
        email, current_password = form.email.data, form.current_password.data
        user, new_password = email.split('@')[0], form.new_password.data

        if not _credentials_are_valid(email, current_password):
            flash('Ungültige Kombination aus E-Mail und Passwort', 'danger')
        else:
            try:
                _set_new_password(user, new_password)
            except (EnvironmentError, pexpect.ExceptionPexpect) as error:
                flash(
                    'Setzen des neuen Passworts ist fehlgeschlagen',
                    'danger'
                )
                logging.error(error.message)
            else:
                flash('Passwort wurde erfolgreich geändert!', 'success')
                return redirect(url_for('change_password'))

    return render_template('index.html', form=form, domain=domain)


def _credentials_are_valid(email, password):
    imap_server = imaplib.IMAP4_SSL(app.config['UBERSPACE_SERVER'])

    try:
        imap_server.login(email, password)
    except imaplib.IMAP4.error:
        return False
    else:
        imap_server.logout()
        return True


def _set_new_password(user, password):
    vpasswd = pexpect.spawn(
        command='vpasswd',
        args=[user],
        env={'HOME': app.config['HOME']}
    )

    vpasswd.expect('password:')
    vpasswd.sendline(password)

    vpasswd.expect('verification:')
    vpasswd.sendline(password)

    vpasswd.expect(pexpect.EOF)
    vpasswd.close()

    if vpasswd.exitstatus != 0:
        last_line = filter(None, vpasswd.before.split('\r\n'))[-1]
        problem = last_line.split(':')[-1]

        raise EnvironmentError(
            '`{}` exited with code {}: {}'.format(
                command,
                vpasswd.exitstatus,
                problem,
            )
        )


if __name__ == '__main__':
    app.run()
