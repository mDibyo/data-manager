#!/usr/bin/env python

import csv


__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class Collection(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.data = None

    @classmethod
    def from_database(cls, db_collection):
        return cls([])

    def to_database(self):
        pass

    @classmethod
    def from_csv_file(cls, csv_file):
        return cls([])

    def to_csv_file(self):
        pass


def generate_database(csv_files):
    for csv_file in csv_files:
        collection = Collection.from_csv_file(csv_file)
        collection.to_database()


def generate_csv_files(db_collections):
    for db_collection in db_collections:
        collection = Collection.from_database(db_collection)
        collection.to_csv_file()
