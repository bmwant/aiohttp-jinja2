import asyncio
import functools
import jinja2
from collections import Mapping


__version__ = '0.0.1'

__all__ = ('setup', 'get_env', 'render_template', 'template')

APP_KEY = 'japronto_jinja2_environment'


class JJException(Exception):
    """Japronto Jinja2 exception"""


def setup(app, *args, app_key=APP_KEY, filters=None, **kwargs):
    env = jinja2.Environment(*args, **kwargs)
    if filters is not None:
        env.filters.update(filters)
    setattr(app, app_key, env)
    env = getattr(app, app_key)

    def url(__aiohttp_jinja2_route_name, **kwargs):
        return app.router[__aiohttp_jinja2_route_name].url_for(**kwargs)

    env.globals['url'] = url
    env.globals['app'] = app

    return env


def get_env(app, *, app_key=APP_KEY):
    return getattr(app, app_key)


def render_string(template_name, request, context, *, app_key=APP_KEY):
    env = getattr(request.app, app_key)
    if env is None:
        text = ('Template engine is not initialized, '
                'call japronto_jinja2.setup first')
        # in order to see meaningful exception message both: on console
        # output and rendered page we add same message to *reason* and
        # *text* arguments.
        return request.Response(code=500, text=text)

    try:
        template = env.get_template(template_name)
    except jinja2.TemplateNotFound as e:
        text = 'Template "{}" not found'.format(template_name)
        raise JJException(text) from e
    if not isinstance(context, Mapping):
        text = 'context should be mapping, not {}'.format(type(context))
        # same reason as above
        return JJException(text)

    text = template.render(context)
    return text


def render_template(template_name, request, context, *,
                    app_key=APP_KEY, encoding='utf-8', status=200):
    if context is None:
        context = {}
    text = render_string(template_name, request, context, app_key=app_key)
    return request.Response(code=status, text=text,
                            mime_type='text/html', encoding=encoding)


def template(template_name, *, app_key=APP_KEY, encoding='utf-8', status=200):
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)
            context = yield from coro(*args)

            request = args[-1]

            response = render_template(template_name, request, context,
                                       app_key=app_key, encoding=encoding,
                                       status=status)
            return response
        return wrapped
    return wrapper
