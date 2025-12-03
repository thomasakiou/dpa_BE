# Backend Requirements: Add payment_month Field to Savings

## Overview
Add a new `payment_month` field to the savings payment system to track which month a payment is associated with.

---

## 1. Database Changes

### Update `savings_payments` Table/Model

**File:** `app/infrastructure/database/models.py`

Add the following field to the `SavingsPaymentModel` class:

```python
payment_month = Column(String(20), nullable=True)
```

**Location:** Add after the `payment_date` field (around line 63)

**Field Specifications:**
- **Type:** `VARCHAR(20)` or `ENUM`
- **Allowed Values:** "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
- **Nullable:** `True` (for backward compatibility with existing records)
- **Default:** `None`

### Create Database Migration

Create an Alembic migration to add this field:

```bash
alembic revision -m "add_payment_month_to_savings_payments"
```

**Migration content:**
```python
def upgrade():
    op.add_column('savings_payments', 
        sa.Column('payment_month', sa.String(20), nullable=True)
    )

def downgrade():
    op.drop_column('savings_payments', 'payment_month')
```

---

## 2. Domain Layer Changes

### Update Domain Entity

**File:** `app/domain/entities/savings_payment.py`

1. **Add to `__init__` method** (around line 20):
```python
payment_month: Optional[str] = None,
```

2. **Add as instance variable** (around line 36):
```python
self.payment_month = payment_month
```

3. **Add to `update` method** (around line 52):
```python
payment_month: Optional[str] = None
```

4. **Add update logic in `update` method** (around line 67):
```python
if payment_month is not None:
    self.payment_month = payment_month
```

**Optional:** Add validation for payment_month values:
```python
def _validate_payment_month(self, month: Optional[str]) -> None:
    """Validate payment month."""
    if month is not None:
        valid_months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        if month not in valid_months:
            raise ValueError(f"Invalid payment month: {month}")
```

---

## 3. API Schema Changes

### Update Pydantic Schemas

**File:** `app/presentation/schemas/savings_payment.py`

1. **Add to `SavingsPaymentCreate` schema** (around line 24):
```python
payment_month: Optional[str] = Field(None, description="Month of payment (e.g., 'January', 'February')")
```

2. **Add to `SavingsPaymentUpdate` schema** (around line 33):
```python
payment_month: Optional[str] = Field(None, description="Month of payment (e.g., 'January', 'February')")
```

3. **Add to `SavingsPaymentResponse` schema** (around line 43):
```python
payment_month: Optional[str]
```

---

## 4. Command Layer Changes

### Update Commands

**File:** `app/application/commands/savings_payment_commands.py`

1. **Update `CreateSavingsPaymentCommand.__init__`** (around line 17):
```python
description: Optional[str] = None,
payment_month: Optional[str] = None
```

Add instance variable:
```python
self.payment_month = payment_month
```

2. **Update `UpdateSavingsPaymentCommand.__init__`** (around line 35):
```python
description: Optional[str] = None,
payment_month: Optional[str] = None
```

Add instance variable:
```python
self.payment_month = payment_month
```

---

## 5. Handler Layer Changes

### Update Handlers

**File:** `app/application/handlers/savings_payment_handlers.py`

1. **Update `handle_create_payment` method:**
   - Pass `payment_month` from command to domain entity constructor

2. **Update `handle_update_payment` method:**
   - Pass `payment_month` from command to domain entity's `update` method

---

## 6. Repository Layer Changes

### Update Repository Implementation

**File:** `app/infrastructure/repositories/savings_payment_repository_impl.py`

1. **Update `create` method:**
   - Map `payment_month` from domain entity to database model

2. **Update `update` method:**
   - Map `payment_month` from domain entity to database model

3. **Update `_to_entity` method:**
   - Map `payment_month` from database model to domain entity

---

## 7. API Endpoint Changes

### Update Admin API Routes

**File:** `app/presentation/api/v1/admin.py`

Update the following endpoints to handle `payment_month`:

### POST /api/v1/admin/savings (Create)
**Line:** ~225

Update command creation:
```python
command = CreateSavingsPaymentCommand(
    user_id=request.user_id,
    amount=request.amount,
    type=request.type.value,
    payment_date=request.payment_date,
    description=request.description,
    payment_month=request.payment_month  # ADD THIS LINE
)
```

### PUT /api/v1/admin/savings/{id} (Update)
**Line:** ~246

Update command creation:
```python
command = UpdateSavingsPaymentCommand(
    payment_id=payment_id,
    amount=request.amount,
    type=request.type.value if request.type else None,
    payment_date=request.payment_date,
    description=request.description,
    payment_month=request.payment_month  # ADD THIS LINE
)
```

### GET /api/v1/admin/savings (List)
**Line:** ~202

No changes needed - the response schema will automatically include `payment_month` once the schema is updated.

---

## 8. Testing Checklist

After implementing the changes, test the following:

- [ ] Database migration runs successfully
- [ ] Create savings payment with `payment_month` field
- [ ] Create savings payment without `payment_month` field (should work for backward compatibility)
- [ ] Update savings payment to add `payment_month`
- [ ] Update savings payment to change `payment_month`
- [ ] List all savings payments and verify `payment_month` is included in response
- [ ] Verify existing records have `payment_month` as `null`

---

## 9. Example API Requests

### Create with payment_month:
```json
POST /api/v1/admin/savings
{
  "user_id": 1,
  "amount": 5000.00,
  "type": "Monthly Savings",
  "payment_date": "2025-12-02T15:00:00Z",
  "description": "December monthly savings",
  "payment_month": "December"
}
```

### Update payment_month:
```json
PUT /api/v1/admin/savings/123
{
  "payment_month": "January"
}
```

### Expected Response:
```json
{
  "id": 123,
  "user_id": 1,
  "amount": 5000.00,
  "type": "Monthly Savings",
  "payment_date": "2025-12-02T15:00:00Z",
  "description": "December monthly savings",
  "payment_month": "December",
  "created_at": "2025-12-02T14:00:00Z"
}
```

---

## Summary of Files to Modify

1. ✅ `app/infrastructure/database/models.py` - Add column to SavingsPaymentModel
2. ✅ `alembic/versions/` - Create new migration file
3. ✅ `app/domain/entities/savings_payment.py` - Add field to domain entity
4. ✅ `app/presentation/schemas/savings_payment.py` - Add field to all schemas
5. ✅ `app/application/commands/savings_payment_commands.py` - Add field to commands
6. ✅ `app/application/handlers/savings_payment_handlers.py` - Handle new field
7. ✅ `app/infrastructure/repositories/savings_payment_repository_impl.py` - Map new field
8. ✅ `app/presentation/api/v1/admin.py` - Pass field in API endpoints

---

## Notes

- The field is **nullable** to maintain backward compatibility with existing records
- No changes needed to GET endpoint - it will automatically return the new field
- Consider adding validation to ensure only valid month names are accepted
- The field should accept exact month names as specified (capitalized, full names)
