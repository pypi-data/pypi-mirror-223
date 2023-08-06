import oss2
from oss2 import Auth, Bucket
from .setting.json_config import JsonConf

conf_url = '.aliOSS/conf.json'


class API:
    __access_key: str
    __access_secret: str
    __bucket: str
    __end_point: str
    __auth: Auth
    __buckets: Bucket

    def __init__(self):

        config = JsonConf(conf_url).config()
        self.__access_key = config.get('access_key')
        self.__access_secret = config.get('access_secret')  # '64507883e71fa7a1f9ace7c0c702d6431624569856'
        self.__bucket = config.get('bucket')  # 'dcdf9bf07f7dc24f8da6161fb0541f5c288503080'
        self.__end_point = config.get('end_point')
        self.__auth = oss2.Auth(self.__access_key, self.__access_secret)
        self.__buckets = oss2.Bucket(self.__auth, self.__end_point, self.__bucket)

    def upload_simple(self, file_name, file_url):

        headers = dict()
        headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PUBLIC_READ
        res = self.__buckets.put_object_from_file(file_name, file_url, headers=headers)
        if res.status == 200:
            return ('https://{}.{}/{}'.format(self.__bucket, self.__end_point, file_name))
