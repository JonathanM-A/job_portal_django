from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import UserViewSet, JobViewSet, ApplicationViewSet, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)

app_name = "jobs"
urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
