# test_capitalize.py

from requests import get

base_url = "http://127.0.0.1:8080/"

class TestApiBase():
    def get_response(self, url):
        response = get(url)
        return response
    def test_base_response_text(self):
        assert self.get_response(base_url).text == '{"message": "hello"}'
    def test_base_response(self):
        assert self.get_response(base_url).status_code == 200
