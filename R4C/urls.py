from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/robots/', include('robots.urls')),
    # path('api/orders', include('orders.urls')),
    # path('api/customers', include('customers.urls')),
    path('admin/', admin.site.urls),
]
