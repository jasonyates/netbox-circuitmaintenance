from netbox.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from netbox.choices import ButtonColorChoices

menuitems = [
    PluginMenuItem(
        link='plugins:netbox_circuitmaintenance:circuitmaintenance_list',
        link_text='Maintenance Events',
        buttons=[
            PluginMenuButton(
                link='plugins:netbox_circuitmaintenance:circuitmaintenance_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN
            )
        ]
    ),
    PluginMenuItem(
        link='plugins:netbox_circuitmaintenance:maintenanceschedule',
        link_text='Maintenance Schedule',
    ),
]

menu = PluginMenu(
            label='Circuit Maintenance',
            groups=(
                ('Circuit Maintenance', menuitems),
            ),
            icon_class='mdi mdi-wrench'
        )

