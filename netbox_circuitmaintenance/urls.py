from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    path('circuitmaintenance/', views.CircuitMaintenanceListView.as_view(), name='circuitmaintenance_list'),

    path('circuitmaintenance/add/', views.CircuitMaintenanceEditView.as_view(), name='circuitmaintenance_add'),
    path('circuitimpact/add/', views.CircuitMaintenanceImpactEditView.as_view(), name='circuitimpact_add'),
    path('circuitnotification/add/', views.CircuitMaintenanceNotificationsEditView.as_view(), name='circuitnotification_add'),

    path('circuitmaintenance/<int:pk>/', views.CircuitMaintenanceView.as_view(), name='circuitmaintenance'),
    path('circuitnotification/<int:pk>/', views.CircuitMaintenanceNotificationView.as_view(), name='circuitnotification'),

    path('circuitmaintenance/<int:pk>/edit/', views.CircuitMaintenanceEditView.as_view(), name='circuitmaintenance_edit'),
    path('circuitimpact/<int:pk>/edit/', views.CircuitMaintenanceImpactEditView.as_view(), name='circuitimpact_edit'),
    #path('circuitnotification/<int:pk>/edit/', views.CircuitMaintenanceNotificationsEditView.as_view(), name='circuitnotification_edit'),

    path('circuitmaintenance/<int:pk>/delete/', views.CircuitMaintenanceDeleteView.as_view(), name='circuitmaintenance_delete'),
    path('circuitimpact/<int:pk>/delete/', views.CircuitMaintenanceImpactDeleteView.as_view(), name='circuitimpact_delete'),
    path('circuitnotification/<int:pk>/delete/', views.CircuitMaintenanceNotificationsDeleteView.as_view(), name='circuitnotification_delete'),

    path('circuitmaintenance/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='circuitmaintenance_changelog', kwargs={
        'model': models.CircuitMaintenance
    }),
    path('circuitimpact/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='circuitmaintenance_changelog', kwargs={
        'model': models.CircuitMaintenanceImpact
    }),

    path('maintenanceschedule/', views.CircuitMaintenanceScheduleView.as_view(), name='maintenanceschedule'),


)
