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

LINK_STATUS_CHOICES = [
    (0, u'等待审核'),
    (1, u'审核通过'),
    (2, u'拒绝'),
]

class Category(models.Model):
    name = models.CharField('链接类别', max_length=10)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name_plural = '链接分类'


class Link(models.Model):
    category = models.ForeignKey(Category,verbose_name='类别',null=True,blank=True)
    url = models.URLField('网址',unique=True)
    title = models.CharField('标题',unique=True,max_length=15)
    email = models.EmailField('邮件')
    remark = models.CharField('说明',max_length=100)
    status = models.IntegerField(u'状态', default=0, choices = LINK_STATUS_CHOICES)
    created_at = models.DateTimeField('时间',auto_now_add=True)

    def get_absolute_url(self):
        return self.url

    class Meta: 
        ordering = ['status','-id']
        verbose_name= '链接'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        if self.display:
            return u'[%s] %s:%s' %(self.category.name,self.title,self.url)
        else:
            return u'[待审核]%s:%s' %(self.title,self.url)
