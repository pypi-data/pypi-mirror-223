from pypi_update.src.zdxtools.dx_tools import decorator
from pypi_update.src.zdxtools.dx_tools import spider_tools
import time


class a :
    @decorator.ExceptionD
    def test(self):
        data = {
            'a':1,
            '222':'2',
            'getsig':'213123',
        }
        int(data)
    def test1(self):
        driver = spider_tools.GetDriver()
        driver.get('https://bot.sannysoft.com/')
        time.sleep(15)
        return

if __name__ == '__main__':
    b = a()
    b.test1()