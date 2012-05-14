import re
import json
import markdown
from markdown.util import etree

class PlotlinkExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = r'{plotlink ([a-zA-Z0-9]+)\s+(.+?)}'
        plotlink_pattern = PlotlinkPattern(pattern, self.getConfigs())
        md.inlinePatterns.add('plotlink', plotlink_pattern, '<not_strong')

class PlotlinkPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern, config):
        markdown.inlinepatterns.Pattern.__init__(self, pattern)
        self.config = config
        self.resource = config['resource']

    def handleMatch(self, m):
        try:
            link_text = m.groups()[1]
            uri = m.groups()[2]
            link = markdown.util.etree.Element('a')
            try:
                status, headers, body = self.resource.get(uri)
                if status > 399:
                    raise Exception('rest api returned error')

                # DOM ID of plot div is cleaned-up version of source data uri
                plot_id = re.sub(r'[\/\_\.\?\=]', '_', uri)

                # script with the data array
                script_data = etree.SubElement(link, 'script')
                script_data.text = 'var data_plot_' + plot_id + ' = ' + body

                link.set('href', '#')
                link.set('onclick', 'showPlotModal("' + link_text + '",data_plot_' + plot_id + ');')
                link.text = link_text

            except Exception:
                raise
                # if anything bad happens, just don't show the element
                print 'md: failed to get', self.resource.host, uri
                link.text = ''

        except IndexError:
            link = ''

        return link

def makeExtension(configs={}):
    return PlotlinkExtension(configs=configs)

