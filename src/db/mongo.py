"""
MongoDB
"""
# External packages
import pandas as pd
from pymongo import MongoClient
import pymongo

# Local packages
from processing.job_offers import process_job

# Constants
DATA_LIMITS = 2048

class MongoDB:
    """
    """
    def __init__(self, config):
        self.host_ = config['host']
        self.port_ = int(config['port'])
        self.default_database_ = config['database_name']

    def connect(self) -> bool:
        """
        Connects to database and returns True if connection has been
        established otherwise False.
        """

        try:
            # Try to connect
            self.client_ = MongoClient(f"mongodb://{self.host_}:{self.port_}/")
            return True

        except Exception as e:
            # Display the problem
            print(f"Error occured at connect : {e}")
            return False
    
    def get_database(self, database_name=None):
        """
        Returns the database.
        """
        # Check if database name has been given otherwise we use
        # the default given by configuration
        if not database_name:
            database_name = self.default_database_
        return self.client_[database_name]
    
    def get_collection(self, collection_name=None, database_name=None):
        """
        Returns the collection.
        """
        # Check if database name has been given otherwise we use
        # the default given by configuration
        if not database_name:
            database_name = self.default_database_

        return self.get_database(database_name)[collection_name]

    def get_dataframe(self, collection_name=None) -> pd.DataFrame:
        """
        Returns a pandas.DataFrame
        """
        # Get the collection
        collection = self.get_collection(collection_name='job_offers')

        # Get the data
        jobs = [process_job(job) for job in collection.find({}).limit(DATA_LIMITS)]

        # Transform to pandas.DataFrame
        frame = pd.json_normalize(jobs)

        return frame

    def insert(self, collection_name=None, item=None) -> bool:
        """
        Insert an item to a specified collection and returns True
        if insertion was successful otherwise False.
        """
        # Get the collection
        collection = self.get_collection(collection_name='job_offers')

        try:
            # Insert operation
            if type(item) is dict:
                r = collection.insert_one(item)
            elif type(item) is list:
                r = collection.insert_many(item)

            return r

        except Exception as e:
            print(f"Problem in MongoDB.insert : {e}")
            return False


def df_to_formatted_json(df, sep="."):
    """
    The opposite of json_normalize
    """
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label,v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i==len(keys)-1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        # save
        result.append(parsed_row)
    return result
