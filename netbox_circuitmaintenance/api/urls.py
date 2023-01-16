from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_circuitmaintenance'

router = NetBoxRouter()
router.register('circuitmaintenance', views.CircuitMaintenanceViewSet)
router.register('circuitmaintenanceimpact', views.CircuitMaintenanceImpactViewSet)
router.register('circuitmaintenancenotifications', views.CircuitMaintenanceNotificationsViewSet)

urlpatterns = router.urls