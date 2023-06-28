
# deployment
An [Apache2](https://httpd.apache.org/) is used as a front end server and [Gunicorn](https://gunicorn.org/) is used as backend production server. A [ProxyPass](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypass) directive redirect a HTTPS request to an internal HTTP IP of the app

## install Gunicorn as production backend server
```
$ source venv/bin/activate
(venv)$ pip install -r deployment/requirements.txt
```

## Gunicorn is started as system service

The subdomain of the app is defined by an environment variable ```NEUROMICS_URLPATH```. It is set to a constant value in the .service file before starting gunicorn.

```
$ sudo cp deployment/neuromics.service /etc/systemd/system/neuromics.service
$ sudo systemctl start neuromics.service
$ sudo systemctl status neuromics.service
```

## enable Apache configuration file for the app
```
$ sudo cp deployment/dashapps.conf /etc/apache2/sites-available/
$ sudo a2ensite dashapps.conf
$ sudo systemctl reload apache2.service
```

