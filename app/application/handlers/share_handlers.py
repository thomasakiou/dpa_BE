"""Share handlers."""
from typing import List, Optional
from fastapi import HTTPException, status
from app.domain.repositories.share_repository import IShareRepository
from app.application.commands.share_commands import (
    CreateShareCommand, UpdateShareCommand, DeleteShareCommand
)
from app.application.queries.queries import GetUserSharesQuery, GetAllSharesQuery
from app.domain.entities.share import Share


class ShareHandler:
    """Handler for share commands and queries."""
    
    def __init__(self, share_repository: IShareRepository):
        self.share_repository = share_repository
    
    # Commands
    def handle_create_share(self, command: CreateShareCommand) -> Share:
        """Handle create share command."""
        share = Share(
            user_id=command.user_id,
            shares_count=command.shares_count,
            share_value=command.share_value,
            purchase_date=command.purchase_date
        )
        return self.share_repository.create(share)
    
    def handle_update_share(self, command: UpdateShareCommand) -> Share:
        """Handle update share command."""
        share = self.share_repository.get_by_id(command.share_id)
        if not share:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Share record not found"
            )
            
        if command.shares_count is not None:
            share.shares_count = command.shares_count
        if command.share_value is not None:
            share.share_value = command.share_value
            
        # Recalculate total value
        share.total_value = share.calculate_total_value()
        
        return self.share_repository.update(share)
        
    def handle_delete_share(self, command: DeleteShareCommand) -> bool:
        """Handle delete share command."""
        return self.share_repository.delete(command.share_id)
    
    # Queries
    def handle_get_user_shares(self, query: GetUserSharesQuery) -> List[Share]:
        """Handle get user shares query."""
        return self.share_repository.get_by_user(
            query.user_id, skip=query.skip, limit=query.limit
        )
        
    def handle_get_all_shares(self, query: GetAllSharesQuery) -> List[Share]:
        """Handle get all shares query."""
        return self.share_repository.get_all(skip=query.skip, limit=query.limit)
