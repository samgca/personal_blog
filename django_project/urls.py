from django.conf.urls import url, include
from django.contrib.auth import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, {'template_name': 'blog/login.html'}, name='auth_login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='auth_logout'),
    url(r'', include('blog.urls')),
]
