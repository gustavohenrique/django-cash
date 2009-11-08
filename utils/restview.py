#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Nuno Mariz'
__url__ = 'http://mariz.org'
__license__ = 'BSD'

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth import authenticate
from django.conf import settings
import re

try:
    import simplejson
except ImportError:
    from django.utils import simplejson

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python 2.3, 2.4 fallback.

nonalpha_re = re.compile('[^A-Z]')

class RestView(object):
    """
    Based on this snippet from Simon Willison(http://simonwillison.net):
    http://www.djangosnippets.org/snippets/1071/
    """
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'OPTIONS')
    realm = 'Restricted Access'

    def __call__(self, request, *args, **kwargs):
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods or not hasattr(self, method):
            return self.method_not_allowed(method)
        try:
            return getattr(self, method)(request, *args, **kwargs)
        except TypeError:
            raise Http404

    def method_not_allowed(self, method):
        response = HttpResponse('Method not allowed: %s' % method)
        response.status_code = 405
        return response

    def forbidden(self):
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        return response

    def authenticate(self, request):
        """
        Uses the default Django authentication via Basic Auth.
        You can override this function to make yours.
        """
        if request.user.is_authenticated():
            return request.user
        auth_info = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_info and auth_info.startswith('Basic '):
            base, basic_info = auth_info.split(' ', 1)
            u, p = basic_info.strip().decode('base64').split(':')
            return authenticate(username=u, password=p)
        return None

def login_required(func):
    """ Decorator for the user authentication. """
    def inner_func(self, request, *args, **kwargs):
        if not self.authenticate(request):
            return self.forbidden()
        return func(self, request, *args, **kwargs)
    return wraps(func)(inner_func)

def ajax_required(func):
    """ Decorator for accepting requests only from AJAX calls """
    def inner_func(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(self, request, *args, **kwargs)
    return wraps(func)(inner_func)

class JsonHttpResponse(HttpResponse):
    """
    JSON HttpResponse

    Usage:

    >>> json = {'blogs': [{'name': u'Nuno Mariz Weblog', 'url' : u'http://mariz.org'}]}
    >>> return JsonResponse(json)

    or

    >>> response = JsonResponse()
    >>> response.write(json)
    >>> return response
    """
    def __init__(self, content='', mimetype='application/json',
                 charset=settings.DEFAULT_CHARSET, ensure_ascii=False, indent=None):
        self._json_ensure_ascii = ensure_ascii
        self._json_indent = indent

        if isinstance(content, basestring):
            HttpResponse.__init__(self,
                                  content,
                                  content_type='%s; charset=%s' % (mimetype, charset))
        else:
            HttpResponse.__init__(self,
                                  simplejson.dumps(content,
                                                   ensure_ascii=self._json_ensure_ascii,
                                                   indent=self._json_indent),
                                  content_type='%s; charset=%s' % (mimetype, charset))

    def write(self, content):
        if isinstance(content, basestring):
            HttpResponse.write(self, content)
        else:
            HttpResponse.write(self,
                               simplejson.dumps(content,
                                                ensure_ascii=self._json_ensure_ascii,
                                                indent=self._json_indent))

class XmlHttpResponse(HttpResponse):
    """
    XML HttpResponse

    Usage:

    >>> xml = '<?xml version="1.0" encoding="utf-8"?>'
    >>> xml += '<blogs>'
    >>> xml += '<blog><name>Nuno Mariz Weblog</name><url>http://mariz.org</url></blog>'
    >>> xml += '</blogs>'
    >>> return XmlResponse(xml)
    """
    def __init__(self, content='', mimetype='application/xml',
                 charset=settings.DEFAULT_CHARSET):
        HttpResponse.__init__(self,
                              content,
                              content_type='%s; charset=%s' % (mimetype, charset))
