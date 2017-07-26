## Email

Email configuration options are available from the Timestrap admin on a 
per-site basis. These settings must be supplied to support features such as
password reset. To access the settings, navigate to `/admin/sites/site/` and
select the site to modify.

If you are using Heroku you can add `sendgrid` to your apps addons on the 
Heroku admin panel or by running:

    heroku addons:create sendgrid
