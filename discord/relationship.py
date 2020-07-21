from . import sdk
from .model import User, Relationship
from .enum import Result
from .event import bindEvents
import ctypes

class RelationshipManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordRelationshipEvents,
            self._OnRefresh,
            self._OnRelationshipUpdate
        )
        
    def _OnRefresh(self, event_data):
        self.OnRefresh()
        
    def _OnRelationshipUpdate(self, event_data, relationship):
        self.OnRelationshipUpdate(Relationship(internal = relationship.contents))
        
    def Filter(self, filter):
        def CFilter(filter_data, relationship):
            return bool(filter(Relationship(internal = relationship.contents)))
            
        CFilter = self._internal.filter.argtypes[-1](CFilter)
        self._garbage.append(CFilter) # prevent it from being garbage collected
        # TODO: eventually remove it
        
        self._internal.filter(self._internal, ctypes.c_void_p(), CFilter)
        
    def Get(self, userId):
        pointer = sdk.DiscordRelationship()
        result = self._internal.get(self._internal, userId, pointer)
        if result != Result.Ok:
            raise Exception(result)
            
        return Relationship(internal = pointer)
    
    def GetAt(self, index):
        pointer = sdk.DiscordRelationship()
        result = self._internal.get_at(self._internal, index, pointer)
        if result != Result.Ok:
            raise Exception(result)
            
        return Relationship(internal = pointer)
    
    def Count(self):
        count = ctypes.c_uint32()
        result = self._internal.count(self._internal, count)
        if result != Result.Ok:
            raise Exception(result)
        
        return count.value
            
    def OnRefresh(self):
        pass
    
    def OnRelationshipUpdate(self, relationship):
        pass