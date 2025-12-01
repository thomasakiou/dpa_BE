"""Application commands package initialization."""
from app.application.commands.auth_commands import (
    LoginCommand,
    ChangePasswordCommand,
    ResetPasswordCommand
)
from app.application.commands.user_commands import (
    CreateUserCommand,
    UpdateUserCommand,
    SuspendUserCommand,
    ActivateUserCommand,
    DeleteUserCommand
)
from app.application.commands.savings_commands import (
    CreateSavingsCommand,
    RecordSavingsPaymentCommand,
    UpdateSavingsCommand,
    DeleteSavingsCommand
)
from app.application.commands.share_commands import (
    CreateShareCommand,
    UpdateShareCommand,
    DeleteShareCommand
)
from app.application.commands.loan_commands import (
    CreateLoanCommand,
    ApproveLoanCommand,
    DisburseLoanCommand,
    RecordLoanRepaymentCommand,
    CloseLoanCommand,
    RejectLoanCommand,
    UpdateLoanCommand,
    DeleteLoanCommand
)

__all__ = [
    # Auth commands
    "LoginCommand",
    "ChangePasswordCommand",
    "ResetPasswordCommand",
    # User commands
    "CreateUserCommand",
    "UpdateUserCommand",
    "SuspendUserCommand",
    "ActivateUserCommand",
    "DeleteUserCommand",
    # Savings commands
    "CreateSavingsCommand",
    "RecordSavingsPaymentCommand",
    "UpdateSavingsCommand",
    "DeleteSavingsCommand",
    # Share commands
    "CreateShareCommand",
    "UpdateShareCommand",
    "DeleteShareCommand",
    # Loan commands
    "CreateLoanCommand",
    "ApproveLoanCommand",
    "DisburseLoanCommand",
    "RecordLoanRepaymentCommand",
    "CloseLoanCommand",
    "RejectLoanCommand",
    "UpdateLoanCommand",
    "DeleteLoanCommand",
]
