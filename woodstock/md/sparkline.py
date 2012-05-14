import re
import json
import markdown
from markdown.util import etree

class SparklineExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = r'{sparkline (.+?)}'
        sparkline_pattern = SparklinePattern(pattern, self.getConfigs())
        md.inlinePatterns.add('sparkline', sparkline_pattern, '<not_strong')

class SparklinePattern(markdown.inlinepatterns.Pattern):
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
                if status > 399:
                    raise Exception('rest api returned error')

                # DOM ID of plot div is cleaned-up version of source data uri
                plot_id = re.sub(r'[\/\_\.\?\=]', '_', uri)

                # script with the data array
                script_data = etree.SubElement(d, 'script')
                script_data.text = 'var data_plot_' + plot_id + ' = ' + body

                # div for flot plot
                plot_div = etree.SubElement(d, 'span')
                plot_div.set('style', 'height:3ex;width:15ex;')
                plot_div.set('class', 'sparkline')
                plot_div.set('id', plot_id)

                # prevent etree from self-closing div
                plot_div.text = '&nbsp;'

            except Exception:
                # if anything bad happens, just don't show the element
                print 'md: failed to get', self.resource.host, uri
                d.text = ''

        except IndexError:
            d = ''

        return d

def makeExtension(configs={}):
    return DynamicPlotExtension(configs=configs)

