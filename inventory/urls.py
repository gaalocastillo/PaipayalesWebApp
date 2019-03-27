from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    # url(r'^(?P<product_id>[0-9]+)$', detail, name="detail"),
    url(r'^(?P<pk>\d+)$', detail, name="detail"),
    url(r'^edit/(?P<pk>\d+)$', edit, name="edit"),
    url(r'^addnew$', addnew, name="addnew"),

    url(r'^products/(?P<cat>\w+)$', ListProductsView.as_view(), name="products-all"),
    url('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    url('auth/login/', LoginUser.as_view(), name="auth-login"),
]
