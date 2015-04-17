#!/usr/bin/env python

import csv


__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class Collection(object):
    def __new__(cls, *args, **kwargs):
        class Entry(object):
            attrs = None
            id_attr = None

            attr_indices_map = {}
            id_attr_index = None

            def __init__(self, values):
                self.values = values

            def __getitem__(self, attr):
                index = self.attr_indices_map.get(attr, None)
                if index is None:
                    raise KeyError('attribute {} does not exist'.format(attr))
                return self.values[index]

        if len(args) >= 1:
            Entry.attrs = args[0]
        else:
            Entry.attrs = kwargs['attrs']
        for index, attr in enumerate(Entry.attrs):
            Entry.attr_indices_map[attr] = index
        if len(args) >= 2:
            Entry.id_attr = args[1]
        else:
            Entry.id_attr = kwargs.get('id_attr', None)
        if Entry.id_attr is not None:
            Entry.id_attr_index = Entry.attr_indices_map[Entry.id_attr]
        cls.Entry = Entry

        return super(Collection, cls).__new__(cls)

    def __init__(self, attrs, id_attr=None):
        self.attrs = attrs
        self.id_attr = id_attr
        self.entries = []

    @classmethod
    def from_database(cls, db_collection, id_attr=None):
        pass

    def to_database(self):
        pass

    @classmethod
    def from_csv_file(cls, csv_file, id_attr=None):
        pass

    def to_csv_file(self):
        pass

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.Entry(self.entries[item])
        elif self.id_attr is not None:
            for entry in self.entries:
                if entry[self.Entry.id_attr_index] == item:
                    return self.Entry(entry)

        raise KeyError('entry {} does not exist'.format(item))


def generate_database(csv_files):
    for csv_file in csv_files:
        collection = Collection.from_csv_file(csv_file)
        collection.to_database()


def generate_csv_files(db_collections):
    for db_collection in db_collections:
        collection = Collection.from_database(db_collection)
        collection.to_csv_file()
