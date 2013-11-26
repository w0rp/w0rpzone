from lxml.html import html5parser
from cssselect import HTMLTranslator

css_to_xpath = HTMLTranslator().css_to_xpath

def rip_wikitables(file_obj):
    def rip_table(table):
        for row in table.xpath("//tr"):
            yield tuple(x.text for x in row.xpath("//td"))

    doc = html5parser.parse(file_obj)

    for table in doc.xpath("//table"):
        yield rip_table(table)

