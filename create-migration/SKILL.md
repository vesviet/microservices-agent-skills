---
name: create-migration
description: Create new database migrations for a microservice using Goose format with proper annotations and naming
---

# Create Migration Skill

Use this skill when the user needs to create a new database migration for any microservice.

## When to Use
- Adding new tables or columns
- Modifying existing schema
- Adding indexes or constraints
- Data migrations
- Any database schema change

## Migration Tool: Goose

This project uses **Goose** for SQL migrations. All migration files are plain SQL with special Goose annotations.

## Migration File Location

```
<service>/migrations/<filename>.sql
```

## Naming Convention

**Format**: `<sequence_number>_<description>.sql`

Examples:
- `001_init_auth_schema.sql`
- `002_add_user_preferences.sql`
- `003_create_token_revocations_table.sql`
- `20251103191700_init_auth_schema.sql` (timestamp-based, also accepted)

**Rules:**
- Use lowercase with underscores
- Be descriptive about what the migration does
- Check existing migrations to determine the next sequence number

## Required Annotations

Every migration file MUST have Goose annotations. **Without these, migrations will NOT run.**

```sql
-- +goose Up
-- SQL in this section is executed when the migration is applied.

CREATE TABLE example (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- +goose Down
-- SQL in this section is executed when the migration is rolled back.

DROP TABLE IF EXISTS example;
```

## Step-by-Step Process

### Step 1: Check Existing Migrations
```bash
ls -la /home/user/microservices/<service>/migrations/
```
Determine the next sequence number and understand the existing schema.

### Step 2: Read the Last Migration
Review the most recent migration to understand current schema state and naming patterns.

### Step 3: Create the Migration File
Create a new file in `<service>/migrations/` following the naming convention.

### Step 4: Write the SQL

**Standard patterns used in this project:**

#### UUID Primary Keys (preferred)
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

#### Timestamps
```sql
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
deleted_at TIMESTAMP WITH TIME ZONE  -- soft delete (nullable)
```

#### Foreign Keys
```sql
customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE
```

#### Indexes
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

#### Enums (using VARCHAR with CHECK)
```sql
status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'inactive', 'deleted'))
```

#### JSONB for flexible data
```sql
metadata JSONB DEFAULT '{}'::jsonb
```

#### Composite indexes
```sql
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
```

### Step 5: Verify the Down Migration
The `-- +goose Down` section must cleanly reverse everything in `-- +goose Up`:
- `CREATE TABLE` → `DROP TABLE IF EXISTS`
- `ALTER TABLE ADD COLUMN` → `ALTER TABLE DROP COLUMN IF EXISTS`
- `CREATE INDEX` → `DROP INDEX IF EXISTS`

### Step 6: Update GORM Models (if applicable)
After creating the migration, update the corresponding GORM model in:
```
<service>/internal/data/model/<entity>.go
```
or
```
<service>/internal/data/<entity>.go
```

### Step 7: Update Repository Interface (if applicable)
If new fields require new queries, update:
```
<service>/internal/biz/<entity>.go   → Repository interface
<service>/internal/data/<entity>.go  → Repository implementation
```

## Template: New Table Migration

```sql
-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS <table_name> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Business fields
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit fields
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_<table_name>_status ON <table_name>(status);
CREATE INDEX IF NOT EXISTS idx_<table_name>_created_at ON <table_name>(created_at);
CREATE INDEX IF NOT EXISTS idx_<table_name>_deleted_at ON <table_name>(deleted_at) WHERE deleted_at IS NOT NULL;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS <table_name>;
-- +goose StatementEnd
```

## Template: Add Column Migration

```sql
-- +goose Up
ALTER TABLE <table_name> ADD COLUMN IF NOT EXISTS <column_name> <type> <constraints>;
CREATE INDEX IF NOT EXISTS idx_<table_name>_<column_name> ON <table_name>(<column_name>);

-- +goose Down
DROP INDEX IF EXISTS idx_<table_name>_<column_name>;
ALTER TABLE <table_name> DROP COLUMN IF EXISTS <column_name>;
```

## Common Gotchas

1. **ALWAYS include `-- +goose Up` and `-- +goose Down`** - Migration will fail without these
2. **Use `IF NOT EXISTS` / `IF EXISTS`** for idempotency
3. **Use `-- +goose StatementBegin` / `-- +goose StatementEnd`** for multi-statement blocks or functions/triggers
4. **UUID is the standard PK type** in this project, NOT auto-incrementing integers
5. **Use `TIMESTAMP WITH TIME ZONE`** not just `TIMESTAMP`
6. **Soft delete pattern**: Use `deleted_at TIMESTAMP WITH TIME ZONE` (nullable)
7. **Always add indexes** for foreign keys and frequently queried columns
8. **Test the down migration** to ensure clean rollback

## Versioning Impact

Ref: [Coding Standards §3](docs/07-development/standards/coding-standards.md)

| Migration Type | Version Bump | Rationale |
|---------------|-------------|-----------|
| New table | **MINOR** | New feature, backward compatible |
| Add column (nullable/default) | **MINOR** | Backward compatible |
| Add column (NOT NULL, no default) | **MAJOR** | May break existing data/queries |
| Remove/rename column | **MAJOR** | Breaking change for existing code |
| Add index | **PATCH** | Performance improvement, no behavior change |
| Data migration only | **PATCH** | Bug fix or data cleanup |

**Always update `CHANGELOG.md`** when adding migrations:
```markdown
## [Unreleased]
### Added
- New migration: add `preferences` column to `users` table
```

## Checklist

- [ ] Checked existing migrations (`ls migrations/`) for sequence number
- [ ] `-- +goose Up` and `-- +goose Down` annotations present
- [ ] `IF NOT EXISTS` / `IF EXISTS` for idempotency
- [ ] UUID primary keys (not auto-increment)
- [ ] `TIMESTAMP WITH TIME ZONE` (not plain `TIMESTAMP`)
- [ ] Indexes added for foreign keys and query columns
- [ ] Down migration cleanly reverses Up migration
- [ ] GORM model updated to match new schema
- [ ] Repository interface updated if new fields need queries
- [ ] Build passes (`go build ./...`)
- [ ] **CHANGELOG.md updated** with migration description
- [ ] **Version impact assessed** (add column = MINOR, remove column = MAJOR)
