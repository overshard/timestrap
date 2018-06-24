## Security

By default we don't enable TLS/SSL features since this project is often run on
an intranet, locally, or in testing environments. If security is a concern of
yours, and it should be, you will need to enable TLS/SSL on your reverse proxy
and setup a certificate there. On Heroku you can run `heoku certs:auto:enable`
to get a free LetsEncrypt certificate.

You will need to configure two settings when you use TLS/SSL on this project.
The first is to force TLS/SSL when people visit your site and the second is to
make sure that Django REST framework returns corrected URLs behind a reverse
proxy:

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
