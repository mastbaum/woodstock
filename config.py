from woodstock.resource import Resource
from woodstock.view import View
from woodstock import md
import markdown

# set up markdown parser
rest_url = 'http://localhost:8052'
rest_server = Resource(rest_url)

configs = {'resource': [rest_server]}
md_parser = markdown.Markdown(extensions=[
    md.dynamic_value.DynamicValueExtension(configs=configs),
    md.dynamic_plot.DynamicPlotExtension(configs=configs)
])

# load up base template
template_root = './templates/'
template_base = template_root + 'base.html'
with open(template_base) as f:
    base_html = f.read()

# configuration must define rewrites dict, but nothing else
rewrites = {
    r'^\/?$': View(template_root + 'index.md', md_parser, base_html=base_html),
    r'^meta\/?$': View(template_root + 'meta.md', md_parser, base_html=base_html)
}

