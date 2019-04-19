from pymongo import MongoClient
from bson.codec_options import CodecOptions
import pytz


class dbOperate():
    def __init__(self, host=None, port=None, mongo_str=None):
        self.host = host
        self.port = port
        if mongo_str:
            self.mongo_str = mongo_str
        else:
            self.mongo_str = 'mongodb://' + self.host + ':' + self.port

    def connect_db(self):
        """
            建立DB連線
            :return: 資料庫的連線狀態(object)
        """
        client = MongoClient(self.mongo_str)
        return client

    def close_db(self, client):
        """
            關閉Client端連線
            :param client:資料庫的連線狀態(object)
            :return:
        """
        client.close()
        return True

    def connect_db_name(self, client, db_name):
        """
            連結到該資料庫
            :param client: 資料庫的連線狀態(object)
            :param db_name: 要連線的資料庫名稱(string)
            :return: 資料庫連線狀態(object)
        """
        return client[db_name]

    def connect_collection(self, db, collection):
        """
            連結所傳入的collection
            :param db: 連線的資料庫(object)
            :param collection: 要連線的資料表名稱(string)
            :return: collection連線狀態(object)
        """
        return db[collection]

    # =============================================CRUD function=======================================
    def db_find(self, db_name, collection, condition, sort=None, limit=None, skip=None):
        """
            依據條件找尋資料庫中的資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param condition: 搜尋條件(json)
            :param sort: 排序方法(json)
            :param limit: 搜尋限制(json)
            :param skip: 搜尋限制(int)
            :return: 搜尋出來的資料(list)
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        data = None
        if sort and limit and skip:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).sort(sort).skip(skip).limit(limit)
        elif sort and limit:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).sort(sort).limit(limit)
        elif sort and skip:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei'))) \
                .find(condition).sort(sort).skip(skip)
        elif limit and skip:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).skip(skip).limit(limit)
        elif limit:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).limit(limit)
        elif sort:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).sort(sort)
        elif skip:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition).skip(skip)
        else:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find(condition)
        self.close_db(client)
        return list(data)

    def db_find_one(self, db_name, collection, condition, sort=None):
        """
            找collection中任意一筆資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param condition: 搜尋條件(json)
            :param sort: 排序方法(json)
            :return: 搜尋出來的資料(list)
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        data = None
        # pymongo3.1版以上有支援將讀出來的資料指定時區
        if sort:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find_one(condition).sort(sort)
        else:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei')))\
                .find_one(condition)
        self.close_db(client)
        return data

    def db_insert(self, db_name, collection, insert_data):
        """
            新增一筆資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param insert_data: 新增的資料(json)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        collection.insert_one(insert_data)
        self.close_db(client)

    def db_collection_count(self, db_name, collection, condition=None):
        """
            查詢此條件的資料筆數
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param condition: 查詢條件(json)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        data = None
        if condition:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei'))) \
                .find(condition).count()
        else:
            data = collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Taipei'))) \
                .find({}).count()
        self.close_db(client)
        return data

    def db_insert_many(self, db_name, collection, insert_data):
        """
            新增多筆資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param insert_data: 新增的資料(list)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        collection.insert_many(insert_data)
        self.close_db(client)

    def db_del_all(self, db_name, collection, condition):
        """
            刪除多筆資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱
            :param condition: 刪除的條件(json)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        collection.delete_many(condition)
        self.close_db(client)

    def db_update(self, db_name, collection, condition, data):
        """
            更新資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param condition: 更新的條件(json)
            :param data: 更新的資料(json)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        collection.update(condition, {'$set': data})
        self.close_db(client)

    def db_update_or_insert(self, db_name, collection, condition, data):
        """
            更新或新增資料
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :param condition: 更新的條件(json)
            :param data: 更新的資料(json)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        collection = db[collection]
        collection.update(condition, {'$set': data}, upsert=True)
        self.close_db(client)

    # =========================================初始化DB用function==============================
    def get_all_db_name(self):
        """
            取得目前連線的位置中每個資料庫的名稱
            :return:
        """
        client = self.connect_db()
        all_db_name = client.database_names()
        self.close_db(client)
        return all_db_name

    def get_all_collection_name(self, db_name):
        """
            取得傳入資料庫中，所有collection的名稱
            :param db_name: 資料庫名稱(string)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        all_collection_name = db.collection_names()
        self.close_db(client)
        return all_collection_name

    def create_db_and_collection(self, db_name, collection):
        """
            建立資料庫及collection
            :param db_name: 資料庫名稱(string)
            :param collection: collection名稱(string)
            :return:
        """
        client = self.connect_db()
        db = self.connect_db_name(client, db_name)
        db.create_collection(collection)
        self.close_db(client)
