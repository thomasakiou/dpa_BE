"""System settings domain entity."""
from datetime import datetime
from typing import Optional


class SystemSettings:
    """Domain entity for system settings."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        key: str = "",
        value: str = "",
        description: Optional[str] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.key = key
        self.value = value
        self.description = description
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate the system settings."""
        if not self.key:
            raise ValueError("Key cannot be empty")
        if not self.value:
            raise ValueError("Value cannot be empty")
    
    def update(self, value: str, description: Optional[str] = None) -> None:
        """Update setting value and description."""
        if not value:
            raise ValueError("Value cannot be empty")
        
        self.value = value
        if description is not None:
            self.description = description
        self.updated_at = datetime.utcnow()
