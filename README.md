## japronto_jinja2

[jinja2](http://jinja.pocoo.org) asynchronous template renderer for 
[japronto](https://github.com/squeaky-pl/japronto).

### Installation

Install from PyPI:
```
pip install japronto-jinja2
```

### Developing

Install requirement and launch tests:
```
pip install -e .[dev]
pytest
```

### Usage

Before template rendering you have to setup *jinja2 environment* first::

    import jinja2
    from japronto import Application
    
    app = Application()
    japronto_jinja2.setup(app, loader=jinja2.FileSystemLoader('/path/to/templates/folder'))


After that you may to use template engine in your *web-handlers*. The
most convenient way is to decorate a *web-handler*.

Using the function based web handlers::

    @ajapronto_jinja2.template('tmpl.jinja2')
    def handler(request):
        return {'action': 'follow', 'person': 'me'}


On handler call the `japronto_jinja2.template` decorator will pass
returned dictionary `{'action': 'follow', 'person': 'me'}` into
template named `tmpl.jinja2` for getting resulting HTML text.

If you need more complex processing (modify response on your own)
you may call `render_template` function.

Using a function based web handler::

    async def handler(request):
        context = {'action': 'unsubscribe', 'from': 'channel'}
        response = aiohttp_jinja2.render_template('tmpl.jinja2',
                                                  request,
                                                  context)
        # do smth with your response
        return response

See [examples](https://github.com/bmwant/japronto-jinja2/tree/master/examples) 
directory for more complete snippets.

### License

`japronto_jinja2` is offered under the Apache 2 license.
