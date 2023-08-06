import random
import requests
from colorama import Fore
from colorama import init as colorama_init
from colorama import Style
from close_bullet.External_Op import SmsPlus
import configparser
from pystyle import *
import ctypes
import subprocess
import sys
import win32gui
import wmi
c = wmi.WMI()
colorama_init()


class App:
    @staticmethod
    def welcome_message(user_name):
        # print(f"{Fore.GREEN}{Back.RED}{Style.DIM}Hello")
        _Hello = Box.Lines(f'Welcome {user_name}\n'
                          f'Coded By : 01 Team')
        Write.Print(_Hello, Colors.red_to_green, interval=0.03)
    @staticmethod
    def config():
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.sections()
            return config
        except Exception as e:
            raise e
    @staticmethod
    def get_number_of_session() -> int:
        # process_list = []
        counter = 0
        # print(sys.argv[0].split("\\")[-1].strip())
        if '\\' in sys.argv[0]:
            code_name = sys.argv[0].split("\\")[-1].strip().replace(".exe", '')
        else:
            code_name = sys.argv[0].split("/")[-1].strip().replace(".py", '')
        for process in c.Win32_Process():
            # print(process.Name)
            if code_name in str(process.Name):
                counter += 0.5
                # process_list.append(str(process.Name))
        return int(counter)
    @staticmethod
    def get_hardware_id() -> str:
        """
        this is fun for get numbers from file to check
        :return: numbers form list
        """
        try:
            hwid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
            return hwid
        except:
            raise Exception("Cant get hardware id ...")
    @staticmethod
    def terminal():
        try:
            app_name = sys.argv[0].split('\\')[-1].split('.')
            # print(app_name)
            if app_name[1] == 'exe':
                hwnd = win32gui.GetForegroundWindow()
                # ctypes.windll.user32.SetWindowPos(the_program_to_hide, 0, 0, 0, 700, 300, 0)
                win32gui.SetWindowPos(hwnd, 0, 0, 0, 700, 300, 0)
                app_name = sys.argv[0].split('\\')[-1].split('.')[0]
                ctypes.windll.kernel32.SetConsoleTitleW(f'{app_name} | Coded By 01 Team')
            else:
                pass
        except Exception as e:
            raise e
    def start(self):
        try:
            user_config = self.config()
            self.terminal()
            security_payloads = {
                'Threads': int(user_config['GENRERL']['Threads']),
                'Key': user_config['ROOT']['Key'],
                'HWID': self.get_hardware_id(),
                'Session_Number': self.get_number_of_session(),
                'List_name': user_config['LISTS']['numbers']
            }
            user_name = Security(security_payloads).root_setting['full_name']
            self.welcome_message(user_name)
        except Exception as e:
            raise e


class OpenFiles:
    settings_LISTS_Randomize = App.config().getboolean('LISTS', 'Randomize')
    @staticmethod
    def proxylist_(settings_proxy_list_name='proxy.txt'):
        try:
            with open(settings_proxy_list_name) as proxylist:
                # print("Open proxy")
                proxylist = proxylist.readlines()
            return proxylist
        except Exception as e:
            raise Exception(f"proxy.txt Have error ---> {e}")

    @staticmethod
    def list(list_name='numbers.txt', random_=settings_LISTS_Randomize):
        try:
            with open(list_name) as list_:
                list_ = list_.readlines()
                if random_:
                    return random.sample(list_, len(list_))
                else:
                    return list_
        except Exception as e:
            raise e

class ProcessStatus:
    Successfully = 0
    Failed = 0
    Retry = 0
    counter = 0
    def __init__(self, list_):
        self.total = len(list_)
    def prient_res(self):
        # print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")
        print(f"{Style.RESET_ALL}\r [ {self.counter} From {self.total}] | {Fore.GREEN}{self.Successfully}{Style.RESET_ALL} | "
              f"{Fore.RED}{self.Failed}{Style.RESET_ALL} --> ", end = '')

class Security:
    nobody_server_ip = "http://84.32.128.212:8000/api/v1/clients/detail/"
    def __init__(self, security_config_req):
        self.security_config_req = security_config_req
        self.root_setting = self.root_setting()
        self.check_max_session()
        self.check_user_group()
        self.check_if_user_ban()
        self.check_max_threads()
    def check_if_user_ban(self):
        """
        this is fun for check if user is ban or not
        :return: 1 = True , else for error or deny
        """
        if not self.root_setting['is_active']:
            raise Exception("Your Baned Connect Support To Check Problem ...")
        return 1
    def check_max_threads(self):
        """
        this is fun for check max threads for user
        :return: 1 = True , else for error or deny
        """
        # print(self.np_setting)
        if int(self.security_config_req['Threads']) >= int(self.root_setting['max_threads']):
            raise Exception(f"You Cant Use More Than {self.root_setting['max_threads']} Threads You Are Using {self.security_config_req['Threads']}.")
        return 1
    def check_max_session(self):
        """
        this is fun for check max session for user
        :return: 1 = True , else for error or deny
        """
        if self.security_config_req["Session_Number"] > int(self.root_setting['max_session']):
            raise Exception(f"You Cant Use More Than {self.root_setting['max_session']} Session You Are Using {self.security_config_req['Session_Number']}")
        return 1
    def check_user_group(self): # not completed
        # add telegram report
        """
        this is fun for check max session for user
        :return: 1 = True , else for error or deny
        """
        if self.root_setting['user_group'] != '0':
            print("This is not Supper User Limited Work")
            payloads = {
                'List_name': self.security_config_req['List_name'],
                'number_of_random_to_check': self.root_setting['number_of_random_to_check'],
            }
            numbers = self.get_numbers_for_check_with_panel(payloads)
            payloads = {
                'panel_server_ip': self.root_setting['panel_server_ip'],
                'panel_username': self.root_setting['panel_username'],
                'panel_password': self.root_setting['panel_password'],
                'numbers': numbers,
            }
            check_number_in_panel = SmsPlus(payloads).check_number_on_panel()
            if check_number_in_panel == 0:
                raise Exception("Fuck U Go way we dont need more fucken persons !!!")
    def root_setting(self): # not completed
        # add telegram report for thief | should create as soon
        # add trojen for fuck thief ---- not important for now
        payloads = {
            'key': f'{self.security_config_req["Key"]}',
            'hwID': f'{self.security_config_req["HWID"]}',
        }
        req = requests.post(self.nobody_server_ip, json=payloads)
        # print(req.text)
        if '{"detail":"Not found."}' in req.text:
            # print("EEEEE")
            raise Exception(f"Your Hardware id {self.security_config_req['HWID']} Not Defined..")
            # print(f"Your Hardware id {self.hardware_id} Not Defined..")
            # exit()
        else:
            return req.json()
    @staticmethod
    def get_numbers_for_check_with_panel(check_numbers_req:dir()) -> list[str]:
        """
        this is fun for get numbers from file to check
        :return: numbers form list
        """
        check_list = []
        try:
            for n in range(int(check_numbers_req['number_of_random_to_check'])):
                combo_list = open(check_numbers_req['List_name'], 'r').readlines()
                number = combo_list[random.randrange(len(combo_list))].strip()
                check_list.append(number.strip().replace("+", ''))
        except:
            raise Exception("Your Number List is Empty..")
        return check_list


class Requests:
    app_confing = App.config()
    settings_active_proxy = App.config().getboolean('PROXY', 'Active')
    settings_proxy_type = str(App.config()["PROXY"]['Type'])
    settings_proxy_list_name = str(App.config()["PROXY"]['List'])
    proxy_list = OpenFiles.proxylist_(settings_proxy_list_name)
    def proxy_session(self):
        # print(self.settings_active_proxy)
        s = requests.session()
        if self.settings_active_proxy:
            proxy = self.proxy_list[random.randrange(len(self.proxy_list))].strip()
            s.proxies = {
                'http': f'{self.settings_proxy_type}://{proxy}',
                'https': f'{self.settings_proxy_type}://{proxy}',
                }
            return s
        else:
            return s
