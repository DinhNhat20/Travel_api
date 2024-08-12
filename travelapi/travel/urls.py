from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from travel import views


r = routers.DefaultRouter()
r.register('roles', views.RoleViewSet, 'roles')
r.register('users', views.UserViewSet, 'users')
r.register('service-providers', views.ServiceProviderViewSet, 'service-providers')
r.register('customers', views.CustomerViewSet, 'customers')
r.register('service-types', views.ServiceTypeViewSet, 'service-types'),
r.register('services', views.ServiceViewSet, 'services')
r.register('discounts', views.DiscountViewSet, 'discounts'),
r.register('service-schedules', views.ServiceScheduleViewSet, 'service-schedules'),
r.register('bookings', views.BookingViewSet, 'bookings'),
r.register('reviews', views.ReviewViewSet, 'reviews'),

urlpatterns = [
    path('', include(r.urls)),
    path('admin/', admin.site.urls),
]