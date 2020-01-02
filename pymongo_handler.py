from pymongo import MongoClient
import datetime
import json


class MongoHandler:

    def __init__(self, password):
        self.password = password
        # remove the string in MongoClient and replace with the one provided by you Mongodb Atlas account
        self.client = MongoClient(f'mongodb+srv://<USER_NAME>:{self.password}@cluster0-vspqb.azure.mongodb.net/test?retryWrites=true&w=majority')
        # create a db instance
        self.db = self.client.maindb
        # create a collection instance
        self.iot = self.db.iot
        


    def insert(self, deviceid, data):
        '''
            This method updates the measurements for a given date. If date or/and deviceid are not
            same (filter), a new document inserted because of { upsert: true } option.
            The data pushed in a list with field name samples and an inc variable count the total measurements.
            Data have the form, e.g. data = { "time": datetime.datetime.now().time(), "H": 45.9, "T": 7.8, "M": 79.8 },
            where T->temperature , H->humidity, M->moisture and time. The units are not stored.
            We have used local format for the date and time. Although, the most common format is UTC.
        '''
        self.iot.update_one({"deviceid": deviceid, "date":str(datetime.date.today())},
                                   {
                                       "$push": {"samples": data},
                                       "$inc": { "nd": 1 }
                                   },
                                   upsert = True )
        return

    def disconnect(self):
        self.client.close()
