import os
import inspect
import asyncio
import functools

from urllib.parse import parse_qs
from importlib import import_module
from aiohttp import web

from tools.error_man import *

EMPTY = inspect.Parameter.empty
POSITIONAL_OR_KEYWORD = inspect.Parameter.POSITIONAL_OR_KEYWORD
VAR_POSITIONAL = inspect.Parameter.VAR_POSITIONAL
KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY
VAR_KEYWORD = inspect.Parameter.VAR_KEYWORD


def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


def get_keywordOnly_empty(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == KEYWORD_ONLY and param.kind == EMPTY:
            args.append(name)
    return tuple(args)


def get_keywordOnly(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def has_keywordOnly(fn, found=False):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == KEYWORD_ONLY:
            found = True
    return found


def has_varKeyword(fn, found=False):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == VAR_KEYWORD:
            found = True
    return found


def has_request(fn, found=False):
    sig = inspect.signature(fn)
    params = sig.parameters
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != VAR_POSITIONAL and param.kind != KEYWORD_ONLY and param.kind != VAR_KEYWORD):
            raise ValueError(
                'request parameter must be the last named parameter in func: %s%s' % (fn.__name__, str(sig)))
    return found


class RequestHandler:
    def __init__(self, app, func):
        self._app = app
        self._func = func
        self._has_request = has_request(func)
        self._has_keywordOnly = has_keywordOnly(func)
        self._has_varKeyword = has_varKeyword(func)
        self._keywordOnly = get_keywordOnly(func)
        self._keywordOnly_empty = get_keywordOnly_empty(func)

    async def __call__(self, request):
        kw = None
        if self._has_varKeyword or self._has_keywordOnly or self._keywordOnly_empty:
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse_qs(qs, True).items():
                        kw[k] = v
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest(reason='Missing Content-Type')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest(reason='JSON body must be object')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest(reason='Unsupported Content-Type: %s' % request.content_type)
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_varKeyword and self._keywordOnly:
                copy = dict()
                for name in self._keywordOnly:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            for k, v in request.match_info.items():
                kw[k] = v
        if self._has_request:
            kw['request'] = request
        if self._keywordOnly_empty:
            for name in self._keywordOnly_empty:
                if not name in kw:
                    return web.HTTPBadRequest(reason='Missing argument: %s' % name)
        try:
            res = await self._func(**kw)
            return res
        except BaseError as e:
            return dict(error=e.error, data=e.field, message=e.message)


def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)


def add_route(app, func):
    method = getattr(func, '__method__', None)
    path = getattr(func, '__route__', None)
    if path is None and method is None:
        raise ValueError('@get or @post not define in %s' % str(func))
    if not asyncio.iscoroutinefunction(func) and not inspect.isgeneratorfunction(func):
        func = asyncio.coroutine(func)
    app.router.add_route(method, path, RequestHandler(app, func))


def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = import_module(module_name)
    else:
        name = module_name[n + 1:]
        mod = getattr(import_module(module_name[:n]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = test = getattr(mod, attr)
        if callable(test):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)
