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

import time
import re
from DjangoCaptcha import Code
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
from django import http
import settings
import markdown

try:
    import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


class PreventWatering(object):
    """
    防灌水
    """

    captcha_uri   = '/captcha/'
    captcha_check_uri  = '/oh-my-god/check/'
    captcha_page_uri   = '/oh-my-god/'
    expaths            = ['/upload/']

    def process_request(self,request):
        if request.path == self.captcha_uri:
            code =  Code(request)
            code.type = 'number'
            return code.display()

        elif request.path == self.captcha_page_uri:
            return render('captcha.html',locals(),context_instance=RequestContext(request))

        elif request.path == self.captcha_check_uri:
            code = Code(request)
            _code = request.REQUEST.get('captcha','')

            # 检查用户输入的验证码是否正确
            if not code.check(_code):
                if request.is_ajax():
                    return HttpResponse('0')
                next = self.captcha_page_uri
            else:
                if request.is_ajax():
                    return HttpResponse('1')
                request.session['post_times'] = 0
                request.session['post_stamp'] = time.time()
                next = request.session.get('next','/')
            return HttpResponseRedirect(next)
        
        if not request.path in self.expaths:
            timer = time.time() - request.session.get('post_stamp',0)
            post_times = request.session.get('post_times',0)
            # 提交次数是否大于单位时间的最大值
            if request.method == 'POST':
                if post_times >= 3:
                    request.session['next'] = request.META.get('HTTP_REFERER','/')

                    # backup data
                    for k,v in request.POST.items():
                        k = 'backup_{}'.format(k)
                        try:
                            request.session[k] = v
                        except:
                            pass

                    return HttpResponseRedirect(self.captcha_page_uri)

class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
        
        
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
        """
    def process_request(self, request):
        
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
            
            return response
        
        return None
    
    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        
        return response

class ApiMiddleware(object):
    """ API protected 

    """
    
    def process_response(self, request, response):
        if request.path.startswith('/main/api/'):
            if request.REQUEST.get('token','') <> settings.API_TOKEN:
                return HttpResponse('invalid token')
        return response


class CommentPatchMiddle(object):
    """ Pathc comment

    """

    def process_request(self,request):
        if request.method == 'POST':
            if request.path == '/comments/post/':
                data = request.POST.copy()
                data['comment'] =  markdown.markdown(data['comment'])
                request.POST = data
