"""System settings repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.system_settings import SystemSettings


class ISystemSettingsRepository(ABC):
    """Interface for system settings repository."""
    
    @abstractmethod
    def get_by_key(self, key: str) -> Optional[SystemSettings]:
        """Get setting by key."""
        pass
    
    @abstractmethod
    def upsert(self, setting: SystemSettings) -> SystemSettings:
        """Create or update a setting."""
        pass
    
    @abstractmethod
    def get_all(self) -> list[SystemSettings]:
        """Get all settings."""
        pass
