import time
from . import util
from . import api
from . import entity

from .alios import api as aliapi
from .alios.setting.json_config import JsonConf

API = api.API
save = util.create_dir



def init(root_url='https://source.showdoc.com.cn/server/index.php?s='):
    print('input your ali access_key:')
    access_key = input()
    print('input your ali access_secret:')
    access_secret = input()
    print('input your ali bucket:')
    bucket = input()
    print('input your ali end_point:')
    end_point = input()
    ali_conf = JsonConf(aliapi.conf_url)
    ali_conf.put_dir({
        'access_key': access_key,
        'access_secret': access_secret,
        'bucket': bucket,
        'end_point': end_point
    })
    print('input your api_key:')
    api_key = input()
    print('input your api_token:')
    api_token = input()
    conf = JsonConf(api.conf_url)
    conf.put_dir({
        'api_key': api_key,
        'api_token': api_token,
        'root_url': root_url
    })
    my_api = API()
    project = my_api.project_get()
    print('project', project)
    conf.put_item('project', project)
    __download_no_key(project)


def download(*project):
    if project[0]:
        __download_no_key(project[0])
    else:
        __download_with_key()


def __download_with_key():
    my_api = API()
    project = my_api.project_get()
    exist = my_api.check_project(project)
    if isinstance(exist, str):
        util.create_dir(project)
    doc = my_api.menu_get(project)
    if isinstance(doc, str):
        FileNotFoundError(project + doc)
    print('file get successful')
    save_document(doc, project)
    print('download successful ')


def __download_no_key(project):
    my_api = API()

    exist = my_api.check_project(project)
    if isinstance(exist, str):
        raise FileNotFoundError(project + exist)

    doc = my_api.menu_get(project)

    util.create_dir(project)
    print('file get successful')
    save_document(doc, project)
    print('download successful ')


def upload(file_local: str):

    my_api = API()
    project = my_api.project_get()
    fileinfo = util.split_location(file_local, project)
    print(my_api.upload(fileinfo.title, fileinfo.content, fileinfo.dir))

def save_document(item: entity.Menu, local='.'):

    for page in item.pages:
        if page.page_title != '':
            file_name = local + '/' + page.page_title+'.md'
            util.create_file(file_name, page.page_content)
    for menu in item.catalogs:
        if menu.cat_name != '':
            d = local + '/' + str(menu.cat_name).strip()
            util.create_dir(d)
            save_document(menu, d)


def upload_image(arg: []):
    file_local = arg[2]
    my_api = API()
    project = my_api.project_get()
    fileinfo = util.split_location(file_local, project)
    if len(arg) >= 3:
        fileinfo.suffix = arg[3][arg[3].index('.')+1:]
    else:
        fileinfo.suffix = '.png'['.png'.index('.')+1:]
    if fileinfo.dir != '':
        fileinfo.title = '{}/{}/{}.{}'.format(fileinfo.dir, fileinfo.title, str(int(time.time())), fileinfo.suffix)
    else:
        fileinfo.title = '{}/{}.{}'.format(fileinfo.title, str(int(time.time())), fileinfo.suffix)
    print(fileinfo)
    api = aliapi.API()
    url = api.upload_simple(fileinfo.title, arg[3])
    print(url)
    return url


def back_up(project):
    __download_no_key(project)
    day = time.localtime()
    file_name = '{}-{}{}{}-{}.zip'.format(project,day.tm_year,day.tm_mon,day.tm_mday,day.tm_sec)
    util.create_zip(file_name, ''+project)

