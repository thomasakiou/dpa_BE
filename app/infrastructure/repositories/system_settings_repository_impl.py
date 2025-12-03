"""System settings repository implementation."""
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.system_settings_repository import ISystemSettingsRepository
from app.domain.entities.system_settings import SystemSettings
from app.infrastructure.database.models import SystemSettingsModel


class SystemSettingsRepository(ISystemSettingsRepository):
    """SQLAlchemy implementation of system settings repository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_key(self, key: str) -> Optional[SystemSettings]:
        """Get setting by key."""
        db_setting = self.db.query(SystemSettingsModel).filter(
            SystemSettingsModel.key == key
        ).first()
        
        return self._to_entity(db_setting) if db_setting else None
    
    def upsert(self, setting: SystemSettings) -> SystemSettings:
        """Create or update a setting."""
        db_setting = self.db.query(SystemSettingsModel).filter(
            SystemSettingsModel.key == setting.key
        ).first()
        
        if db_setting:
            # Update existing
            db_setting.value = setting.value
            db_setting.description = setting.description
        else:
            # Create new
            db_setting = SystemSettingsModel(
                key=setting.key,
                value=setting.value,
                description=setting.description
            )
            self.db.add(db_setting)
        
        self.db.commit()
        self.db.refresh(db_setting)
        
        return self._to_entity(db_setting)
    
    def get_all(self) -> list[SystemSettings]:
        """Get all settings."""
        db_settings = self.db.query(SystemSettingsModel).all()
        return [self._to_entity(s) for s in db_settings]
    
    def _to_entity(self, model: SystemSettingsModel) -> SystemSettings:
        """Convert database model to domain entity."""
        return SystemSettings(
            id=model.id,
            key=model.key,
            value=model.value,
            description=model.description,
            updated_at=model.updated_at
        )
