from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    # url(r'^(?P<product_id>[0-9]+)$', detail, name="detail"),
    url(r'^(?P<pk>[\w-]+)$', detail, name="detail"),
    url(r'^edit/(?P<pk>[\w-]+)$', edit, name="edit"),
    url(r'^addnew/$', addnew, name="addnew"),

    url(r'^api/v1/products/(?P<cat>\w+)$', ListProductsView.as_view(), name="products-all"),
    url(r'^api/v1/userZones/$', ListUserZonesView.as_view(), name="user-zones-all"),
    url('api/v1/auth/register/', RegisterUsers.as_view(), name="auth-register"),
    url('api/v1/auth/login/', LoginUser.as_view(), name="auth-login"),

    url(r'^api/v1/users/deliveryMen/$', ListDeliveryManView.as_view(), name="delivery-man-all"),
    url(r'^api/v1/purchases/status/(?P<pk>\w+)$', PurchaseStateView.as_view(), name="purchase-state"),
]
