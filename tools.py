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
    if type(item) == list:
        if all([flatElementCheck(x) for x in item]):
            return True
        else:
            return False
    else:
        raise ValueError("Item is not List as Expected")
    
def listofChildrenCheck(item) -> bool:
    if type(item) == list:
        for element in item:
            if type(element) == dict:
                if ('name' not in element.keys()):
                    return False
                if ('children' not in element.keys()):
                    return False
                if type(element['children']) != list:
                    return False
            else:
                return True
    else:
        raise ValueError("Item is not List as Expected")
    
def listofdicts(item) -> bool:
    if type(item) == list:
        if all([type(x) == dict for x in item]):
            return True
        else:
            return False
    else:    
        raise ValueError("Item is not a List as Expected")   
    
def removeDictElement(adict:dict,key:str) -> dict:
    newdict = dict(adict)
    del(newdict[key])
    return newdict

def firstLevelListSort(alist:list,keyvalue:str) -> dict:
    if flatListCheck(alist):
        groups = []
        alist_sorted = sorted(alist,key = lambda x:x[keyvalue])
        for k,g in groupby(alist_sorted,lambda x:x[keyvalue]):
            groups.append({'name':k, 'children': [removeDictElement(d,keyvalue) for d in g]})      
        return groups
    else:
        raise ValueError("Expected List")

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