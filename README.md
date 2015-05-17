About
=====

`uberspace_vpasswd` is a very simple [Flask](http://flask.pocoo.org/)
application that allows a user to change the password of her
[Uberspace](https://uberspace.de) email account via a web form.

This avoids the necessity of shell access to change the password directly.


How
---

The server side validates the provided password against the configured `IMAP`
server and sets the new password through the `vpasswd` binary.


Deployment
==========

 0. SSH into your account
 1. Checkout the project

        $ cd /var/www/virtual/$USER/
        $ git clone https://github.com/0x64746b/uberspace_vpasswd.git
        $ cd uberspace_vpasswd

 2. Adjust the `config.py`

    1. Configure the domain of the email accounts
    2. Configure the IMAP server
    3. Generate 2 strong secrets to derive session keys and CSRF nonces from

 3. Create a `fcgi` file

    1. Copy the provided `vpasswd.fcgi.template`

            $ cp vpasswd.fcgi.template ../fcgi-bin/vpasswd.fcgi
            $ cd ../fcgi-bin/

    2. Adjust the `fcgi` file

        1. Configure the path to your `python` binary
        2. Configure the path to the project checkout
