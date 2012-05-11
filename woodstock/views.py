# views

import os
import markdown

import resource

import md.dynamic_value
import md.dynamic_plot

resource_url = 'http://localhost:8052'
resource = resource.Resource(resource_url)

with open('templates/base.html') as f:
    base_html = f.read()

configs = {'resource': [resource]}
dve = md.dynamic_value.DynamicValueExtension(configs=configs)
dpe = md.dynamic_plot.DynamicPlotExtension(configs=configs)

mark = markdown.Markdown(extensions=[dve, dpe])

class View:
    def __init__(self, template_path):
        self.headers = {'Content-type': 'text/html'}
        self.template_path = os.path.abspath(template_path)
        self.template = None
        self.load_template()
    def load_template(self):
        '''Load a template from disk.'''
        with open(self.template_path) as f:
            self.template = f.read()
    def run(self, env):
        '''Send the request to a method appropriate to the request method.
        Return a tuple of integer HTTP status, HTTP header dictionary, and
        UTF-8 string HTTP response.
        '''
        method = env['REQUEST_METHOD']
        print self.template_path, method
        try:
            return getattr(self, method)(env)
        except AttributeError:
            return 501, {}, '501 NOT IMPLEMENTED'

class Index(View):
    '''The main page'''
    def GET(self, env):
        data = {
            'title': 'woodstock',
            'content': mark.convert(self.template).encode('utf-8')
        }
        html = base_html % data
        return 200, self.headers, html

class Meta(View):
    '''metadata'''

