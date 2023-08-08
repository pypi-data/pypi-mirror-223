import requests
from bs4 import BeautifulSoup
from .util import headers
from PIL import Image
import io
import json
import ast
class Client():
    def __init__(self):
        self.api = "https://student.gehu.ac.in"
        self.authenticated = False
        self.configured = False
        self.session = requests.Session()
        self.gen()
        # self.SessionId=None
        # self.RequestVerificationToken=None
    

    def parse_headers(self, data: str = None,type: str =None):
        if type:
            return headers.ApisHeaders(data=data).token_head
        else:
            return headers.ApisHeaders(data=data).headers
        
    def login_required(func):
        def wrapper(self, *args, **kwargs):
            if not self.authenticated:
                print("Login first")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def gen(self):
        response = self.session.get(self.api, headers=self.parse_headers(type="token"))

        cookies = response.cookies.get_dict()
        headers.SessionId = cookies.get('ASP.NET_SessionId')
        headers.RequestVerificationToken = cookies.get('__RequestVerificationToken')
        return [headers.RequestVerificationToken,headers.SessionId]
    

    def login_token(self):
        response = self.session.get(self.api, headers=self.parse_headers(type="token"))
        soup = BeautifulSoup(response.content, 'html.parser')
        verification_token_input = soup.find('input', {'name': '__RequestVerificationToken'})
        verification_token_value = verification_token_input['value']
        return verification_token_value

    def captcha(self):
        headers=self.parse_headers()
        headers["Content-Length"]="0"
        response =self.session.post(f"{self.api}/Account/showcaptchaImage", headers=headers)


        image_bytes = response.text
        py_list = ast.literal_eval(image_bytes)
        img_data = bytes(py_list)
        img = Image.open(io.BytesIO(img_data))
        
        img.show()
        code=input("captcha code :")
        return code
    def login(self,user, password):
        data = {
            'hdnMsg': 'GEU',
            'checkOnline': '',
            '__RequestVerificationToken':self.login_token(),
            'UserName': user,
            'Password': password,
            'clientIP': '',
            'captcha': f'{self.captcha()}'
        }
        data_str = "&".join([f"{k}={v}" for k, v in data.items()]).encode()

        

        response = requests.post(self.api, headers=self.parse_headers(data=data),data=data_str)
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        error_div = soup.find('div', class_='validation-summary-errors')

        if error_div:
            error_message = error_div.find('li').text.strip()
            print(f"Login Error: {error_message}")
            return None
        else:
            self.authenticated=True
            return response.text
        
    @login_required
    def info(self):
        response = requests.post(f"{self.api}/Account/GetStudentDetail", headers=self.parse_headers())
        
        return json.loads(response.json()['state'])[0]