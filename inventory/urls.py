from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from .views import *





urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<product_id>[0-9]+)$', detail, name="detail"),
    url(r'^(?P<pk>[\w-]+)$', detail, name="detail"),
    url(r'^edit/(?P<pk>[\w-]+)$', edit, name="edit"),
    url(r'^addnew/$', addnew, name="addnew"),

    url(r'^api/v1/products/(?P<cat>\w+)$', ListProductsView.as_view(), name="products-all"),
    url(r'^api/v1/users/user-zones/$', ListUserZonesView.as_view(), name="user-zones-all"),
    url('api/v1/auth/register/', RegisterUsers.as_view(), name="auth-register"),
    url('api/v1/auth/login/', LoginUser.as_view(), name="auth-login"),

    url(r'^api/v1/users/delivery-men/$', ListDeliveryManView.as_view(), name="delivery-man-all"),
    url(r'^api/v1/purchases/status/(?P<pk>\w+)$', PurchaseStateView.as_view(), name="purchase-state"),
    url(r'^api/v1/purchases/info/(?P<pk>\w+)$', PurchaseInfoView.as_view(), name="purchase-info"),
    url(r'^api/v1/delivery-centers/$', ListDeliveryCentersView.as_view(), name="delivery-centers-all"),
    url(r'^api/v1/purchases/query?.+$', ListPurchasesView.as_view(), name="purchases"),
    url('api/v1/purchases/make-purchase/', MakePurchaseView.as_view(), name="make-purchase"),
    url('api/v1/purchases/process-purchase/', ProcessPurchaseView.as_view(), name="process-purchase"),
    url(r'^api/v1/user-purchases/query?.+$', ListUserPurchasesView.as_view(), name="user-purchases"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
