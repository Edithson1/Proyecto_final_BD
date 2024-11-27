import pymysql

def get_connection():
    return pymysql.connect(
        host='junction.proxy.rlwy.net',
        user='root',
        password='GUGPuaDajYUZbtXKVvqgtmeWIeRrYuwM',
        database='BaseDatos',
        port=42752,
        cursorclass=pymysql.cursors.DictCursor
    )
