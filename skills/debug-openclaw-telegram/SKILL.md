---
name: debug-openclaw-telegram
description: Debug OpenClaw Telegram bot issues on the homelab server, including health checks, gateway/service failures, template breakage, OAuth/API-key confusion, and safe cleanup guardrails
---

# Debug OpenClaw Telegram Skill

Use this skill when Telegram on OpenClaw returns generic failures, stops replying, shows model/auth errors, or breaks after migration/cleanup on the homelab server.

## Environment

- Active server: `tuananh@192.168.1.114`
- Retired server: `tuananh@192.168.1.112` (should stay off to avoid Telegram polling conflicts)
- Repo path: `/home/tuananh/openclaw`
- Config path: `/home/tuananh/.openclaw/openclaw.json`
- Service file: `/home/tuananh/.config/systemd/user/openclaw-gateway.service`
- Workspace path: `/home/tuananh/.openclaw/workspace`
- Runtime log: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

## Known Good Baseline

- Gateway runs as user service: `openclaw-gateway`
- System Node is `/usr/bin/node` on Node 24
- Gateway bind is `loopback`
- `loginctl show-user tuananh -p Linger` should be `Linger=yes`
- `memorySearch` is disabled
- `openai-codex/gpt-5.2` and `openai-codex/gpt-5.4` use `transport: sse`

## Fast Triage

Run these in order:

```bash
# 1) Service state
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'systemctl --user is-active openclaw-gateway && systemctl --user status openclaw-gateway --no-pager | head -40'

# 2) Health
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'cd /home/tuananh/openclaw && /usr/bin/node dist/index.js health 2>&1 | head -120'

# 3) Direct model/agent test
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'cd /home/tuananh/openclaw && /usr/bin/node dist/index.js agent --agent main --message "Reply with exactly: ok" --json --timeout 60 2>&1 | head -200'

# 4) Recent log scan
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'LOG=$(ls -1 /tmp/openclaw/openclaw-*.log 2>/dev/null | tail -1); echo "$LOG"; tail -n 200 "$LOG"'
```

## Log Patterns To Grep

```bash
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'LOG=$(ls -1 /tmp/openclaw/openclaw-*.log 2>/dev/null | tail -1); \
   grep -i -E "telegram dispatch failed|Missing workspace template|No API key for provider|gateway closed|assistant_error|sendMessage ok|409|getUpdates conflict" "$LOG" | tail -120'
```

## Known Failure Modes

### Telegram says `Something went wrong while processing your request`

Check logs first. In this environment, one confirmed cause was:

- `Missing workspace template: AGENTS.md (/home/tuananh/openclaw/docs/reference/templates/AGENTS.md)`

This happened after SSD cleanup removed runtime templates under `docs/reference/templates`.

Fix:

```bash
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 '
  set -e
  mkdir -p /home/tuananh/openclaw/docs/reference/templates
  for f in AGENTS.md BOOTSTRAP.md HEARTBEAT.md IDENTITY.md SOUL.md TOOLS.md USER.md; do
    cp "/home/tuananh/.openclaw/workspace/$f" "/home/tuananh/openclaw/docs/reference/templates/$f"
  done
  printf "%s\n" "# Memory" "" "Runtime memory template placeholder." > /home/tuananh/openclaw/docs/reference/templates/MEMORY.md
  cp /home/tuananh/openclaw/docs/reference/templates/MEMORY.md /home/tuananh/openclaw/docs/reference/templates/memory.md
  systemctl --user restart openclaw-gateway
'
```

Then rerun `health` and the direct `agent` test.

### `No API key for provider: openai-codex`

This does not always mean logout. Verify auth first:

```bash
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'cd /home/tuananh/openclaw && /usr/bin/node dist/index.js models status --check 2>&1 | head -240'
```

Notes:

- OAuth can still be valid even when a code path incorrectly expects an API key
- This setup uses `sse` for `openai-codex` models to avoid the older WS path that caused auth/fallback issues
- If config drift happened, confirm `transport: "sse"` is still set in `~/.openclaw/openclaw.json`

### `gateway closed (1006 abnormal closure)`

- If it appears during a manual restart, treat it as transient
- If it keeps happening during normal operation, restart the service and rerun `health` plus the direct `agent` test
- If `health` is green and the direct `agent` test returns `ok`, Telegram usually recovers after the restart

### Telegram `409` / polling conflict

Two servers are polling the same bot token.

Fix:

- Keep only `192.168.1.114` running
- Ensure `openclaw-gateway` on `192.168.1.112` stays disabled/stopped

## Safe Recovery Commands

```bash
# Restart cleanly
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'systemctl --user restart openclaw-gateway && sleep 2 && systemctl --user is-active openclaw-gateway'

# Verify templates still exist
ssh -o ConnectTimeout=10 tuananh@192.168.1.114 \
  'ls -la /home/tuananh/openclaw/docs/reference/templates'
```

## Cleanup Guardrails

Safe to remove when slimming the server:

- old backups under home
- `.git`, editor metadata, and most source/docs that are not required at runtime
- old Node versions under `~/.nvm` after the service has moved to `/usr/bin/node`

Do not remove:

- `/home/tuananh/openclaw/dist`
- `/home/tuananh/openclaw/node_modules`
- `/home/tuananh/openclaw/extensions`
- `/home/tuananh/openclaw/docs/reference/templates`
- `/home/tuananh/.openclaw/workspace`
- `/home/tuananh/.openclaw/openclaw.json`
- `/home/tuananh/.config/systemd/user/openclaw-gateway.service`

## Verification Checklist

- [ ] `systemctl --user is-active openclaw-gateway` is `active`
- [ ] `health` shows `Telegram: ok`
- [ ] direct `agent` test returns `ok`
- [ ] latest log has no new `Missing workspace template`
- [ ] latest log has no new `No API key for provider: openai-codex`
