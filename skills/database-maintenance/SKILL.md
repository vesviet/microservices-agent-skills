---
name: database-maintenance
description: Database backup, restore, point-in-time recovery, and maintenance operations for PostgreSQL databases
---

# Database Maintenance Skill

Use this skill for PostgreSQL database operations across the microservices platform.

## When to Use
- Performing database backups (scheduled or ad-hoc)
- Restoring from backup
- Point-in-time recovery after data loss
- Running database maintenance (VACUUM, REINDEX, ANALYZE)
- Migrating data between environments
- Troubleshooting database performance

## Database Architecture

Each microservice has its own PostgreSQL database (database-per-service pattern):

| Service | Database Name | Key Tables |
|---------|--------------|------------|
| Auth | `auth_db` | users, tokens, roles |
| User | `user_db` | users, addresses |
| Order | `order_db` | orders, order_items, outbox_events |
| Payment | `payment_db` | payments, payment_methods, transactions |
| Catalog | `catalog_db` | products, categories, brands, attributes |
| Warehouse | `warehouse_db` | inventory, stock_movements, reservations |
| Checkout | `checkout_db` | carts, cart_items |
| Customer | `customer_db` | customers, customer_addresses |
| Fulfillment | `fulfillment_db` | fulfillments, picklists, packages |
| Shipping | `shipping_db` | shipments, tracking_events |
| Promotion | `promotion_db` | promotions, coupons, usage |
| Pricing | `pricing_db` | prices, price_tiers |
| Return | `return_db` | returns, return_items |
| Loyalty | `loyalty_db` | accounts, transactions, rewards |
| Review | `review_db` | reviews, ratings |
| Notification | `notification_db` | notifications, templates |
| Analytics | `analytics_db` | events, metrics |

## Backup Operations

### Full Database Backup

```bash
# Single service backup
SERVICE="order"
DB_NAME="${SERVICE}_db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

pg_dump -h localhost -U ${SERVICE}_user -d $DB_NAME \
  --format=custom \
  --compress=6 \
  --file=$BACKUP_FILE

echo "Backup created: $BACKUP_FILE ($(du -h $BACKUP_FILE | cut -f1))"
```

### All Services Backup Script

```bash
#!/bin/bash
# backup_all.sh — Backs up all service databases
BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

SERVICES=(auth user order payment catalog warehouse checkout customer fulfillment shipping promotion pricing return loyalty-rewards review notification analytics)

for SERVICE in "${SERVICES[@]}"; do
    DB_NAME="${SERVICE//-/_}_db"
    DB_USER="${SERVICE//-/_}_user"
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_$(date +%H%M%S).dump"

    echo "Backing up $DB_NAME..."
    pg_dump -h $PG_HOST -U $DB_USER -d $DB_NAME \
        --format=custom --compress=6 \
        --file=$BACKUP_FILE 2>&1

    if [ $? -eq 0 ]; then
        echo "  ✅ $DB_NAME → $BACKUP_FILE ($(du -h $BACKUP_FILE | cut -f1))"
    else
        echo "  ❌ $DB_NAME backup FAILED"
    fi
done

echo "Backup complete: $BACKUP_DIR"
```

### Schema-Only Backup (for migrations)

```bash
pg_dump -h localhost -U ${SERVICE}_user -d $DB_NAME \
  --schema-only \
  --no-owner \
  --no-privileges \
  > schema_${DB_NAME}.sql
```

## Restore Operations

### Full Restore

```bash
# ⚠️ WARNING: This will REPLACE all data in the target database!
SERVICE="order"
DB_NAME="${SERVICE}_db"
BACKUP_FILE="backup_${DB_NAME}_20260215_120000.dump"

# 1. Drop and recreate database
psql -h localhost -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$DB_NAME' AND pid <> pg_backend_pid();"
psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -h localhost -U postgres -c "CREATE DATABASE $DB_NAME OWNER ${SERVICE}_user;"

# 2. Restore from backup
pg_restore -h localhost -U postgres -d $DB_NAME \
  --no-owner --no-privileges \
  $BACKUP_FILE

echo "Restore complete for $DB_NAME"
```

### Table-Level Restore

```bash
# Restore specific tables from a backup
pg_restore -h localhost -U postgres -d $DB_NAME \
  --table=orders --table=order_items \
  --data-only \
  $BACKUP_FILE
```

## Point-in-Time Recovery (PITR)

### Prerequisites
- PostgreSQL WAL archiving enabled
- `archive_mode = on` and `archive_command` configured
- Regular base backups + continuous WAL archiving

### Recovery Steps

```bash
# 1. Stop the PostgreSQL server
systemctl stop postgresql

# 2. Remove current data directory
rm -rf /var/lib/postgresql/15/main/*

# 3. Restore base backup
pg_basebackup -h backup-server -D /var/lib/postgresql/15/main/ -U replication

# 4. Create recovery.conf (or postgresql.auto.conf for PG 12+)
cat > /var/lib/postgresql/15/main/postgresql.auto.conf << EOF
restore_command = 'cp /mnt/wal_archive/%f %p'
recovery_target_time = '2026-02-15 14:30:00+07'
recovery_target_action = 'promote'
EOF

# 5. Create recovery signal file (PG 12+)
touch /var/lib/postgresql/15/main/recovery.signal

# 6. Start PostgreSQL - it will replay WAL files up to target time
systemctl start postgresql

# 7. Verify recovery
psql -U postgres -c "SELECT pg_is_in_recovery();"
# Should return 'f' (false) after promotion
```

## Maintenance Operations

### VACUUM (Reclaim Storage)

```bash
# Regular maintenance vacuum (safe to run anytime)
psql -h localhost -U ${SERVICE}_user -d $DB_NAME \
  -c "VACUUM ANALYZE;"

# Full vacuum (locks tables — schedule during maintenance window)
psql -h localhost -U ${SERVICE}_user -d $DB_NAME \
  -c "VACUUM FULL ANALYZE;"
```

### REINDEX (Fix Bloated Indexes)

```bash
# Reindex specific table
psql -h localhost -U ${SERVICE}_user -d $DB_NAME \
  -c "REINDEX TABLE orders;"

# Reindex entire database (maintenance window)
psql -h localhost -U postgres -d $DB_NAME \
  -c "REINDEX DATABASE $DB_NAME;"
```

### Table Statistics

```bash
# Check table sizes
psql -h localhost -U ${SERVICE}_user -d $DB_NAME -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS data_size,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename) - pg_relation_size(schemaname || '.' || tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;
"
```

### Dead Row Monitoring

```bash
# Check for tables needing vacuum
psql -h localhost -U ${SERVICE}_user -d $DB_NAME -c "
SELECT
    relname AS table_name,
    n_dead_tup AS dead_rows,
    n_live_tup AS live_rows,
    round(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 2) AS dead_pct,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
"
```

## Goose Migrations

Each service uses [Goose](https://github.com/pressly/goose) for schema migrations.

### Running Migrations

```bash
cd <service>
# Up (apply all pending)
go run ./cmd/migrate up

# Down (rollback last)
go run ./cmd/migrate down

# Status
go run ./cmd/migrate status

# Migrate to specific version
go run ./cmd/migrate up-to 005
```

### Creating New Migrations

See the `create-migration` skill for detailed instructions.

```bash
# Convention: NNNN_description.sql
# Example: 026_add_exchange_order_support.sql
```

## Outbox & Idempotency Table Maintenance

### Cleanup Old Outbox Events

```sql
-- Delete processed events older than 7 days
DELETE FROM outbox_events
WHERE status = 'published'
  AND processed_at < NOW() - INTERVAL '7 days';

-- Archive failed events
INSERT INTO outbox_events_archive
SELECT * FROM outbox_events
WHERE status = 'failed'
  AND created_at < NOW() - INTERVAL '30 days';

DELETE FROM outbox_events
WHERE status = 'failed'
  AND created_at < NOW() - INTERVAL '30 days';
```

### Cleanup Old Idempotency Records

```sql
-- Delete old idempotency records (older than 14 days)
DELETE FROM event_idempotency
WHERE created_at < NOW() - INTERVAL '14 days';
```

## Monitoring Queries

### Connection Pool Status

```sql
SELECT
    datname,
    count(*) AS total_connections,
    count(*) FILTER (WHERE state = 'active') AS active,
    count(*) FILTER (WHERE state = 'idle') AS idle,
    count(*) FILTER (WHERE state = 'idle in transaction') AS idle_in_tx
FROM pg_stat_activity
GROUP BY datname
ORDER BY total_connections DESC;
```

### Slow Queries

```sql
SELECT
    pid,
    now() - query_start AS duration,
    state,
    left(query, 100) AS query_preview
FROM pg_stat_activity
WHERE state != 'idle'
  AND now() - query_start > INTERVAL '5 seconds'
ORDER BY duration DESC;
```

### Lock Monitoring

```sql
SELECT
    pg_blocking.pid AS blocking_pid,
    pg_blocked.pid AS blocked_pid,
    pg_blocking.query AS blocking_query,
    pg_blocked.query AS blocked_query
FROM pg_stat_activity AS pg_blocking
JOIN pg_locks AS bl ON bl.pid = pg_blocking.pid
JOIN pg_locks AS wl ON wl.locktype = bl.locktype
    AND wl.database IS NOT DISTINCT FROM bl.database
    AND wl.relation IS NOT DISTINCT FROM bl.relation
JOIN pg_stat_activity AS pg_blocked ON pg_blocked.pid = wl.pid
WHERE NOT bl.granted AND wl.granted;
```

## Emergency Procedures

### Kill Long-Running Queries

```bash
# Find and kill queries running longer than 5 minutes
psql -U postgres -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > INTERVAL '5 minutes'
  AND pid <> pg_backend_pid();
"
```

### Reset Connection Pool

```bash
# When a service has too many idle connections
# Restart the service pod (k8s will handle connection cleanup)
kubectl rollout restart deployment/<service-name>
```
