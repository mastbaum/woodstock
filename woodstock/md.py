import markdown
from markdown.util import etree

class DynamicValueExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = r'{dynamic (.+?)}'
        dynamic_value_pattern = DynamicValuePattern(pattern, self.getConfigs())
        md.inlinePatterns.add('dynamic_value', dynamic_value_pattern, '<not_strong')

class DynamicValuePattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern, config):
        markdown.inlinepatterns.Pattern.__init__(self, pattern)
        self.config = config

    def handleMatch(self, m):
        try:
            uri = m.group(1)
            d = markdown.util.etree.Element('span')
            d.text = 'omg'
            d.set('style', 'background:green')
        except IndexError:
            d = ''

        return d

def makeExtension(configs={}):
    return DynamicValueExtension(configs=configs)

