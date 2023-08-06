
from lxml import html

class Bsxpath:
    tree = None
    def __init__(self, res=None):
        if res:
            self.tree = html.fromstring(res)
    
    def find_all(self, tag, **kwargs):
        for key, value in kwargs.items():
            els = self.tree.xpath(f'//{tag}[@{key}="{value}"]')
            if els:
                if kwargs.get('limit'):
                    els = [els[0]]
                elements = []
                for el in els:
                    temp = Bsxpath()
                    temp.tree = el
                    elements.append(temp)
                return elements

    def find(self, tag, **kwargs):
        kwargs['limit'] = True
        elements = self.find_all(tag, **kwargs)
        if elements:
            return elements[0]
    
    def text(self):
        if self.tree.text:
            return str(self.tree.text)
        
    def get(self, tag):
        return self.tree.get(tag)