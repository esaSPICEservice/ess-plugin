import re

class BlockParser:

    def __init__(self, xml_content, strict_bounds=False):
        self.strict_bounds = strict_bounds
        self.xml_content = xml_content

    def process(self):
        self.start_times = self.get_tags('startTime')
        self.end_times = self.get_tags('endTime')
        self.block_contents = self.get_tags('block')

    def get_tags(self, tag):
        xml_pattern = "(?:<{tag}.*?>)(.*?)(?:<\\/{tag}>)".format(tag=tag)
        return re.findall(xml_pattern, self.xml_content)