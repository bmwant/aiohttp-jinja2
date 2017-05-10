import jinja2
import pytest
import japronto
import japronto_jinja2


async def test_func(loop, test_client):

    @japronto_jinja2.template('tmpl.jinja2')
    async def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'
    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader({
        'tmpl.jinja2': template
    }))

    app.router.add_route('*', '/', func)

    client = await test_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_meth(loop, test_client):

    class Handler:

        @japronto_jinja2.template('tmpl.jinja2')
        async def meth(self, request):
            return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'

    handler = Handler()

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader({
        'tmpl.jinja2': template
    }))

    app.router.add_route('*', '/', handler.meth)

    client = await test_client(app)

    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_convert_func_to_coroutine(loop, test_client):

    @japronto_jinja2.template('tmpl.jinja2')
    def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader({
        'tmpl.jinja2': template
    }))

    app.router.add_route('*', '/', func)

    client = await test_client(app)

    resp = await client.get('/')

    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


# async def test_render_not_initialized(loop):
#
#     async def func(request):
#         return japronto_jinja2.render_template('template', request, {})
#
#     app = japronto.Application()
#
#     app.router.add_route('GET', '/', func)
#
#     req = make_mocked_request('GET', '/', app=app)
#     msg = "Template engine is not initialized, " \
#           "call aiohttp_jinja2.setup(..., app_key={}" \
#           ") first".format(japronto_jinja2.APP_KEY)
#
#     with pytest.raises(web.HTTPInternalServerError) as ctx:
#         await func(req)
#
#     assert msg == ctx.value.text


async def test_set_status(loop, test_client):

    @japronto_jinja2.template('tmpl.jinja2', status=201)
    def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader({
        'tmpl.jinja2': template
    }))

    app.router.add_route('*', '/', func)

    client = await test_client(app)

    resp = await client.get('/')

    assert 201 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_render_template(loop, test_client):

    async def func(request):
        return japronto_jinja2.render_template(
            'tmpl.jinja2', request,
            {'head': 'HEAD', 'text': 'text'})

    template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader({
        'tmpl.jinja2': template
    }))

    app.router.add_route('*', '/', func)

    client = await test_client(app)

    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt
#
#
# @asyncio.coroutine
# def test_render_template_custom_status(loop, test_client):
#
#     @asyncio.coroutine
#     def func(request):
#         return japronto_jinja2.render_template(
#             'tmpl.jinja2', request,
#             {'head': 'HEAD', 'text': 'text'}, status=404)
#
#     template = '<html><body><h1>{{head}}</h1>{{text}}</body></html>'
#
#     app = japronto.Application()
#     japronto_jinja2.setup(app, loader=jinja2.DictLoader({
#         'tmpl.jinja2': template
#     }))
#
#     app.router.add_route('*', '/', func)
#
#     client = await test_client(app)
#
#     resp = await client.get('/')
#
#     assert 404 == resp.status
#     txt = await resp.text()
#     assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


# async def test_template_not_found(loop):
#
#     @asyncio.coroutine
#     def func(request):
#         return japronto_jinja2.render_template('template', request, {})
#
#     app = japronto.Application()
#     japronto_jinja2.setup(app, loader=jinja2.DictLoader({}))
#
#     app.router.add_route('GET', '/', func)
#
#     req = make_mocked_request('GET', '/', app=app)
#
#     with pytest.raises(web.HTTPInternalServerError) as ctx:
#         await func(req)
#
#     t = "Template 'template' not found"
#     assert t == ctx.value.text
#     assert t == ctx.value.reason


# @asyncio.coroutine
# def test_render_not_mapping(loop):
#
#     @japronto_jinja2.template('tmpl.jinja2')
#     @asyncio.coroutine
#     def func(request):
#         return 123
#
#     app = japronto.Application()
#     japronto_jinja2.setup(app, loader=jinja2.DictLoader(
#         {'tmpl.jinja2': 'tmpl'}))
#
#     app.router.add_route('GET', '/', func)
#
#     req = make_mocked_request('GET', '/', app=app)
#     msg = "context should be mapping, not <class 'int'>"
#     with pytest.raises(web.HTTPInternalServerError) as ctx:
#         await func(req)
#
#     assert msg == ctx.value.text
#

async def test_render_without_context(loop, test_client):

    @japronto_jinja2.template('tmpl.jinja2')
    def func(request):
        pass

    template = '<html><body><p>{{text}}</p></body></html>'

    app = japronto.Application()
    japronto_jinja2.setup(app, loader=jinja2.DictLoader(
        {'tmpl.jinja2': template}))

    app.router.add_route('GET', '/', func)

    client = await test_client(app)
    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><p></p></body></html>' == txt
