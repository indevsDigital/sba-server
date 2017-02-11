from django.conf.urls import url,include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from . import views
router = routers.DefaultRouter()
urlpatterns = format_suffix_patterns([
    url(r'^$', views.ApiRootView.as_view(),name='api'),
    url(r'^auth/register', views.Registration.as_view(), name='register'),
    url(r'^api-token-auth/', obtain_jwt_token,name='token-obtain'),
    url(r'^users/$', views.UserList.as_view(),name="user-list"),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(),name="user-detail"),
    url(r'^users-profiles/$', views.UserProfileList.as_view(),name="user-profile-list"),    
    url(r'^users-profiles/(?P<pk>\d+)/$', views.UserProfileDetail.as_view(),name="user-profile"),
    url(r'^categories/$', views.CategoryList.as_view(),name="category-list"),
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryDetail.as_view(),name="category-detail"),
    url(r'^products/$', views.ProductList.as_view(),name="product-list"),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetail.as_view(),name="product-detail"),
    url(r'^businesses/$', views.BusinessList.as_view(),name="business-list"),
    url(r'^businesses/(?P<pk>\d+)/$', views.BusinessDetail.as_view(),name="business-detail"),
    url(r'^sales/$', views.SalesList.as_view(),name="sales-list"),
    url(r'^sales/(?P<pk>\d+)/$', views.SaleDetail.as_view(),name="sales-detail"),
    
    
    
])
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]