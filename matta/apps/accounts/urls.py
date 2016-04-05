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
import apps.accounts.views as accounts_views

urlpatterns = [
    url('^login/$', accounts_views.login),
    url('^logout/$', accounts_views.logout),
    # 先不考虑第三方账号的登陆

    url('^register/$', accounts_views.register),
    url(r'^active/(\d{1,10})/(.*)/$', accounts_views.active),
]
