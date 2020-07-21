import ctypes
    
def bindEvents(structure, *methods):
    contents = structure()
    for index, (name, func) in enumerate(structure._fields_):
        setattr(contents, name, func(methods[index]))
        
    pointer = ctypes.pointer(contents)
    return pointer