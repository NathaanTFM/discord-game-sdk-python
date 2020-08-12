from . import sdk
from .model import ImageDimensions, ImageHandle
from .enum import Result
from .exception import getException
from typing import Callable, Optional
import ctypes

class ImageManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = None
        
    def Fetch(self, handle: ImageHandle, refresh: bool, callback: Callable[[Result, Optional[ImageHandle]], None]) -> None:
        """
        Prepares an image to later retrieve data about it.
        
        Returns discord.enum.Result (int) and ImageHandle via callback.
        """
        def CCallback(callback_data, result, handle):
            self._garbage.remove(CCallback)
            result = Result(result)
            if result == Result.Ok:
                callback(result, ImageHandle(internal = handle))
            else:
                callback(result, None)
                
        CCallback = self._internal.fetch.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.fetch(self._internal, handle._internal, refresh, ctypes.c_void_p(), CCallback)
        
    def GetDimensions(self, handle: ImageHandle) -> ImageDimensions:
        """
        Gets the dimension for the given user's avatar's source image
        """
        dimensions = sdk.DiscordImageDimensions()
        result = Result(self._internal.get_dimensions(self._internal, handle._internal, dimensions))
        if result != Result.Ok:
            raise getException(result)
            
        return ImageDimensions(internal = dimensions)
        
    def GetData(self, handle: ImageHandle) -> bytes:
        """
        Gets the image data for a given user's avatar.
        """
        dimensions = self.GetDimensions(handle)
        buffer = (ctypes.c_uint8 * (dimensions.Width * dimensions.Height * 4))()
        
        result = Result(self._internal.get_data(self._internal, handle._internal, buffer, len(buffer)))
        if result != Result.Ok:
            raise getException(result)
            
        return bytes(buffer)
        