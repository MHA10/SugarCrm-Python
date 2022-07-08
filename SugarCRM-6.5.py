import json
from hashlib import md5
import requests


class Rest:
    protocol = "https"
    uri = "https://instanceuri.com/"
    service_path = "service/v4_1/rest.php"
    user = "user"
    password_md5 = "password"
    resp = None

    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            protocol: str = "https",
            port: int = None,
    ):
        self.protocol = protocol
        if not port:
            if self.protocol == "https":
                self.uri = f"{protocol}://{host}/{self.service_path}"
            elif self.protocol == "http":
                self.uri = f"{protocol}://{host}/{self.service_path}"
        else:
            self.uri = f"{protocol}://{host}:{port}/{self.service_path}"
        self.user = user
        self.password_md5 = md5(password.encode("UTF-8")).hexdigest()
        self.resp = self.login()
        self.resp = json.loads(self.resp.text.replace("&#039;", "'"))

    def login_parameters(self):
        parameters = {
            "user_auth": {
                "user_name": self.user,
                "password": self.password_md5,
            },
            "application": "RestTest",
            "name_value_list": {},
        }
        return parameters

    def login(self):
        return self.call("login", self.login_parameters())

    def call(self, method: str, parameters):
        post = {
            "method": method,
            "input_type": "JSON",
            "response_type": "JSON",
            "rest_data": json.dumps(parameters),
        }
        return requests.post(self.uri, headers=None, data=post)

    def get_entry_list_parameters(self, session, module_name, select_fields=(), order_by="", max_results=0, offset=0,
                                  deleted=False, favorites=False):
        data = [session, module_name, "", order_by, offset, select_fields,
                (), max_results, int(deleted), int(favorites)]
        return data

    # Function to fetch records for a module
    def get_entry_list(self, method, session, module_name):
        post = {
            "method": method,
            "input_type": "JSON",
            "response_type": "JSON",
            "rest_data": json.dumps(self.get_entry_list_parameters(session, module_name)),
        }
        resp = requests.post(self.uri, headers=None, data=post)
        return json.loads(resp.text.replace("&#039;", "'"))

    def set_entry(self, session, module_name, name_value_list, track_view=0):
        data = [session, module_name, name_value_list, int(track_view)]
        post = {
            "method": "set_entry",
            "input_type": "JSON",
            "response_type": "JSON",
            "rest_data": json.dumps(data),
        }
        resp = requests.post(self.uri, headers=None, data=post)
        return json.loads(resp.text.replace("&#039;", "'"))


def main():
    rest = Rest(host="crmtest.teraquant.com", user="audacitystudios", password="uwu5ZGBEG6JgVA")
    session = rest.resp['id']
    module_res = rest.get_entry_list(method="get_entry_list", session=session, module_name="Contacts")

    name_value_list = [
        {
            "name": "id",
            "value": "9f5ad523-c526-9fe7-36fb-62c0a7aa6c8e",
        },
        {
            "name": "name",
            "value": "Test Account",
        },
        {
            "name": "website",
            "value": "http://google.com",
        }
    ]
    record_update_res = rest.set_entry(session=session, module_name="Accounts",
                                       name_value_list=name_value_list)


if __name__ == '__main__':
    main()
