import unittest
from auslib.global_state import dbo
from auslib.web.public.base import app


class UnicodeTest(unittest.TestCase):
    def setUp(self):
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.client = app.test_client()

    def testUnicodeInRoute(self):
        url = "/update/3/GMP/53.0/20170421105455/Linux_x86_64-gcc3/null/{}/Linux%204.4.0-53-generic%20(GTK%203.18.9,libpulse%208.0.0)/mint/1.0/update.xml"
        # Test an arbitrary number of unicode chars
        cdec = step = 42
        while cdec < 4200:
            channel = ''.join(unichr(c) for c in range(cdec, cdec + step) if unichr(c).isalpha())
            cdec += step
            url = url.format(channel)
            ret = self.client.get(url)
            self.assertEqual(ret.status_code, 200)
