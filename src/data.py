#!/usr/bin/env python

import os.path as osp
import csv

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class DataTable(object):
    db_char_swaps = [('.', '*')]

    def __new__(cls, *args, **kwargs):
        class Entry(object):
            attrs = None
            id_attr = None

            attr_indices_map = {}
            id_attr_index = None

            db_char_swaps = cls.db_char_swaps

            def __init__(self, values):
                self.values = values

            def __getitem__(self, attr):
                index = self.attr_indices_map.get(attr, None)
                if index is None:
                    raise KeyError('attribute "{}" does not exist'.format(attr))
                return self.values[index]

            def __repr__(self):
                return str({attr: self.values[index] for attr, index
                            in self.attr_indices_map.iteritems()})

            @classmethod
            def from_db(cls, db_entry):
                values = [None] * len(cls.attrs)
                for attr, value in db_entry.iteritems():
                    for real_char, db_char in cls.db_char_swaps:
                        attr = attr.replace(db_char, real_char)
                    values[cls.attr_indices_map[attr]] = value

                return Entry(values)

            def to_db(self):
                db_entry = {}
                for attr in self.attrs:
                    value = self.values[self.attr_indices_map[attr]]
                    for real_char, db_char in self.db_char_swaps:
                        attr = attr.replace(real_char, db_char)
                    db_entry[attr] = value

                return db_entry

        print args, kwargs

        if len(args) >= 2:
            Entry.attrs = args[1]
        else:
            Entry.attrs = kwargs['attrs']
        for index, attr in enumerate(Entry.attrs):
            Entry.attr_indices_map[attr] = index
        if len(args) >= 3:
            Entry.id_attr = args[2]
        else:
            Entry.id_attr = kwargs.get('id_attr', None)
        if Entry.id_attr is not None:
            Entry.id_attr_index = Entry.attr_indices_map[Entry.id_attr]
        cls.Entry = Entry

        return super(DataTable, cls).__new__(cls)

    def __init__(self, name, attrs, id_attr=None):
        self.name = name
        self.attrs = attrs
        self.id_attr = id_attr
        self._entries = []
        self.id_attr_entries_map = {}

        if self.id_attr is not None:
            self.id_attr_index = self.attrs.index(self.id_attr)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.Entry(self.entries[item])
        elif isinstance(item, slice):
            step = 1 if item.step is None else item.step
            return [self.Entry(self.entries[index]) for index
                    in xrange(item.start, item.stop, step)]
        elif self.id_attr is not None:
            return self.Entry(self.id_attr_entries_map[item])

        raise KeyError('entry "{}" does not exist'.format(item))

    @property
    def entries(self):
        return self._entries

    @entries.setter
    def entries(self, entries):
        self._entries = entries

        id_attr_index = self.id_attr_index
        for entry in self._entries:
            self.id_attr_entries_map[entry[id_attr_index]] = entry

    @entries.deleter
    def entries(self):
        self._entries = []
        self.id_attr_entries_map = {}

    @classmethod
    def from_db(cls, db_collection, id_attr=None):
        attrs = []
        for attr in db_collection.find_one().iterkeys():
            for real_char, db_char in cls.db_char_swaps:
                attr = attr.replace(db_char, real_char)
            attrs.append(attr)
        table = cls(db_collection.name, attrs, id_attr)

        for db_entry in db_collection.find():
            table.entries.append(cls.Entry.from_db(db_entry).values)

        return table

    def to_db(self, db):
        for entry in self.entries:
            db[self.name].insert(self.Entry(entry).to_db())

    @classmethod
    def from_csv_file(cls, csv_file, id_attr=None):
        csv_table = csv.reader(csv_file)
        table = cls(osp.basename(csv_file.name).rstrip('.csv'),
                    csv_table.next(), id_attr)
        table.entries = [entry for entry in csv_table]
        return table

    def to_csv_file(self, csv_file):
        csv_table = csv.writer(csv_file)
        csv_table.writerow(self.attrs)
        for entry in self.entries:
            csv_table.writerow(entry)


def generate_database(csv_files):
    for csv_file in csv_files:
        collection = DataTable.from_csv_file(csv_file)
        collection.to_db()


def generate_csv_files(db_collections):
    for db_collection in db_collections:
        collection = DataTable.from_db(db_collection)
        collection.to_csv_file()


if __name__ == '__main__':
    from pymongo import MongoClient
    client = MongoClient()
    db = client['bear_transit']
    c = db['api_call']

