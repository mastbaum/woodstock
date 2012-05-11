from woodstock.view import View
from woodstock.md import DynamicMarkdown

# set up dynamic markdown parser
rest_server = 'http://localhost:8052'
md_parser = DynamicMarkdown(rest_server)

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

