import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from unomas.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'unomas')
    
    def test_get_guest(self):
        from unomas.views import get_guest_view
        request = testing.DummyRequest()
        info = get_guest_view(request)
        
    def test_post_guest(self):
        from unomas.views import post_guest_view
        request = testing.DummyRequest()
        request.POST['content'] = "Ooh la la"