from . import sdk
from .model import ImageDimensions, ImageHandle
from .enum import Result
import ctypes

class ImageManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = None
        
    def Fetch(self, handle, refresh, callback):
        def CCallback(callback_data, result, handle):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, ImageHandle(internal = handle))
            else:
                callback(result, None)
                
        CCallback = self._internal.fetch.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.fetch(self._internal, handle._internal, refresh, ctypes.c_void_p(), CCallback)
        
    def GetDimensions(self, handle):
        dimensions = sdk.DiscordImageDimensions()
        result = self._internal.get_dimensions(self._internal, handle._internal, dimensions)
        if result != Result.Ok:
            raise Exception(result)
            
        return ImageDimensions(internal = dimensions)
        
    def GetData(self, handle):
        dimensions = self.GetDimensions(handle)
        buffer = (ctypes.c_uint8 * (dimensions.Width * dimensions.Height * 4))()
        
        self._internal.get_data(self._internal, handle._internal, buffer, buffer._length_)
        return bytes(buffer)