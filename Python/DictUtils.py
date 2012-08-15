"""
    Name:
        DictUtils.py

    Description:
        Dictionary Utils -- provides utilities for dictionaries

"""

def missingKey(d1, d2):
    '''Returns a list of name value pairs for all the elements that are present in one dictionary and not the other'''
    l = []
    l += [ {k:d1[k]} for k in d1 if k not in d2 ]
    l += [ {k:d2[k]} for k in d2 if k not in d1 ]
    return l

def dictCompare(d1, d2):
    '''Returns a list of name value pairs for all the elements that are different between the two dictionaries'''
    diffs = missingKey(d1, d2)
    diffs += [ {k:str(d1[k]) + '->' + str(d2[k])} for k in d1 if k in d2 and d1[k] != d2[k]]
    return diffs

def userInputStrip(uDict):
    """Strip whitespace out of input provided by the user"""
    dictList = map(lambda x: (x[1] and type(x[1]) == type('')) and (x[0], x[1].strip()) or (x[0], x[1]), uDict.items())
    return dict(dictList)

def setNestedValue(d, keyString, value):
    """Sets the value in a nested dictionary where '.' is the delimiter"""
    keys = keyString.split('.')
    currentValue = d
    for key in keys:
        previousValue = currentValue
        currentValue = currentValue.setdefault(key, {})
    previousValue[key] = value

def getNestedValue(dictionary, keyString, default=None):
    """Returns the value from a nested dictionary where '.' is the delimiter"""
    keys = keyString.split('.')
    currentValue = dictionary
    for key in keys:
        if not isinstance(currentValue, dict):
            return default
        currentValue = currentValue.get(key, None)
        if currentValue == None:
            return default

    return currentValue

def stringKeys(dictionary):
    for key, value in dictionary.items():
        if type(key) != str:
            dictionary.pop(key)
            dictionary[str(key)] = value

    return dictionary

def iterateOver(dictionary, key):
    results = dictionary.get(key, [])
    if type(results) != list:
        results = [results]

    return enumerate(results)

def twoWayDict(dictionary):
    for key, value in dictionary.items():
        dictionary[value] = key

    return dictionary

class OrderedDict(dict):

    class ItemIterator(dict):

        def __init__(self, orderedDict, includeIndex=False):
            self.orderedDict = orderedDict
            self.length = len(orderedDict)
            self.index = 0
            self.includeIndex = includeIndex

        def next(self):
            if self.index < self.length:
                key = self.orderedDict.orderedKeys[self.index]
                value = self.orderedDict[key]
                to_return = (self.includeIndex and (self.index, key, value)) or (key, value)
                self.index += 1
                return to_return
            else:
                raise StopIteration

        def __iter__(self):
            return self

    def __init__(self, tuplePairs=()):
        self.orderedKeys = []

        for key, value in tuplePairs:
            self[key] = value

    def __add__(self, value):
        if isinstance(value, OrderedDict):
            newDict = self.copy()
            newDict.update(value)
            return newDict

        return dict.__add__(self, value)

    def copy(self):
        newDict = OrderedDict()
        newDict.update(self)
        return newDict

    def update(self, dictionary):
        for key, value in dictionary.iteritems():
            self[key] = value

    def items(self):
        items = []
        for key in self.orderedKeys:
            items.append((key, self[key]))

        return items

    def values(self):
        values = []
        for key in self.orderedKeys:
            values.append(self[key])

        return values

    def keys(self):
        return self.orderedKeys

    def iterkeys(self):
        return self.orderedKeys.__iter__()

    def __iter__(self):
        return self.iterkeys()

    def iteritems(self):
        return self.ItemIterator(self)

    def iteritemsWithIndex(self):
        return self.ItemIterator(self, includeIndex=True)

    def __setitem__(self, keyString, value):
        if not keyString in self.orderedKeys:
            self.orderedKeys.append(keyString)
        return dict.__setitem__(self, keyString, value)

    def setdefault(self, keyString, value):
        if not keyString in self.orderedKeys:
            self.orderedKeys.append(keyString)
        return dict.setdefault(self, keyString, value)


def getAllNestedKeys(dictionary, prefix=""):
    keys = []
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            keys.extend(getAllNestedKeys(value, prefix=prefix + key + '.'))
            continue

        keys.append(prefix + key)

    return keys



class NestedDict(dict):
    def __init__(self, d=None):
        if d:
            self.update(d)

    def setValue(self, keyString, value):
        setNestedValue(self, keyString, value)

    def allKeys(self):
        return getAllNestedKeys(self)

    def difference(self, otherDict):
        """ returns a list of tuples [(key, myValue, otherDictValue),]
            allowing you to do:
                for fieldName, oldValue, newValue in oldValues.difference(newValues)
        """
        differences = []
        for key in set(self.allKeys() + otherDict.allKeys()):
            myValue = self.getValue(key, default=None)
            otherDictValue = otherDict.getValue(key, default=None)
            if myValue != otherDictValue:
                differences.append((key, myValue, otherDictValue))

        return differences


    def getValue(self, keyString, **kwargs):
        keys = keyString.split('.')
        currentNode = self
        for key in keys:
            if not key:
                continue
            currentNode = currentNode.get(key, None)
            if not currentNode:
                break

        if currentNode:
            return currentNode
        elif kwargs.has_key('default'):
            return kwargs.get('default')
        else:
            raise KeyError(keyString)


def createDictFromString(string, itemSeparator, keyValueSeparator, ordered=False):
    if ordered:
        newDict = OrderedDict()
    else:
        newDict = {}
    if not string:
        return newDict
    for item in string.split(itemSeparator):
        key, value = item.split(keyValueSeparator)
        oldValue = newDict.get(key, None)
        if oldValue is not None:
            if type(oldValue) == list:
                newDict[key].append(value)
            else:
                newDict[key] = [oldValue, value]
        else:
            newDict[key] = value

    return newDict
