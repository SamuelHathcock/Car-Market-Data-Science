

import unittest
import importlib
# craig = importlib.import_module('craigslist_spider.py', package='BestDealsFinder')
# from spiders.craigslist_spider import craig
import sys

class TestCraigslistSpider(unittest.TestCase):
    sys.path.append('/home/cha/Repositories/BestDealsFinder/spiders')
    
    print(sys.path)

    def test_clean(self):
        S = "1994 \nLincoln\n town \ncar"
        result = craig.clean(S)
        self.assertEqual(result, "1994 Lincoln town car")

if __name__ == '__main__':
    from spiders.craigslist_spider import craig
    unittest.main()