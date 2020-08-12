from . import sdk
from .enum import Result
from .model import Sku, Entitlement
from .event import bindEvents
from .exception import getException
from typing import Callable
import ctypes

class StoreManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordStoreEvents,
            self._OnEntitlementCreate,
            self._OnEntitlementDelete
        )
        
    def _OnEntitlementCreate(self, event_data, entitlement):
        self.OnEntitlementCreate(Entitlement(copy = entitlement))
        
    def _OnEntitlementDelete(self, event_data, entitlement):
        self.OnEntitlementDelete(Entitlement(copy = entitlement))
    
    def FetchSkus(self, callback: Callable[[Result], None]) -> None:
        """
        Fetches the list of SKUs for the connected application, readying them for iteration.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.fetch_skus.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.fetch_skus(self._internal, ctypes.c_void_p(), CCallback)
        
    def CountSkus(self) -> int:
        """
        Get the number of SKUs readied by FetchSkus().
        """
        count = ctypes.c_int32()
        self._internal.count_skus(self._internal, count)
        return count.value
        
    def GetSku(self, skuId: int) -> Sku:
        """
        Gets a SKU by its ID.
        """
        sku = sdk.DiscordSku()
        
        result = self._internal.get_sku(skuId, sku)
        if result != Result.Ok:
            raise getException(result)
            
        return Sku(internal = sku)
        
    def GetSkuAt(self, index: int) -> Sku:
        """
        Gets a SKU by index when iterating over SKUs.
        """
        sku = sdk.DiscordSku()
        
        result = self._internal.get_sku_at(index, sku)
        if result != Result.Ok:
            raise getException(result)
            
        return Sku(internal = sku)
        
    def FetchEntitlements(self, callback: Callable[[Result], None]) -> None:
        """
        Fetches a list of entitlements to which the user is entitled.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.fetch_entitlements.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.fetch_entitlements(self._internal, ctypes.c_void_p(), CCallback)
        
    def CountEntitlements(self) -> int:
        """
        Get the number of entitlements readied by FetchEntitlements(). 
        """
        count = ctypes.c_int32()
        self._internal.count_entitlements(self._internal, count)
        return count.value
        
    def GetEntitlement(self, entitlementId: int) -> Entitlement:
        """
        Gets an entitlement by its id.
        """
        entitlement = sdk.DiscordEntitlement()
        
        result = self._internal.get_entitlement(entitlementId, entitlement)
        if result != Result.Ok:
            raise getException(result)
            
        return Entitlement(internal = sku)
        
    def GetEntitlementAt(self, index: int) -> Entitlement:
        """
        Gets an entitlement by index when iterating over a user's entitlements.
        """
        entitlement = sdk.DiscordEntitlement()
        
        result = self._internal.get_entitlement_at(index, entitlement)
        if result != Result.Ok:
            raise getException(result)
            
        return Entitlement(internal = sku)
        
    def HasSkuEntitlement(self, skuId: int) -> bool:
        """
        Returns whether or not the user is entitled to the given SKU ID.
        """
        has_entitlement = ctypes.c_bool()
        
        result = self._internal.has_sku_entitlement(skuId, has_entitlement)
        if result != Result.Ok:
            raise getException(result)
            
        return has_entitlement.value
        
    def StartPurchase(self, skuId: int, callback: Callable[[Result], None]) -> None:
        """
        Opens the overlay to begin the in-app purchase dialogue for the given SKU ID.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.start_purchase.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.start_purchase(self._internal, skuId, ctypes.c_void_p(), CCallback)
        
    def OnEntitlementCreate(self, entitlement: Entitlement) -> None:
        """
        Fires when the connected user receives a new entitlement, either through purchase or through a developer grant.
        """
        pass
        
    def OnEntitlementDelete(self, entitlement: Entitlement) -> None:
        """
        Fires when the connected user loses an entitlement, either by expiration, revocation, or consumption in the case of consumable entitlements.
        """
        pass
        