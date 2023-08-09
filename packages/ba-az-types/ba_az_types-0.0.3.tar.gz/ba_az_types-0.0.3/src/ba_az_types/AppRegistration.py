from typing import Any

from .interfaces.IAppRegistration import IAppRegistration

class AppRegistration(IAppRegistration):
    def __init__(self, definition_json: dict[str, Any]):
        self.__definition_json = definition_json

        self.__name = definition_json[self.NAME_KEY]
        
        self._app_id = None
        self._app_secret = None
        self._service_principal_id = None
    
    @property
    def name(self) -> str:
        """The name of the app registration"""
        
        return self.__name
    
    @property
    def app_id(self) -> str:
        """The app id of the app registration"""
        
        return self._app_id # type: ignore
    
    @app_id.setter
    def app_id(self, value: str):
        self._app_id = value
    
    @property
    def app_secret(self) -> str:
        """The app secret of associated with the app registration"""
        
        return self._app_secret # type: ignore
    
    @app_secret.setter
    def app_secret(self, value: str):
        self._app_secret = value
    
    @property
    def service_principal_id(self) -> str:
        """The id of the service principal associated with the app registration"""
        
        return self._service_principal_id # type: ignore
    
    @service_principal_id.setter
    def service_principal_id(self, value: str):
        self._service_principal_id = value
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name,
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "service_principal_id": self.service_principal_id
        }