import unittest
from argparse import Namespace
from proxy_client import build_config, quoted

def args(**kw):
    d=dict(url='https://example.com',country='US',state=None,city=None,session=None,asn=None,timeout=15,protocol='http')
    d.update(kw)
    return Namespace(**d)
META={'proxy_host':'proxy.example.com','http_port':8080,'socks_port':1080}
V2={'IPLOOP_PROXY_USERNAME':'user123','IPLOOP_PROXY_PASSWORD':'fake_password'}
class Contract(unittest.TestCase):
    def test_v2(self):
        self.assertIn('user123-country-us:fake_password',build_config(args(),V2,META))
    def test_legacy(self):
        self.assertIn('iploop:legacy-country-US',build_config(args(),{'IPLOOP_API_KEY':'legacy'}))
    def test_partial(self):
        with self.assertRaises(ValueError):build_config(args(),{'IPLOOP_PROXY_USERNAME':'user123'},META)
    def test_country(self):
        for c in ['ZZ','USA','US-session-x']:
            with self.assertRaises(ValueError):build_config(args(country=c),V2,META)
    def test_city_gate(self):
        with self.assertRaises(ValueError):build_config(args(state='tx',city='austin'),V2,META)
    def test_future_city(self):
        self.assertIn('-country-us-state-tx-city-austin:',build_config(args(state='tx',city='austin'),dict(V2,IPLOOP_V2_CITY_ENABLED='1'),META))
    def test_city_requires_state(self):
        with self.assertRaises(ValueError):build_config(args(city='austin'),dict(V2,IPLOOP_V2_CITY_ENABLED='1'),META)
    def test_session(self):
        self.assertIn('-session-demo123:',build_config(args(session='demo123'),V2,META))
        with self.assertRaises(ValueError):build_config(args(session='x-city-austin'),V2,META)
    def test_asn(self):
        with self.assertRaises(ValueError):build_config(args(asn='123'),V2,META)
    def test_socks(self):
        self.assertIn('socks5h://',build_config(args(protocol='socks5h'),V2,META))
    def test_no_creds(self):
        with self.assertRaises(ValueError):build_config(args(),{})
    def test_bad_meta(self):
        for m in [dict(META,http_port=True),dict(META,proxy_host='127.0.0.1'),dict(META,proxy_host='bad/user')]:
            with self.assertRaises(ValueError):build_config(args(),V2,m)
    def test_newline(self):
        with self.assertRaises(ValueError):quoted('bad\nconfig')
    def test_timeout(self):
        with self.assertRaises(ValueError):build_config(args(timeout=121),V2,META)
if __name__=='__main__':unittest.main()
