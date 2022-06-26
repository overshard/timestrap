# Configuration

## Security

By default we don't enable TLS/SSL features since this project is often run on
an intranet, locally, or in testing environments. If security is a concern of
yours, and it should be, you will need to enable TLS/SSL on your reverse proxy
and setup a certificate there. For an easy TLS enabled reverse proxy check out
Caddy.

You will need to configure two settings when you use TLS/SSL on this project.
The first is to force TLS/SSL when people visit your site and the second is to
make sure that Django REST framework returns corrected URLs behind a reverse
proxy. These can be added to `timestrap/settings/base.py` anywhere:

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

## Email

Email configuration options are available from the Timestrap admin on a
per-site basis. These settings must be supplied to support features such as
password reset. To access the settings, navigate to `/admin/sites/site/` and
select the site to modify.

### Email Docker

You can configure email by setting environmental variables in the
`docker-compose` config for `web`. These would be:

- **EMAIL_HOST**
- **EMAIL_HOST_USER**
- **EMAIL_HOST_PASSWORD**
- **EMAIL_PORT** defaults to port `25`
- **EMAIL_USE_TLS** defaults to `False`, you can set this to `True`

These would go where the `SECRET_KEY` environmental variable is set

## Time and Date Localization

Language and timezone settings are available on a per-site basis in the site
configuration area (`/admin/sites/site/`). Timestrap uses [Moment.js](http://momentjs.com/)
on the frontend so localization will be applied to all dates based on these
settings. We'd like to eventually have localization of everything.
