from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from travel import views
from travel.views import get_customers_by_schedule

r = routers.DefaultRouter()
r.register('roles', views.RoleViewSet, 'roles')
r.register('users', views.UserViewSet, 'users')
r.register('providers', views.ProviderViewSet, 'providers')
r.register('customers', views.CustomerViewSet, 'customers')
r.register('service-types', views.ServiceTypeViewSet, 'service-types'),
r.register('provinces', views.ProvinceViewSet, 'provinces')
r.register('images', views.ImageViewSet, 'images')
r.register('services', views.ServiceViewSet, 'services')
r.register('discounts', views.DiscountViewSet, 'discounts'),
r.register('service-schedules', views.ServiceScheduleViewSet, 'service-schedules'),
r.register('bookings', views.BookingViewSet, 'bookings'),
r.register('reviews', views.ReviewViewSet, 'reviews'),
r.register('revenue', views.RevenueViewSet, basename='revenue')

urlpatterns = [
    path('', include(r.urls)),
    path('admin/', admin.site.urls),
    path('payment/', views.payment_view, name='payment'),
    path('zalo/payment/', views.create_payment, name='zalopay'),
    path('customers-by-schedule/<int:schedule_id>/', get_customers_by_schedule, name='customers-by-schedule'),
]
