from zope.interface import Interface

class ISpiderLoader(Interface):

    def from_settings(settings):
        """Return an instance of the class for the given settings"""

    def load(spider_name):
        """Return the Spider class for the given spider name. If the spider
        name is not found, it must raise a KeyError."""

    def list():
        """Return a list with the names of all spiders available in the
        project"""

    def find_by_request(request):
        """Return the list of spiders names that can handle the given request"""


class ICzaSpider(Interface):
    def test1():...
    def test2(settings):...


from zope.interface import implementer

@implementer(ICzaSpider)
class Test:
    def test1(self):print('test1')
    def test2(self):print('test2')


if __name__ == '__main__':
    a = Test()
    a.test1()
    a.test2()
