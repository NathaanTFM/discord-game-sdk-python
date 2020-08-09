from . import sdk
from .model import User, Relationship
from .enum import Result, RelationshipType, Status
from .event import bindEvents
from typing import Callable
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
        self.OnRelationshipUpdate(Relationship(copy = relationship.contents))
        
    def Filter(self, filter: Callable) -> None:
        """
        Filters a user's relationship list by a boolean condition.
        """
        def CFilter(filter_data, relationship):
            return bool(filter(Relationship(copy = relationship.contents)))
            
        CFilter = self._internal.filter.argtypes[-1](CFilter)
        
        self._internal.filter(self._internal, ctypes.c_void_p(), CFilter)
        
    def Get(self, userId: int) -> Relationship:
        """
        Get the relationship between the current user and a given user by id.
        """
        pointer = sdk.DiscordRelationship()
        result = self._internal.get(self._internal, userId, pointer)
        if result != Result.Ok:
            raise Exception(result)
            
        return Relationship(internal = pointer)
    
    def GetAt(self, index: int) -> Relationship:
        """
        Get the relationship at a given index when iterating over a list of relationships.
        """
        pointer = sdk.DiscordRelationship()
        result = self._internal.get_at(self._internal, index, pointer)
        if result != Result.Ok:
            raise Exception(result)
            
        return Relationship(internal = pointer)
    
    def Count(self) -> int:
        """
        Get the number of relationships that match your filter.
        """
        count = ctypes.c_int32()
        result = self._internal.count(self._internal, count)
        if result != Result.Ok:
            raise Exception(result)
        
        return count.value
            
    def OnRefresh(self) -> None:
        """
        Fires at initialization when Discord has cached a snapshot of the current status of all your relationships.
        """
        pass
    
    def OnRelationshipUpdate(self, relationship: Relationship) -> None:
        """
        Fires when a relationship in the filtered list changes, like an updated presence or user attribute.
        """
        pass