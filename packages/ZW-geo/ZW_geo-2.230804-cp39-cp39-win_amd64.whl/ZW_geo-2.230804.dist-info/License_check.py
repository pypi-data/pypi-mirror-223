#!/usr/bin/python3
import uuid
from binascii import b2a_hex, a2b_hex
from datetime import datetime

import pymysql
from Crypto.Cipher import AES


class LicenseGenerate:
    def __init__(self, host, user, passwd, port, database, client_data=None):
        try:
            self.db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=database)
            print('连接成功！')
        except pymysql.err.OperationalError:
            print('something wrong!')
        self.client_name, self.deal_date, self.deadline_date, self.MAC = client_data
        self.license = self.encrypt(f'{self.MAC}#{self.deadline_date}', self.MAC, self.deadline_date)
        client_data.append(self.license)
        self.client_data = client_data

    @staticmethod
    def create_database(_cursor):
        # 创建数据库LICENSE
        _cursor.execute("CREATE DATABASE IF NOT EXISTS LICENSE")

    @staticmethod
    def create_table(_cursor):
        # 创建表LICENSE
        _cursor.execute("DROP TABLE IF EXISTS LICENSE")
        _cursor.execute('''CREATE TABLE LICENSE (
                     client_name CHAR(100) PRIMARY KEY,
                     deal_date CHAR(100),
                     deadline_date CHAR(100),
                     MAC CHAR(100),
                     license CHAR(100))''')

    @staticmethod
    def insert_data(_cursor, _data):
        # 插入数据
        sql = """INSERT INTO LICENSE(client_name, deal_date, deadline_date, MAC, license)
                 VALUES (%s, %s, %s, %s, %s)"""
        _cursor.execute(sql, _data)

    @staticmethod
    def update_data(_cursor, _client_name, _deal_date, _deadline_date, _MAC, _license):
        # 修改数据
        _cursor.execute("UPDATE LICENSE SET deal_date=%s, deadline_date=%s, MAC=%s, license=%s WHERE client_name = %s",
                        (_deal_date, _deadline_date, _MAC, _license, _client_name))

    @staticmethod
    def gen_secret_key(mac_addr):
        while len(mac_addr) % 16:
            mac_addr += "ZW_geometry_lib"[len(mac_addr) % 16 - 1]
        return mac_addr

    @staticmethod
    def encrypt(content, secret_key, date):
        secret_key = LicenseGenerate.gen_secret_key(secret_key).encode('utf-8')
        init_vector = date * 2
        # key: The secret key to use in the symmetric cipher.
        # iv: The initialization vector to use for encryption or decryption which must be 16 bytes long.
        aes = AES.new(key=secret_key, mode=AES.MODE_CBC, iv=init_vector.encode('utf-8'))
        content += (16 - len(content) % 16) * " "
        encrypted_content = aes.encrypt(content.encode('utf-8'))
        return b2a_hex(encrypted_content).decode('utf-8')

    def while_deal(self):
        with self.db:
            cursor = self.db.cursor()
            # 交易完成时
            try:
                self.insert_data(cursor, self.client_data)
            except pymysql.err.IntegrityError:
                self.update_data(cursor, self.client_name, self.deal_date, self.deadline_date, self.MAC, self.license)
            self.db.commit()
            print("data uploaded!")


class LicenseCheck:
    def __init__(self, host, user, passwd, port, database, client_name):
        try:
            self.db = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=database)
            print('连接成功！')
        except pymysql.err.OperationalError:
            print('something wrong!')
        self.client_name = client_name

    @staticmethod
    def select_data(_cursor, _client_name):
        # 匹配数据
        _cursor.execute("SELECT * FROM LICENSE WHERE client_name = (%s)", _client_name)  # 数据筛选
        # cursor.execute("SELECT * FROM LICENSE")  # 全部数据
        _results = _cursor.fetchall()
        return _results[0]

    @staticmethod
    def decrypt(content, secret_key, date):
        # secret_key: The secret secret_key to use in the symmetric cipher.
        # iv: The initialization vector to use for encryption or decryption which must be 16 bytes long.
        init_vector = date * 2
        aes = AES.new(key=secret_key.encode('utf-8'), mode=AES.MODE_CBC, iv=init_vector.encode('utf-8'))
        decrypted_content = aes.decrypt(a2b_hex(content.encode('utf-8')))
        return decrypted_content.decode('utf-8')

    @staticmethod
    def gen_secret_key(mac_addr):
        while len(mac_addr) % 16:
            mac_addr += "ZW_geometry_lib"[len(mac_addr) % 16 - 1]
        return mac_addr

    @staticmethod
    def get_mac_addr():
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    @staticmethod
    def license_check(mac_attr, deadline_date, license):
        secret_key = LicenseCheck.gen_secret_key(mac_attr)
        sign = LicenseCheck.decrypt(license, secret_key, deadline_date)
        sign_list = sign.split('#')
        mac, date = map(str.strip, sign_list)
        if (mac != mac_attr) or (date != deadline_date):  # Check license file is modified or not.
            raise ValueError("License file is modified!")
        if len(sign_list) == 2:  # Check MAC and effective date invalid or not.
            mac = LicenseCheck.get_mac_addr()
            _current_date = datetime.now().strftime('%Y%m%d')
            if mac != mac:  # Must run this script under specified MAC.
                raise ValueError("Invalid host!")
            if date < _current_date:  # Current time must be before effective date.
                raise ValueError("License is expired!")
        else:
            raise ValueError("Wrong Sign setting on license file.")
        print("license checked!")

    def while_import(self):
        with self.db:
            cursor = self.db.cursor()
            # 客户调用时
            client_name, deal_date, deadline_date, MAC, license = self.select_data(cursor, self.client_name)
            # print(license)
            self.license_check(MAC, deadline_date, license)


if __name__ == "__main__":
    # client_name = 'Runtian Lee'
    # deal_date = '20230703'
    # deadline_date = '20230813'
    # MAC = '58:11:22:cf:07:49'

    client_name = 'Igasylng Seren'  # 显式
    deal_date = '20230703'  # 隐式
    deadline_date = '20330703'  # 隐式
    MAC = '9C:B6:D0:C0:43:C5'  # 隐式
    # license为显式

    data = [client_name, deal_date, deadline_date, MAC]

    # lg = LicenseGenerate(host='192.168.2.133', user='root', passwd='230703', port=3306, database='LICENSE',
    #                      client_data=data)
    lc = LicenseCheck(host='192.168.2.133', user='root', passwd='230703', port=3306, database='LICENSE',
                      client_name='Igasylng Seren')

    # lg.while_deal()
    lc.while_import()
