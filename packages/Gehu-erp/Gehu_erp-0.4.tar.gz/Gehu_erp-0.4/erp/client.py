import requests
from bs4 import BeautifulSoup
from .util import headers,config
from PIL import Image
import io
import json
import ast
class Client():
    def __init__(self,use_config : bool=False):
        self.api = "https://student.gehu.ac.in"
        self.authenticated = False
        self.configured = False
        self.regId=None
        self.session = requests.Session()
        if use_config:
            if not config.load_config():
                self.gen()
            else:
                self.authenticated=True
                self.student_info()
        else:
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
                exit()
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

        

        response = self.session.post(self.api, headers=self.parse_headers(data=data),data=data_str)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        error_div = soup.find('div', class_='validation-summary-errors')

        if error_div:
            error_message = error_div.find('li').text.strip()
            print(f"Login Error: {error_message}")
            return None
        else:
            self.authenticated=True
            self.student_info()
            config.save_config(headers.SessionId,headers.RequestVerificationToken)
            return response.text
        
    @login_required
    def student_info(self):
        response = self.session.post(f"{self.api}/Account/GetStudentDetail", headers=self.parse_headers())
        if response.status_code==200:
            data=json.loads(response.json()['state'])[0]
            self.regId=data["RegID"]
            return data
    
    
    @login_required
    def all_sem_marksHistory(self):
        response = self.session.post(f"{self.api}/Web_Exam/GetStudentAllSemesterMarksHistory?RegID={self.regId}", headers=self.parse_headers())
        if response.status_code==200:
            return json.loads(response.json()['state'])
    
    
    @login_required
    def exam_Summary(self):
        response = self.session.post(f"{self.api}/Web_StudentAcademic/GetStudentExamSummary?RegID={self.regId}", headers=self.parse_headers())
        if response.status_code==200:
            return json.loads(response.json()['ExamSummary'])
        
    @login_required
    def profile_image(self, save_path="profile_image.png"):
        response = self.session.get(f"{self.api}/Account/show", headers=self.parse_headers())
        
        if response.status_code == 200:
            with open(save_path, "wb") as image_file:
                image_file.write(response.content)
            print(f"Profile image saved as {save_path}")
        else:
            print("Failed to fetch profile image")

    @login_required
    def upload_profile(self, img_path: str =None):
        
        files = {'helpSectionImages': ('profile_image.png', open(img_path, 'rb'), 'image/png')}
        
        response = self.session.post(f"{self.api}/SMS/UploadStudentPhoto?RegID={self.regId}",files=files, headers=self.parse_headers(type="multipart/form-data; boundary=----WebKitFormBoundaryAg6xlnZBrD2mJbPp"))
        if response.status_code==200:
            print("uploaded successfully")

    @login_required
    def change_password(self, new_password):
        data={
            "Password":new_password
        }
        data_str = "&".join([f"{k}={v}" for k, v in data.items()]).encode()
        response = self.session.post(f"{self.api}/Account/ChangeUserPassword?RegID={self.regId}",data=data_str,headers=self.parse_headers(data=data))
        if response.status_code==200:
            if response.json()["data"]==1:
                print("password changed")