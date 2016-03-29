#encoding:utf-8
"""
Copyright (C) 2016  PYTHONER.ORG

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

from django.db import models

ITEM_STATUS_CHOICES = [
    (0, u'等待审核'),
    (1, u'审核通过'),
    (2, u'拒绝'),
]

class Item(models.Model):
    url = models.URLField('网址',unique=True)
    title = models.CharField('标题',unique=True,max_length=15)
    content = models.CharField('介绍',max_length=500)
    status = models.IntegerField(u'状态', default=0, choices = ITEM_STATUS_CHOICES)

    class Meta: 
        ordering = ['status','-id']
        verbose_name= u'发现条目'
        verbose_name_plural = verbose_name
