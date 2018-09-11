# test_capitalize.py

from requests import get, post
from time import sleep

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

class TestCreateToken():
    def get_response(self, url, head={}, port=80, data='{}'):
        response = post(url + ":" + str(port) + "/create", headers=head, data = data)
        return response
    def test_create_without_data(self):
        headers = {'token':first_token}
        assert self.get_response(base_url, head=headers, port=first_port).status_code == 400
    def test_create_without_id(self):
        headers = {'token':first_token}
        datas = '{"source":"perso", "limit_time":0}'
        assert self.get_response(base_url, head=headers, port=first_port, data=datas).status_code == 400
    def test_create_without_time_limit(self):
        headers = {'token':first_token}
        datas = '{"source":"perso", "id":1}'
        assert self.get_response(base_url, head=headers, port=first_port, data=datas).status_code == 400
    def test_create_without_source(self):
        headers = {'token':first_token}
        datas = '{"id":1, "limit_time":0}'
        assert self.get_response(base_url, head=headers, port=first_port, data=datas).status_code == 400
    def test_create_with_data(self):
        headers = {'token':first_token}
        datas = '{"source":"perso","id":1,"limit_time":0}'
        assert self.get_response(base_url, head=headers, port=first_port, data=datas).status_code == 200
    def test_create_with_no_duplicate(self):
        headers = {'token':first_token}
        datas = '{"source":"perso","id":1,"limit_time":0}'
        first = self.get_response(base_url, head=headers, port=first_port, data=datas).json()["token"]
        second =  self.get_response(base_url, head=headers, port=first_port, data=datas).json()["token"]
        assert first == second

class TestCheckToken():
    def get_response(self, url, head={}, port=80, data='{}', route=''):
        response = post(url + ":" + str(port) + "/" + route, headers=head, data = data)
        return response
    def test_id_valid_check_with_data_without_correct_token(self):
        headers = {'token':first_token}
        source = 'pioupiou'
        token = 'lolicool'
        data2 = '{"source":"' + source + '","token":"' + token +'"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='check').json()
        assert ret["is_valid"] == 0
    def test_is_valid_check_with_data_with_correct_token(self):
        headers = {'token':first_token}
        source_id = 15
        source = 'pioupiou'
        time_limit = 3600
        data1 = '{"source":"' + source + '","id":"' + str(source_id) +'","limit_time":"' + str(time_limit) + '"}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        data2 = '{"source":"' + source + '","token":"' + token +'"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='check').json()
        assert ret["is_valid"] == 1
    def test_id_check_with_data_with_correct_token(self):
        headers = {'token':first_token}
        source_id = 15
        source = 'pioupiou'
        time_limit = 3600
        data1 = '{"source":"' + source + '","id":"' + str(source_id) +'","limit_time":"' + str(time_limit) + '"}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        data2 = '{"source":"' + source + '","token":"' + token +'"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='check').json()
        assert ret["id"] == source_id

class TestDeleteToken():
    def get_response(self, url, head={}, port=80, data='{}', route=''):
        response = post(url + ":" + str(port) + "/" + route, headers=head, data = data)
        return response
    def test_is_valid_delete_without_valid_token(self):
        headers = {'token':first_token}
        source = 'pioupiou'
        token = 'lol'
        data = '{"source":"' + source + '","token":"' + token + '"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data, route='delete').json()
        assert ret["is_valid"] == 0
    def test_is_valid_delete_with_valid_token(self):
        headers = {'token':first_token}
        source = 'pioupiou'
        data1 = '{"source":"' + source + '","id":1,"limit_time":0}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        data2 = '{"source":"' + source + '","token":"' + token + '"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='delete').json()
        assert ret["is_valid"] == 1
    def test_is_deleted_delete_with_valid_token(self):
        headers = {'token':first_token}
        source = 'pioupiou'
        data1 = '{"source":"' + source + '","id":1,"limit_time":0}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        data2 = '{"source":"' + source + '","token":"' + token + '"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='delete').json()
        assert ret["is_deleted"] == 1

class TestTimeDelete():
    def get_response(self, url, head={}, port=80, data='{}', route=''):
        response = post(url + ":" + str(port) + "/" + route, headers=head, data = data)
        return response
    def test_time_with_correct_time(self):
        headers = {'token':first_token}
        source_id = 15
        source = 'pioupiou'
        time_limit = 3600
        data1 = '{"source":"' + source + '","id":"' + str(source_id) +'","limit_time":"' + str(time_limit) + '"}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        sleep(2)
        data2 = '{"source":"' + source + '","token":"' + token +'"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='check').json()
        assert ret["id"] == source_id
    def test_time_without_correct_time(self):
        headers = {'token':first_token}
        source_id = 18
        source = 'pioupiou'
        time_limit = 1
        data1 = '{"source":"' + source + '","id":"' + str(source_id) +'","limit_time":"' + str(time_limit) + '"}'
        token = self.get_response(base_url, head=headers, port=first_port, data=data1, route='create').json()["token"]
        sleep(2)
        data2 = '{"source":"' + source + '","token":"' + token +'"}'
        ret = self.get_response(base_url, head=headers, port=first_port, data=data2, route='check').json()
        assert ret["is_valid"] == 0
