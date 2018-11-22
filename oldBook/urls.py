from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^book/$', views.index, name='book_index'),
    url(r'^book/(?P<pk>[0-9]+)$', views.detail, name='book_detail'),
    url(r'^user/create$', views.user_create, name='user_create'),
    url(r'^user/authenticate$', views.user_verify, name='user_authenticate'),
    url(r'^user/logout$', views.user_logout, name='user_logout'),
]
