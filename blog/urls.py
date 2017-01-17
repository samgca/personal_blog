from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^new-tag/$', views.new_tag, name='new_tag'),
    url(r'^post-search/$', views.post_search, name='post_search'),
    url(r'^search-modal/$', views.search_modal, name='search_modal'),
    url(r'^post/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<slug>[-\w]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<slug>[-\w]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^tag/(?P<slug>\S+)$', views.post_with_tag, name="post_tag"),
]
