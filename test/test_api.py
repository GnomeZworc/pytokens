# test_capitalize.py

from requests import get

base_url = "http://127.0.0.1:8000/"
api_token = 'api-token'

class TestApiBase():
    def get_response(self, url, head={}):
        response = get(url, headers=head)
        return response
    def test_base_response_with_token_text(self):
        headers = {'token':api_token}
        assert self.get_response(base_url, head=headers).text == '{"message": "hello"}'
    def test_base_response_with_token(self):
        headers = {'token':api_token}
        assert self.get_response(base_url, head=headers).status_code == 200
    def test_base_response_without_token(self):
        assert self.get_response(base_url).status_code == 401
