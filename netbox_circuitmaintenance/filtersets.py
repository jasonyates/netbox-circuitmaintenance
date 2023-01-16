from netbox.filtersets import NetBoxModelFilterSet
from .models import CircuitMaintenance


# class circuitmaintenanceFilterSet(NetBoxModelFilterSet):
#
#     class Meta:
#         model = circuitmaintenance
#         fields = ['name', ]
#
#     def search(self, queryset, name, value):
#         return queryset.filter(description__icontains=value)
