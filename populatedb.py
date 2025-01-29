import requests, random
from pymongo import MongoClient
import argparse

class MongoFiledDBError(Exception):
    """MongoFiledDB error"""

class MongoFiledDB():

    def __init__(self, mongo_uri, db_name, collection_name, reference_url=""):
        self.mongo_uri = mongo_uri
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.client[collection_name]
        self.reference_url = reference_url

    def get_data_from_reference_data_api(self, reference_url="", num_users=10):
        reference_url = reference_url or self.reference_url
        if not reference_url:
            raise MongoFiledDBError("Needed reference")
        # reference_url += f"/{num_users}"
        res = requests.get(reference_url, timeout=10)
        if res.status_code == 200:
            return random.choices(res.json(), k=num_users)
        raise MongoFiledDBError("Not valid response")
    
    def filter_relevant_data(self, reference_data, *args):
        users = []
        for sing_data in reference_data:
           users.append({k:v for k, v in sing_data.items() if k in args})
        return users

    def populate_mongo_db(self, users):
        try:
            self.collection.insert_many(users)
        except Exception:
            raise MongoFiledDBError("A problem occur while the data base was being field")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("-m", "--mongo_uri", help="The MongoDB URI", default="mongodb+srv://eleusiscarretero:J8nKfYYIuPa0XcJB@cluster0.73nlx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    parser.add_argument("-d", "--db_name",  help="The Name of the desired database", default="users_data")
    parser.add_argument("-c", "--collection_name",  help="The Name of the desired collection", default="users")
    parser.add_argument("-u","--url_reference",  help="The Name of the desired collection", default="https://jsonplaceholder.typicode.com/users")
    parser.add_argument("-f","--fields", nargs='+', help="Fields to filter", default=["name", "username", "address"])
    args = parser.parse_args()
    md_db = MongoFiledDB(args.mongo_uri, args.db_name, args.collection_name, args.url_reference)
    tmp_user_data = md_db.get_data_from_reference_data_api()
    md_db.filter_relevant_data(tmp_user_data, *args.fields)