from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views
from .ical import MaintenanceICalView

urlpatterns = (
    path(
        "circuitmaintenance/",
        views.CircuitMaintenanceListView.as_view(),
        name="circuitmaintenance_list",
    ),
    path(
        "circuitmaintenance/edit/",
        views.CircuitMaintenanceBulkEditView.as_view(),
        name="circuitmaintenance_bulk_edit",
    ),
    path(
        "circuitmaintenance/delete/",
        views.CircuitMaintenanceBulkDeleteView.as_view(),
        name="circuitmaintenance_bulk_delete",
    ),
    path(
        "circuitmaintenance/import/",
        views.CircuitMaintenanceBulkImportView.as_view(),
        name="circuitmaintenance_import",
    ),
    path(
        "circuitmaintenance/add/",
        views.CircuitMaintenanceEditView.as_view(),
        name="circuitmaintenance_add",
    ),
    path(
        "circuitimpact/add/",
        views.CircuitMaintenanceImpactEditView.as_view(),
        name="circuitimpact_add",
    ),
    path(
        "circuitnotification/",
        views.CircuitMaintenanceNotificationsListView.as_view(),
        name="circuitmaintenancenotifications_list",
    ),
    path(
        "circuitnotification/add/",
        views.CircuitMaintenanceNotificationsEditView.as_view(),
        name="circuitmaintenancenotifications_add",
    ),
    path(
        "circuitmaintenance/<int:pk>/",
        views.CircuitMaintenanceView.as_view(),
        name="circuitmaintenance",
    ),
    path(
        "circuitnotification/<int:pk>/",
        views.CircuitMaintenanceNotificationView.as_view(),
        name="circuitnotification",
    ),
    path(
        "circuitmaintenance/<int:pk>/edit/",
        views.CircuitMaintenanceEditView.as_view(),
        name="circuitmaintenance_edit",
    ),
    path(
        "circuitimpact/<int:pk>/edit/",
        views.CircuitMaintenanceImpactEditView.as_view(),
        name="circuitimpact_edit",
    ),
    path(
        "circuitnotification/<int:pk>/edit/",
        views.CircuitMaintenanceNotificationsEditView.as_view(),
        name="circuitmaintenancenotifications_edit",
    ),
    path(
        "circuitmaintenance/<int:pk>/delete/",
        views.CircuitMaintenanceDeleteView.as_view(),
        name="circuitmaintenance_delete",
    ),
    path(
        "circuitimpact/<int:pk>/delete/",
        views.CircuitMaintenanceImpactDeleteView.as_view(),
        name="circuitimpact_delete",
    ),
    path(
        "circuitnotification/<int:pk>/delete/",
        views.CircuitMaintenanceNotificationsDeleteView.as_view(),
        name="circuitmaintenancenotifications_delete",
    ),
    path(
        "circuitmaintenance/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="circuitmaintenance_changelog",
        kwargs={"model": models.CircuitMaintenance},
    ),
    path(
        "circuitimpact/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="circuitimpact_changelog",
        kwargs={"model": models.CircuitMaintenanceImpact},
    ),
    path(
        "circuitnotification/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="circuitmaintenancenotifications_changelog",
        kwargs={"model": models.CircuitMaintenanceNotifications},
    ),
    path(
        "maintenanceschedule/",
        views.CircuitMaintenanceScheduleView.as_view(),
        name="maintenanceschedule",
    ),
    path(
        "maintenancesummary/",
        views.CircuitMaintenanceSummaryView.as_view(),
        name="maintenancesummary",
    ),
    path("maintenance.ics", MaintenanceICalView.as_view(), name="maintenance_ics"),
)
