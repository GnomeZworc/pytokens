# test_capitalize.py

from requests import get

base_url = "http://127.0.0.1"
first_port = 8000
second_port = 8001
first_token = 'api-token'
second_token = '32ewD9S7NbWBx5sN7JpX6S8WhoZLU71a0PBF9Yekwy2Uj7S3zuBDwW0IYRkpGaS8'

class TestApiBase():
    def get_response(self, url, head={}, port=80):
        response = get(url + ":" + str(port) + "/", headers=head)
        return response
    def test_base_response_with_token_text(self):
        headers = {'token':first_token}
        assert self.get_response(base_url, head=headers, port=first_port).text == '{"message": "hello"}'
    def test_base_response_with_token(self):
        headers = {'token':first_token}
        assert self.get_response(base_url, head=headers, port=first_port).status_code == 200
    def test_base_response_with_custom_token_text(self):
        headers = {'token':second_token}
        assert self.get_response(base_url, head=headers, port=second_port).text == '{"message": "hello"}'
    def test_base_response_with_custom_token(self):
        headers = {'token':second_token}
        assert self.get_response(base_url, head=headers, port=second_port).status_code == 200
    def test_base_response_without_token(self):
        assert self.get_response(base_url, port=second_port).status_code == 401
