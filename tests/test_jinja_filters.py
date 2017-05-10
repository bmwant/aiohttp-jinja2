import asyncio
import jinja2
import japronto
import japronto_jinja2


@asyncio.coroutine
def test_jinja_filters(test_client, loop):

    @japronto_jinja2.template('tmpl.jinja2')
    @asyncio.coroutine
    def index(request):
        return {}

    def add_2(value):
        return value + 2

    app = japronto.Application()
    japronto_jinja2.setup(
        app,
        loader=jinja2.DictLoader({'tmpl.jinja2': '{{ 5|add_2 }}'}),
        filters={'add_2': add_2}
    )

    app.router.add_route('GET', '/', index)
    client = yield from test_client(app)

    resp = yield from client.get('/')
    assert resp.status == 200
    txt = yield from resp.text()
    assert txt == '7'
