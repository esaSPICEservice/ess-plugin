import xml.etree.ElementTree as ET
import os
from xml.dom import minidom


class BlockParser:

    def __init__(self, xml_content, strict_bounds=False):
        self.strict_bounds = strict_bounds
        try:
            self.root = ET.fromstring(xml_content)
        except Exception as e:
            raise ValueError("The string cannot be parsed as XML: " + str(e))

        self.start_times = list()
        self.end_times = list()
        self.block_contents = list()

    def process(self):
        self.blocks = self.root.findall('.//block')
        for block in self.blocks:
            self.start_times.append(self.get_start_time(block))
            self.end_times.append(self.get_end_time(block))
            self.block_contents.append(BlockParser.prettify(block))

    def get_start_time(self, block):
        if (block.attrib['ref'] == 'SLEW'):
            return ''
        return self.get_unique_path(block, "./startTime")

    def get_end_time(self, block):
        if (block.attrib['ref'] == 'SLEW'):
            return ''
        return self.get_unique_path(block, "./endTime")

    def get_off_start_time(self, block):
        return self.get_unique_path(block, "./endTime")

    def get_unique_path(self, element, path):
        st_candidates = element.findall(path)
        if len(st_candidates) == 0:
            if self.strict_bounds:
                raise ValueError("The xml does not contain the path " + path)
            else:
                return ''
        elif len(st_candidates) > 1:
            raise ValueError("The xml contains several values for the path " + path)
        else:
            # Important do the strip
            return st_candidates[0].text.strip()

    def dump_agm(self):
        return '\n'.join([ ET.tostring(b, 'utf-8').decode() for b in self.blocks])

    def dump_agm_file(self, agm_filename):
        with open(agm_filename, 'w') as f:
            f.write(self.dump_agm())
        return os.path.abspath(agm_filename)

    @staticmethod
    def _walk_n_apply(func, cond, parent):
        if parent.childNodes:
            for child in list(parent.childNodes):
                if cond(child):
                    func(parent, child)
                    continue
                BlockParser._walk_n_apply(func, cond, child)

    @staticmethod
    def remove_child(parent, child):
        node = parent.removeChild(child)

    @staticmethod
    def is_empty_text_node(node):
        return node.nodeType == node.TEXT_NODE and node.data.strip() == ''

    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        BlockParser._walk_n_apply(BlockParser.remove_child, BlockParser.is_empty_text_node, reparsed)
        return reparsed.toprettyxml(indent='  ')
