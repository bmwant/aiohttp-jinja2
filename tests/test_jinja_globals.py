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


async def test_url(test_client, loop):
    @japronto_jinja2.template('tmpl.jinja2')
    async def index(request):
        return {}

    async def other(request):
        return

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader(
        {'tmpl.jinja2':
         "{{ url('other', name='John_Doe')}}"}))

    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/user/{name}', other, name='other')
    client = await test_client(app)

    resp = await client.get('/')
    assert resp.status == 200
    txt = await resp.text()
    assert txt == '/user/John_Doe'
    assert False
