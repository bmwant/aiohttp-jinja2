import jinja2
import japronto_jinja2
from japronto import Application


def hello(request):
    return request.Response(text='Hello world!')


@japronto_jinja2.template('index.html')
def index(request):
    context = {'first_name': 'Ja', 'second_name': 'Pronto'}
    return context


app = Application()
japronto_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_route('/', hello)
app.router.add_route('/index', index)
app.run(debug=True)
