'''Markdown parsing facilities.

woodstock uses python-markdown extensions to inject dynamic content into
Markdown templates.
'''

import markdown

import woodstock.resource
import dynamic_value
import dynamic_plot

extensions = [
    dynamic_value.DynamicValueExtension,
    dynamic_plot.DynamicPlotExtension
]

class DynamicMarkdown(markdown.Markdown):
    '''A Markdown parser with dynamic content superpowers.
    
    If `rest_server` is given (a string URI or `woodstock.resource.Resource`
    instance work), use extensions to include dynamic content.
    '''
    def __init__(self, rest_server=None):
        if isinstance(rest_server, str):
            self.rest_server = woodstock.resource.Resource(rest_server)
        else:
            self.rest_server = rest_server

        if rest_server is not None:
            configs = {'resource': [self.rest_server]}
            ext = [x(configs=configs) for x in extensions]
        else:
            ext = []

        markdown.Markdown.__init__(self, extensions=ext)

