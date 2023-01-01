from itertools import groupby

def flatElementCheck(d) -> dict:
    if type(d) == dict:
       if ('name' not in d.keys()) and ('children' not in d.keys()):
           return True
       else:
           return False
    else:
        return False

def flatListCheck(item: list) -> bool:
    """Function to check if list contains only dicts without
    parent/child structure.

    Args:
        item (list): List to be tested.

    Raises:
        ValueError: Raises value error if argument is not a list.

    Returns:
        bool: Returns True if list is of only dicts wihtout parent/child structure.
    """
    if type(item) == list:
        if all([flatElementCheck(x) for x in item]):
            return True
        else:
            return False
    else:
        raise ValueError("Item is not List as Expected")
      
def listofdicts(item:list) -> bool:
    """Check to make sure all elements of a list are dicts.

    Args:
        item (list): List 

    Raises:
        ValueError: Raises a value error if item is not a list

    Returns:
        bool: True if list contains only dicts.
    """
    if type(item) == list:
        if all([type(x) == dict for x in item]):
            return True
        else:
            return False
    else:    
        raise ValueError("Item is not a List as Expected")   
    
def removeDictElement(adict:dict,key:str) -> dict:
    """_summary_

    Args:
        adict (dict): Dictionary that element is to be remobed from
        key (str): Key for element to be removed.

    Returns:
        dict: Dictionary with element removed.
    """
    newdict = dict(adict)
    del(newdict[key])
    return newdict

def oneLevelListSort(alist:list,keyvalue:str,firstlevel:bool=False) -> dict:
    """Groups a list of dicts by key

    Args:
        alist (list): List of dictionary's 
        keyvalue (str): key property of dictionary to group on.

    Returns:
        dict: {name:key,[{objects}]}
    """
    if flatListCheck(alist):
        groups = []
        alist_sorted = sorted(alist,key = lambda x:x[keyvalue])
        for k,g in groupby(alist_sorted,lambda x:x[keyvalue]):
            groups.append({'name':k, 'children': [removeDictElement(d,keyvalue) for d in g]})
        
        if firstlevel:    
            return {'name':keyvalue, 'children': groups}
        else:
            return groups
    else:
        raise ValueError()
    
def findLowest(d,newparent:str,firstlevel:bool=False) -> dict:
    if type(d) == list:
        if flatListCheck(d):
            #Note that the order of this if chain matters. All items
            #that pass flatListCheck will also pass listofdicts check
            d = oneLevelListSort(d,newparent,firstlevel)
            return d
        elif listofdicts(d):
            for element in d:
                element = findLowest(element,newparent)
        else:
            raise ValueError("Unexpected Elements in List")
    if type(d) == dict:
        if 'children' in d.keys():
            d['children'] = findLowest(d['children'],newparent)
        else:
            raise ValueError("Dict has no child key")
    return d

def stratify(flatlist:list,groupby:list) -> dict:
    d = flatlist
    for i,element in enumerate(groupby):
        if i==0:
            d = findLowest(d,element,True)
        else:
            d = findLowest(d,element,False)
    return d