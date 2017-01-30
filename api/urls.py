from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^users/$', views.UserList.as_view(),name="user-list"),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(),name="user-detail"),
    url(r'^users-profile/$', views.UserProfileList.as_view(),name="user-profile-list"),    
    url(r'^users-profile/(?P<pk>\d+)/$', views.UserProfileDetail.as_view(),name="user-profile"),
    
]
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
urlpatterns = format_suffix_patterns(urlpatterns)