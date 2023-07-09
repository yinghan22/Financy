"""
@file    : Config.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/04/09 14:40
"""

base_server_url = '127.0.0.1'

Config = {
    'server': {
        'host': '127.0.0.1',
        'port': 8000
    },
    'redis_server': 'redis://{}:6379/0'.format(base_server_url),
    # 'mysql_server': 'mysql://root:123456@{}:3306/FinancySystem'.format(base_server_url),
    'db_server': 'sqlite://db.sqlite3',
    'time': {
        'day': 60 * 60 * 24,
        'three_day': 60 * 60 * 24 * 3,
        'five_day': 60 * 60 * 24 * 5,
        'week': 60 * 60 * 24 * 7,
    }
}
