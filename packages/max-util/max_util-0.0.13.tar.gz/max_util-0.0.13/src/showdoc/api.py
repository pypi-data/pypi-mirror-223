import requests
from . import entity
from .alios.setting.json_config import JsonConf

conf_url = '.showDoc/conf.json'


class API:
    __conf_url: str
    __root_url: str
    __api_key: str
    __api_token: str
    __project: str

    def __init__(self):


        config = JsonConf(conf_url).config()
        self.__root_url = config.get('root_url')
        self.__api_key = config.get('api_key')  # '64507883e71fa7a1f9ace7c0c702d6431624569856'
        self.__api_token = config.get('api_token')  # 'dcdf9bf07f7dc24f8da6161fb0541f5c288503080'
        self.__project = config.get('project')


    def project_get(self):
        return self.__project

    def page_get(self, page_id):
        url = '/api/page/info'
        param = {
            'page_id': page_id
        }

        res = requests.post(self.__root_url + url, param).json()
        if res['error_code'] == 0:
            return parse_page(res['data'])
        return entity.Page()

    def upload(self, page_title, page_content, cat_name = ''):
        if not self.__api_key or self.__api_key == "":
            raise NotImplementedError('no inited')
        url = '/api/item/updateByApi'
        param = {
            'api_key': self.__api_key,
            'api_token': self.__api_token,
            'cat_name': cat_name,
            'page_title': page_title,
            'page_content': page_content
        }
        print(param)
        res = requests.post(self.__root_url + url, param).json()
        if res['error_code'] == 0:
            return 'upload success'
        return res['error_message']

    def check_project(self, project):
        url = '/api/item/info'
        param = {
            'item_id': project
        }
        res = requests.post(self.__root_url + url, param).json()
        if res['error_code'] == 0:
            return True
        return res['error_message']

    def menu_get(self):
        url = '/api/item/info'
        param = {
            'api_key': self.__api_key,
            'api_token': self.__api_token,
        }
        res = requests.post(self.__root_url + url, param).json()
        if res['error_code'] == 0:
            return parse_menu(res['data']['menu'])
        return res['error_message']

    def menu_get(self, project):
        url = '/api/item/info'
        param = {
            'item_id': project
        }
        res = requests.post(self.__root_url + url, param).json()
        if res['error_code'] == 0:
            return parse_menu(res['data']['menu'])
        return res['error_message']


def parse_menu(item: object):
    m = entity.Menu()

    for field in ('item_id', 'cat_name', 'addtime', 'cat_id', 's_number', 'level'):
        if field in item:
            setattr(m, field, item[field])
    m.catalogs = parse_menus(item['catalogs'])
    m.pages = parse_pages(item['pages'])
    return m


def parse_menus(items: []):
    menus = []
    for item in items:
        menus.append(parse_menu(item))
    return menus


def parse_pages(items: []):
    pages = []
    for item in items:
        pages.append(API().page_get(item['page_id']))
    return pages


def parse_page(item):
    m = entity.Page()
    m.page_id = item['page_id']
    m.author_uid = item['author_uid']
    m.cat_id = item['cat_id']
    m.page_title = item['page_title']

    m.addtime = item['addtime']
    m.ext_info = item['ext_info']
    m.s_number = item['s_number']
    m.item_id = item['item_id']
    m.author_username = item['author_username']

    m.page_comments = item['page_comments']
    m.page_content = item['page_content']
    m.is_del = item['is_del']
    m.attachment_count = item['attachment_count']
    m.unique_key = item['unique_key']
    return m
