from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, EmployeeVoteViewSet


router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('votes', EmployeeVoteViewSet, basename='vote')

urlpatterns = router.urls
