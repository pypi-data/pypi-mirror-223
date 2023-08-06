#  Copyright (c) 2023 7 25.
#  Coded By NoBody
#  Contact : https://t.me/Nobodycp
import requests


class SmsPlus:
    def __init__(self, check_panel_req):
        self.server_ip = check_panel_req['panel_server_ip']
        self.username = check_panel_req['panel_username']
        self.password = check_panel_req['panel_password']
        self.numbers = check_panel_req['numbers']

    def panel_login(self):
        s = requests.session()
        headers = {
            'Host': f'{self.server_ip}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': f'http://{self.server_ip}',
            'Referer': f'http://{self.server_ip}/index.php',
        }
        payloads = {
            'action': 'save',
            'sub': 'login',
            'username': f'{self.username}',
            'password': f'{self.password}',
        }
        try:
            s.post(f'http://{self.server_ip}/ajax_form_handler.php', headers=headers, data=payloads)
            return s
        except Exception as e:
            print(e)

    def check_number_on_panel(self):
        login = self.panel_login().cookies.get('PHPSESSID')
        # print(login)
        for number in self.numbers:
            try:
                headers = {
                    'Host': f'{self.server_ip}',
                    'Cookie': f'PHPSESSID={login}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': f'http://{self.server_ip}',
                    'Referer': f'http://{self.server_ip}/index.php?page=numbers&sub=numberslist&view=sms',
                }
                payloads = {
                    'sub': 'numberslist',
                    'pageview': 'sms',
                    'pageviewcnt': '1',
                    'pagesearch': f'{str(number).strip()}',
                    'pageno': '1',
                    'search_option': '1',
                    'action': 'get',
                }
                res = requests.post(f'http://{self.server_ip}/ajax_form_handler.php', headers=headers, data=payloads)
                # print(res.json())
                if res.json()['listcount'] != 1:
                    return 0
            except Exception as e:
                return str(e)

