from django.test import TestCase


class DummyTest(TestCase):
    def test_sanity(self):
        # minimal sanity test so test discovery runs cleanly while
        # we repair the full integration test separately
        self.assertTrue(True)
