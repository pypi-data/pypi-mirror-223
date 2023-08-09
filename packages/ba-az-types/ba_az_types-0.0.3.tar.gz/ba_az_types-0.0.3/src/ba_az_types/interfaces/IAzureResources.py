from abc import ABCMeta, abstractmethod

from .IResourceGroup import IResourceGroup
from .IWebApp import IWebApp
from .IContainerRegistry import IContainerRegistry
from .IAppRegistration import IAppRegistration
from .IDatabase import IDatabase
from .IRedisCache import IRedisCache
from .IStorageAccount import IStorageAccount
from .IKeyVault import IKeyVault
from .ICategorizableResource import ICategorizableResource

class IAzureResources:
    __metaclass__ = ABCMeta

    RESOURCE_GROUPS_KEY = 'resourceGroups'
    """Key for the resource groups section of an Azure Resources definition"""
    WEB_APPS_KEY = 'webApps'
    """Key for the web apps section of an Azure Resources definition"""
    CONTAINER_REGISTRIES_KEY = 'containerRegistries'
    """Key for the container registries section of an Azure Resources definition"""
    APP_REGISTRATIONS_KEY = 'appRegistrations'
    """Key for the app registrations section of an Azure Resources definition"""
    DATABASES_KEY = 'databases'
    """Key for the databases section of an Azure Resources definition"""
    CACHES_KEY = 'caches'
    """Key for the caches section of an Azure Resources definition"""
    STORAGE_KEY = 'storage'
    """Key for the storage section of an Azure Resources definition"""
    VAULTS_KEY = 'vaults'
    """Key for the vaults section of an Azure Resources definition"""
    CATEGORIZED_RESOURCES_KEY = 'categorizedResources'
    """Key for the categorized resources section of an Azure Resources definition"""

    @property
    @abstractmethod
    def resource_groups(self) -> list[IResourceGroup]:
        pass
    @abstractmethod
    def has_resource_group(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_resource_group(self, name: str) -> IResourceGroup | None:
        pass
    
    @property
    @abstractmethod
    def web_apps(self) -> list[IWebApp]:
        pass
    @abstractmethod
    def has_web_app(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_web_app(self, name: str) -> IWebApp | None:
        pass
    
    @property
    @abstractmethod
    def container_registries(self) -> list[IContainerRegistry]:
        pass
    @abstractmethod
    def has_container_registry(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_container_registry(self, name: str) -> IContainerRegistry | None:
        pass
    
    @property
    @abstractmethod
    def app_registrations(self) -> list[IAppRegistration]:
        pass
    @abstractmethod    
    def has_app_registration(self, name: str) -> bool:
       pass
    @abstractmethod
    def get_app_registration(self, name: str) -> IAppRegistration | None:
        pass
    
    @property
    @abstractmethod
    def databases(self) -> list[IDatabase]:
        pass
    @abstractmethod
    def has_database(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_database(self, name: str) -> IDatabase | None:
        pass

    @property
    @abstractmethod
    def caches(self) -> list[IRedisCache]:
        pass
    @abstractmethod
    def has_cache(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_cache(self, name: str) -> IRedisCache | None:
        pass

    @property
    @abstractmethod
    def uncategorized_storage(self) -> list[IStorageAccount]:
        pass
    @abstractmethod
    def has_uncategorized_storage(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_uncategorized_storage(self, name: str) -> IStorageAccount | None:
        pass

    @property
    @abstractmethod
    def uncategorized_vaults(self) -> list[IKeyVault]:
        pass
    @abstractmethod
    def has_uncategorized_vault(self, name: str) -> bool:
        pass
    @abstractmethod
    def get_uncategorized_vault(self, name: str) -> IKeyVault | None:
        pass

    
    @property
    @abstractmethod
    def categorized_resources(self) -> dict[str, dict[str, ICategorizableResource]]:
        pass
    @abstractmethod
    def get_resource_categories(self) -> list[str]:
        pass
    @abstractmethod
    def has_resource_category(self, category: str) -> bool:
        pass
    @abstractmethod    
    def get_category_resources(self, category: str) -> list[ICategorizableResource] | None:
        pass
    
    @classmethod
    @abstractmethod
    def from_file(cls, file_path: str):
        pass