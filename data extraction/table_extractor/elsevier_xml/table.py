from bson.objectid import ObjectId
from copy import deepcopy
import pandas as pd
import numpy as np


class Document(dict):

    structure = dict()

    def __init__(self, initializer=None):
        for key, (struct, value) in self.structure.items():
            dict.__setitem__(self, key, deepcopy(value))

        if initializer is not None:
            for key, value in initializer.items():
                self.__setitem__(self, key, deepcopy(value))

    def __setitem__(self, key, value):
        if key not in self.structure:
            raise KeyError("Invalid key used: '" + key + "'.")

        expected = self.structure[key][0]

        if value is not None:
            if type(expected) == list:
                if type(value) != list:
                    raise TypeError("Invalid type used: Expected '[" + 
                    self.structure[key][0][0].__name__ + "]' but key '" + key + "' is not array.")
                if not all(isinstance(x, expected[0]) for x in value):
                    raise TypeError("Invalid type used: Expected '[" + 
                    self.structure[key][0][0].__name__ + "]' but got '" + type(value).__name__ 
                    + "' for item in key '" + key + "'.")
            elif not isinstance(value, expected):
                raise TypeError("Invalid type used: Expected '" + 
                self.structure[key][0].__name__ + "' but got '" + 
                type(value).__name__ + "' for key '" + key + "'.")

        return dict.__setitem__(self, key, value)

   
class Link(Document):
    structure = dict({
        'name':(str, None),
        'link_ref':(list, [])
    })

class Attribute(Document):
    structure = dict({
        'name':(str, None), 
        'value':(float, 0),
        'links': ([Link], []),
        'string_value' : (str, None),
        'unit': (str, None),
        'value_ref':(list, []),
        'attr_ref':(list, [])
    })

# top level of graph structure
class Entity(Document):
    structure = dict({
        'name':(str, None),
        'attributes':([Attribute], []),
        'links':([Link], []),
        'descriptor':(str, None),
        'ent_ref':(list, [])
    })

class Table(Document):
    structure = dict({
        '_id': (ObjectId, None),
        'paper_doi':(str, None),
        'order':(int, 0),
        'act_table':(list, None), 
        'entities':([Entity], []), 
        'caption':(str, None),
        'caption_ref':(list, []),
        'composition_table':(bool, False), 
        'footer':(dict, None)
    })








