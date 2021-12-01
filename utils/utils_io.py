import pandas as pd


class DataReader:
    def __init__(self):
        return self

    @staticmethod
    def read_from_db(db):
        return db.engine.execute("select * from database.table;")

    @staticmethod
    def read_data_from_a_file(file_path):
        return pd.read_csv(file_path)


def long_function_involving_reading_data():
    print("Starting function")
    dr = DataReader
    data = dr.read_data_from_a_file("/path/to/data")
    print("Finishing function")
    return data
