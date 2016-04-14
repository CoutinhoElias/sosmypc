from django.conf.urls import url, include

import sosmypc
from . import views


urlpatterns = [
   url(r'^$',views.index_html,name='sosmypc'),
   #url(r'^login/$',views.login,name='login'),--
   url(r'^registro/$',views.register_html,name='registro'),
]
