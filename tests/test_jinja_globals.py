import asyncio
import japronto
import jinja2
import japronto_jinja2


def test_get_env(loop):
    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader(
        {'tmpl.jinja2': 'tmpl'}))

    env = japronto_jinja2.get_env(app)
    assert isinstance(env, jinja2.Environment)
    assert env is japronto_jinja2.get_env(app)


# @asyncio.coroutine
# def test_url(test_client, loop):
#
#     @japronto_jinja2.template('tmpl.jinja2')
#     @asyncio.coroutine
#     def index(request):
#         return {}
#
#     @asyncio.coroutine
#     def other(request):
#         return
#
#     app = japronto.Application()
#     japronto_jinja2.setup(app, loader=jinja2.DictLoader(
#         {'tmpl.jinja2':
#          "{{ url('other', name='John_Doe')}}"}))
#
#     app.router.add_route('GET', '/', index)
#     app.router.add_route('GET', '/user/{name}', other, name='other')
#     client = yield from test_client(app)
#
#     resp = yield from client.get('/')
#     assert 200 == resp.status
#     txt = yield from resp.text()
#     assert '/user/John_Doe' == txt
