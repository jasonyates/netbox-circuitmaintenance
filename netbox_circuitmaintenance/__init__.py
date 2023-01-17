"""Top-level package for Netbox Circuit Maintenance Plugin."""

__author__ = """Jason Yates"""
__email__ = 'me@jasonyates.co.uk'
__version__ = '0.2.1'


from extras.plugins import PluginConfig


class CircuitMaintenanceConfig(PluginConfig):
    name = 'netbox_circuitmaintenance'
    verbose_name = 'Netbox Circuit Maintenance Plugin'
    description = 'Manages circuit maintenance events'
    version = __version__
    base_url = 'maintenance'


config = CircuitMaintenanceConfig
