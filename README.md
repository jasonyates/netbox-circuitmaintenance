=================================
# Netbox Circuit Maintenance Plugin
=================================

NetBox plugin for managing Circuit Maintenance events.


* Free software: Apache-2.0
* This plugin is still in development. Use at your own risk.


## Features

Provides the ability to record circuit maintenance, maintenance impact and maintenance notifications in Netbox and link them to Providers and Circuits.

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
|     3.4        |      0.1.0     |

## Installing

While this is still in development and not yet on pypi you can install with pip:

```bash
pip install git+https://github.com/jasonyates/netbox_circuitmaintenance
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com/jasonyates/netbox_circuitmaintenance
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'netbox_circuitmaintenance'
]

PLUGINS_CONFIG = {
    "netbox_circuitmaintenance": {},
}
```

## Credits

Based on the NetBox plugin tutorial:

- [demo repository](https://github.com/netbox-community/netbox-plugin-demo)
- [tutorial](https://github.com/netbox-community/netbox-plugin-tutorial)

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin) project template.
