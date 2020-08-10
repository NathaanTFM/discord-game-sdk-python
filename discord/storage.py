from . import sdk
from .enum import Result
from .exception import getException
from .model import FileStat
from typing import Callable
import ctypes

class StorageManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = None
        
    def GetPath(self) -> str:
        """
        Returns the filepath to which Discord saves files if you were to use the SDK's storage manager.
        """
        path = sdk.DiscordPath()
        
        result = self._internal.get_path(self._internal, path)
        if result != Result.Ok:
            raise getException(result)
            
        return path.value.decode("utf8")
        
    def Read(self, name: str) -> bytes:
        """
        Reads data synchronously from the game's allocated save file.
        """
        # we need the file stat for this one, as length-fixed buffers does not exist in python
        fileStat = self.Stat(name)
        fileSize = fileStat.Size 
        
        name = ctypes.c_char_p(name.encode("utf8"))
        buffer = (ctypes.c_uint8 * fileSize)()
        read = ctypes.c_uint32()
        
        result = self._internal.read(self._internal, name, buffer, len(buffer), read)
        if result != Result.Ok:
            raise getException(result)
            
        if read.value != fileSize:
            print("discord/storage.py: warning: attempting to read " + str(fileSize) + " bytes, but read " + str(read.value))
            
        return bytes(buffer[:read.value])
            
    def ReadAsync(self, name: str, callback: Callable) -> None:
        """
        Reads data asynchronously from the game's allocated save file.
        
        Returns discord.enum.Result (int) and data (bytes) via callback.
        """
        def CCallback(callback_data, result, data, data_length):
            self._garbage.remove(CCallback)
            if data:
                data = bytes(data[:data_length])
                callback(result, data)
            else:
                callback(result, None)
                
        CCallback = self._internal.read_async.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        name = ctypes.c_char_p(name.encode("utf8"))
        self._internal.read_async(self._internal, name, ctypes.c_void_p(), CCallback)
        
    def ReadAsyncPartial(self, name: str, offset: int, length: int, callback: Callable) -> None:
        """
        Reads data asynchronously from the game's allocated save file, starting at a given offset and up to a given length.
        """
        def CCallback(callback_data, result, data, data_length):
            self._garbage.remove(CCallback)
            if data:
                data = bytes(data[:data_length])
                callback(result, data)
            else:
                callback(result, None)
                
        CCallback = self._internal.read_async.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        name = ctypes.c_char_p(name.encode("utf8"))
        self._internal.read_async_partial(self._internal, name, offset, length, ctypes.c_void_p(), CCallback)
        
    def Write(self, name: str, data: bytes) -> None:
        """
        Writes data synchronously to disk, under the given key name.
        """
        name = ctypes.c_char_p(name.encode("utf8"))
        data = (ctypes.c_uint8 * len(data))(*data)
        
        result = self._internal.write(self._internal, name, data, len(data))
        if result != Result.Ok:
            raise getException(result)
        
    def WriteAsync(self, name: str, data: bytes, callback: Callable) -> None:
        """
        Writes data asynchronously to disk under the given keyname.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.write_async.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        name = ctypes.c_char_p(name.encode("utf8"))
        data = (ctypes.c_uint8 * len(data))(*data)
        
        self._internal.write_async(self._internal, name, data, len(data), ctypes.c_void_p(), CCallback)
        
    def Delete(self, name: str) -> None:
        """
        Deletes written data for the given key name.
        """
        name = ctypes.c_char_p(name.encode("utf8"))
        
        result = self._internal.delete_(self._internal, name)
        if result != Result.Ok:
            raise getException(result)
    
    def Exists(self, name: str) -> bool:
        """
        Checks if data exists for a given key name.
        """
        exists = ctypes.c_bool()
        name = ctypes.c_char_p(name.encode("utf8"))
        
        result = self._internal.exists(self._internal, name, exists)
        if result != Result.Ok:
            raise getException(result)
            
        return exists.value
    
    def Stat(self, name: str) -> FileStat:
        """
        Returns file info for the given key name.
        """
        stat = sdk.DiscordFileStat()
        
        name = ctypes.c_char_p(name.encode("utf8"))
        result = self._internal.stat(self._internal, name, stat)
        if result != Result.Ok:
            raise getException(result)
            
        return FileStat(internal = stat)
    
    def Count(self) -> int:
        """
        Returns the count of files, for iteration.
        """
        count = ctypes.c_int32()
        self._internal.count(self._internal, count)
        return count.value
    
    def StatAt(self, index: int) -> FileStat:
        """
        Returns file info for the given index when iterating over files.
        """
        stat = sdk.DiscordFileStat()
        
        result = self._internal.stat_at(self._internal, index, stat)
        if result != Result.Ok:
            raise getException(result)
        
        return FileStat(internal = stat)