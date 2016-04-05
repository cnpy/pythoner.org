#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.conf.urls import url
import views as accounts_views
import sina

urlpatterns = [
    url('^login/$', accounts_views.login),

    url('^login/sina/$', sina.index),
    url(r'login/sina/callback/$', sina.callback),

    #('^login/douban/$','douban.index'),
    #(r'login/douban/callback/$','douban.callback'),

    #('^login/twitter/$','twitter.index'),
    #(r'login/twitter/callback/$','twitter.callback'),

    url('^logout/$', accounts_views.logout),
    url('^register/$', accounts_views.register),
    url(r'^active/(\d{1,10})/(.*)/$', accounts_views.active),
]