## Password Resets and Email

To support email for things like password resetting you need to update
Timestrap's settings. I will not presume your email situation and allow you to
do this yourself by reading [Django's documentation](https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend).

If you are using Heroku you can add `sendgrid` to your apps addons on the 
Heroku admin panel or by running:

    heroku addons:create sendgrid

You then need to add these settings to `timestrap/settings/heroku.py`:

    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
