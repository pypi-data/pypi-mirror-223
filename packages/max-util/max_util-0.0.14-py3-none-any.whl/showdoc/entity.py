class Page:
    item_id: str
    addtime: str
    cat_id: str
    s_number: str
    page_id: str
    author_uid: str
    author_username: str

    page_title: str
    page_comments: str
    page_content: str

    is_del: str

    ext_info: str
    attachment_count: str
    unique_key: str

    def __init__(self):
        self.item_id = ''
        self.addtime = ''
        self.cat_id = ''
        self.s_number = ''
        self.page_id = ''
        self.author_uid = ''
        self.author_username = ''

        self.page_title = ''
        self.page_comments = ''
        self.page_content = ''

        self.is_del = ''

        self.ext_info = ''
        self.attachment_count = ''
        self.unique_key = ''

    def __repr__(self):
        return 'page_title: {}' \
               'page_id: {}' \
               'page_content: {}'.format(self.page_title, self.page_id, self.page_content)


class Menu(object):
    item_id: str
    addtime: str
    cat_id: str
    cat_name: str
    s_number: str
    level: str
    catalogs: []
    pages: []
    parent_cat_id: str

    def __init__(self):
        self.item_id = ''
        self.addtime = ''
        self.cat_id = ''
        self.cat_name = ''
        self.s_number = ''
        self.level = ''
        self.catalogs = []

        self.pages = []
        self.parent_cat_id = ''

    def __repr__(self):
        return 'cat_name: {}' \
               ' catalogs: {}' \
               ' pages: {}' \
               ''.format(self.cat_name, self.catalogs, self.pages)


class FileInfo:
    content: str
    title: str
    dir: str
    suffix: str

    def __init__(self, title='', dir='', content='',suffix='' ):
        self.content = content
        self.title = title
        self.dir = dir
        self.suffix = suffix

    def __repr__(self):
        return 'title: {}' \
               ' dir: {}' \
               ' suffix: {}' \
               ' content: {}' \
               ''.format(self.title, self.dir, self.suffix, self.content)




