import os
import markdown

import config
import resource
import md.dynamic_value
import md.dynamic_plot

class View:
    '''Render page HTML from Markdown templates.'''
    def __init__(self, template_path, md_parser, base_html=None, title=None):
        self.headers = {'Content-type': 'text/html'}
        self.template_path = os.path.abspath(template_path)
        self.base_html = base_html
        self.md_parser = md_parser
        if title is None:
            self.title = os.path.splitext(os.path.basename(template_path))[0].title()
        else:
            self.title = title
        self.template = None
        self.load_template()

    def load_template(self):
        '''Load a template from disk.'''
        with open(self.template_path) as f:
            self.template = f.read()

    def run(self, env):
        '''Send the request to a method appropriate to the request method.
        Return a tuple of integer HTTP status, HTTP header dictionary, and
        string HTTP response.
        '''
        method = env['REQUEST_METHOD']
        print method, self.template_path
        try:
            return getattr(self, method)(env)
        except AttributeError:
            return 501, {}, '501 NOT IMPLEMENTED'

    def GET(self, env):
        '''Process a GET request.'''
        content = self.md_parser.convert(self.template).encode('utf-8')
        if self.base_html:
            data = {
                'title': self.title,
                'content': content
            }
            html = self.base_html % data
        else:
            html = content

        return 200, self.headers, html

