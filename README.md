=================================
# Netbox Circuit Maintenance Plugin
=================================

NetBox plugin for managing Circuit Maintenance events.

See Github Feature Requests for upcoming list of features.

## Features

Provides the ability to record circuit maintenance, maintenance impact and maintenance notifications in Netbox and link them to Providers and Circuits.

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     3.4        |      0.2.2     |

## Installing

A working installation of Netbox 3.4+ is required - [see official documentation](https://netbox.readthedocs.io/en/stable/plugins/).

### Package Installation from PyPi

Activate your virtual env and install via pip::

```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-circuitmaintenance
```

To ensure the Netbox Documents plugin is automatically re-installed during future upgrades, add the package to your `local_requirements.txt` :

```bash
# echo netbox-circuitmaintenance >> local_requirements.txt
```

### Enable the Plugin

In the Netbox `configuration.py` configuration file add or update the PLUGINS parameter, adding `netbox_documents`:


```python
PLUGINS = [
    'netbox_circuitmaintenance'
]

PLUGINS_CONFIG = {
    "netbox_circuitmaintenance": {},
}
```

### Apply Database Migrations

Apply database migrations with Netbox `manage.py`:

```
(venv) $ python manage.py migrate
```

### Restart Netbox

Restart the Netbox service to apply changes:

```
sudo systemctl restart netbox
```

## Screenshots

![Maintenance Event View](docs/img/maintenance.png)
![Circuit Maintenance View](docs/img/circuit_maintenance.png)
![Provider Maintenance View](docs/img/provider_maintenance.png)


## Credits

Based on the NetBox plugin tutorial:

- [demo repository](https://github.com/netbox-community/netbox-plugin-demo)
- [tutorial](https://github.com/netbox-community/netbox-plugin-tutorial)

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin) project template.
