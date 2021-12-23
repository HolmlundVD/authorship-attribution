#
#you can use this on any indexable data structure. This will add the element at the end of the specified path if the element exists it will edit using the supplied function
#
def add_or_edit(structure,path:tuple,*,to_add,edit_function):
    item=structure
    for i in len(path)-1:
        item=item[path[i]]
    if(item[path(len(path-1))]):
        item[path(len(path)-1)]=edit_function(item[path(len(path)-1)])
    else:
        item[path(len(path)-1)]=to_add

#
##you can use this on any indexable data structure. This will retun the item at the end of the path
#
def retrieve_in_structure(structure,edit_function,path:tuple):
    item=structure
    for i in len(path)-1:
        item=item[path[i]]
    return item[path(len(path)-1)]