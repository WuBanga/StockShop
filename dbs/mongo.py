from app import mongo
from bson.objectid import ObjectId


class Mongo:

    @staticmethod
    def insert(collection, data, returned=False):
        if returned == True:
            db = mongo.get_database('stockshop')
            col = db.get_collection(collection)
            rtn_id = col.insert_one(data).inserted_id
            return rtn_id
        else:
            db = mongo.get_database('stockshop')
            col = db.get_collection(collection)
            rtn_id = col.insert_one(data)
    

    @staticmethod
    def return_collection(collection):
        db = mongo.get_database('stockshop')
        col = db.get_collection(collection)
        return col.find({})


    @staticmethod
    def delete(collection, delete_doc):
        db = mongo.get_database('stockshop')
        col = db.get_collection(collection)
        col.delete_one(delete_doc)


    @staticmethod
    def get_doc_by_id(collection, id):
        db = mongo.get_database('stockshop')
        col = db.get_collection(collection)
        return col.find({"_id": ObjectId(id)})


    @staticmethod
    def get_doc_by_part(collection, value):
        db = mongo.get_database('stockshop')
        col = db.get_collection(collection)
        return col.find({"id": value})

