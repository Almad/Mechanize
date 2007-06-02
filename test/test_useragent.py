#!/usr/bin/env python

from unittest import TestCase

import mechanize

from test_browser import make_mock_handler


class UserAgentTests(TestCase):

    def test_set_handled_schemes(self):
        class MockHandlerClass(make_mock_handler()):
            def __call__(self): return self
        class BlahHandlerClass(MockHandlerClass): pass
        class BlahProcessorClass(MockHandlerClass): pass
        BlahHandler = BlahHandlerClass([("blah_open", None)])
        BlahProcessor = BlahProcessorClass([("blah_request", None)])
        class TestUserAgent(mechanize.UserAgent):
            default_others = []
            default_features = []
            handler_classes = mechanize.UserAgent.handler_classes.copy()
            handler_classes.update(
                {"blah": BlahHandler, "_blah": BlahProcessor})
        ua = TestUserAgent()

        self.assertEqual(len(ua.handlers), 4)
        ua.set_handled_schemes(["http", "https"])
        self.assertEqual(len(ua.handlers), 2)
        self.assertRaises(ValueError,
            ua.set_handled_schemes, ["blah", "non-existent"])
        self.assertRaises(ValueError,
            ua.set_handled_schemes, ["blah", "_blah"])
        ua.set_handled_schemes(["blah"])

        req = mechanize.Request("blah://example.com/")
        r = ua.open(req)
        exp_calls = [("blah_open", (req,), {})]
        assert len(ua.calls) == len(exp_calls)
        for got, expect in zip(ua.calls, exp_calls):
            self.assertEqual(expect, got[1:])

        ua.calls = []
        req = mechanize.Request("blah://example.com/")
        ua._set_handler("_blah", True)
        r = ua.open(req)
        exp_calls = [
            ("blah_request", (req,), {}),
            ("blah_open", (req,), {})]
        assert len(ua.calls) == len(exp_calls)
        for got, expect in zip(ua.calls, exp_calls):
            self.assertEqual(expect, got[1:])
        ua._set_handler("_blah", True)


if __name__ == "__main__":
    import unittest
    unittest.main()
