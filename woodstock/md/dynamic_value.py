import json
import markdown
from markdown.util import etree

class DynamicValueExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = r'{value (.+?)}'
        dynamic_value_pattern = DynamicValuePattern(pattern, self.getConfigs())
        md.inlinePatterns.add('dynamic_value', dynamic_value_pattern, '<not_strong')

class DynamicValuePattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern, config):
        markdown.inlinepatterns.Pattern.__init__(self, pattern)
        self.config = config
        self.resource = config['resource']

    def handleMatch(self, m):
        try:
            uri = m.groups()[1]
            d = markdown.util.etree.Element('span')
            try:
                status, headers, body = self.resource.get(uri)
                body = json.loads(body) #['value']
                if isinstance(body, dict):
                    text = json.dumps(body, sort_keys=True, indent=4)
                    for block in text.split('\n'):
                        elem = markdown.util.etree.SubElement(d, 'span')
                        elem.text = block.replace(' ', '&nbsp;')
                        markdown.util.etree.SubElement(d, 'br')
                elif isinstance(body, list):
                    d.text = json.dumps(body, sort_keys=True, indent=4)
                else:
                    d.text = str(body)
            except Exception:
                print 'md: failed to get', self.resource.host, uri
                d.text = ''
        except IndexError:
            d = ''

        return d

def makeExtension(configs={}):
    return DynamicValueExtension(configs=configs)

