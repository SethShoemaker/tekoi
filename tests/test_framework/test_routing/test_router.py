import unittest
from tekoi.framework.routing import Router

class TestRouter(unittest.TestCase):

    def test_match_route__returns_empty_dict_for_base_path(self):
        router = Router([])

        match_result = router.match_route("GET", "/", "GET", "/")

        self.assertDictEqual({}, match_result)
        
    def test_match_route__returns_false_for_nonmatching_paths(self):
        router = Router([])

        match_result = router.match_route("GET", "/", "GET", "/login")

        self.assertFalse(match_result)

    def test_match_route__returns_dict_with_path_variables(self):
        router = Router([])

        match_result = router.match_route("GET", "/how-to-write-unit-tests", "GET", "/:post-slug")

        self.assertDictEqual({"post-slug": "how-to-write-unit-tests"}, match_result)

    def test_match_route__returns_false_for_nonmatching_paths_with_path_variables(self):
        router = Router([])

        match_result = router.match_route("GET", "/how-to-write-unit-tests/something", "GET", "/:post-slug/")

        self.assertFalse(match_result)

    def test_match_route__returns_false_for_nonmatching_methods(self):
        router = Router([])

        match_result = router.match_route("GET", "/hello", "PUT", "/hello")

        self.assertFalse(match_result)

    def test_match_route__returns_returns_dict_with_partial_wildcard(self):

        router = Router([])

        match_result = router.match_route("GET", "/hello/world", "GET", "/*/world")

        self.assertDictEqual({}, match_result)

    def test_match_route__returns_false_with_nonmatching_paths_and_partial_wildcard(self):

        router = Router([])

        match_result = router.match_route("GET", "/hello/world", "GET", "/*/world/*")

        self.assertFalse(match_result)

    def test_match_route__returns_dict_with_complete_wildcard(self):

        router = Router([])

        match_result = router.match_route("GET", "/hello/python/world", "GET", "/hello/**")

        self.assertDictEqual({}, match_result)
