from .enum import Result

class DiscordException(Exception):
    pass

exceptions = {}
    
# we dynamically create the exceptions
for name in dir(Result):
    value = getattr(Result, name)
    if not name.startswith("_") and name != "Ok":
        exception = type(name, (DiscordException,), {})
        
        globals()[name] = exception
        exceptions[value] = exception
        
def getException(result):
    return exceptions.get(result, DiscordException)("result " + str(result))