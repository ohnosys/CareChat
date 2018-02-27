import os
import tornado
from tornado.options import define, options


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Apache経由などで動作させたりするとカレントディレクトリ等の関係でうまくいかないことがあるため絶対パスで取得

define('port', default=8888, help="run on the given port", type=int) # 指定できるオプションを定義
define('debug', default=True, help='debug mode')
tornado.options.parse_command_line() # 指定したコマンドライン解析 / ログローテートまでやってくれる

settings = {}
settings['debug'] = options.debug
settings['static_path'] = os.path.join(BASE_DIR, 'static')
settings['template_path'] = os.path.join(BASE_DIR, 'templates')
settings['cookie_secret'] = os.environ.get('SECRET_TOKEN', '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__')
settings['xsrf_cookies'] = True
settings['login_url'] = '/auth/login/'

from modules.modules import SearchBar, DeleteModal, CreateModal, EditModal
settings['ui_modules'] = {'SearchBar': SearchBar, 'DeleteModal': DeleteModal,
                          'CreateModal': CreateModal, 'EditModal': EditModal}

DATABASES = {
    'default': {
        'ENGINE': 'mysql+mysqlconnector',
        'NAME': 'exampledb',
        'USER': 'example_user',
        'PASSWORD': 'pass',
        'HOST': 'example-rds-mysql-server.cjdy4gezssw8.ap-northeast-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}
url_placeholder = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
url = url_placeholder.format(**DATABASES['default'])
