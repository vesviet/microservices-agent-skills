---
name: meeting-review
description: Simulate a multi-agent meeting review (up to 7 specialist agents) to discuss, debate, and review any codebase topic — auto-selects the best panel based on topic
---

# Meeting Review Skill — Multi-Agent Panel Discussion

Mô phỏng cuộc họp review với **4-5 chuyên gia AI** (chọn tự động từ bảng 7 agents) cùng thảo luận, tranh luận và đánh giá một chủ đề trong codebase. Mỗi agent có góc nhìn riêng biệt, tạo ra bức tranh toàn diện về vấn đề.

---

## When to Use

- User nói: "meeting review", "họp review", "thảo luận về...", "discuss về..."
- Cần đánh giá đa chiều (kỹ thuật + business) cho một vấn đề
- Trước khi bắt tay refactor/viết tính năng lớn
- Đánh giá architecture decision hoặc tech debt
- Review infrastructure, deployment, hoặc database design

---

## The 7 Agent Pool

### 🔒 Core Agents (Luôn có mặt)

| Icon | Agent | Title | Focus Area | Câu hỏi đặc trưng |
|------|-------|-------|-----------|-------------------|
| 📐 | **Agent A** | **System Architect** | Architecture, Clean Architecture, DDD, component boundaries, scalability, system design patterns | "Kiến trúc có đúng hướng không? Boundaries có rõ ràng không?" |
| 🛡️ | **Agent B** | **Security & Performance Engineer** | Auth, vulnerabilities, race conditions, memory leaks, goroutine safety, OWASP, load testing, benchmarks | "Có lỗ hổng bảo mật không? Performance bottleneck ở đâu?" |
| 💻 | **Agent C** | **Senior Go Developer (10+ YOE)** | Go idioms, Kratos best practices, testability, code quality, DRY, SOLID, concurrency patterns, error handling | "Code có clean không? Test được không? Có đúng Go conventions không?" |

### 🔄 Contextual Agents (Chọn 1-2 theo topic)

| Icon | Agent | Title | Focus Area | Câu hỏi đặc trưng |
|------|-------|-------|-----------|-------------------|
| � | **Agent D** | **Senior Business Analyst / Domain Expert** | Business rules, edge cases, acceptance criteria, cross-domain consistency, backward compatibility, compliance (GDPR), revenue/UX impact | "Nếu coupon hết hạn giữa lúc checkout thì xử lý thế nào? Spec có ghi rõ chưa?" |
| 🛠️ | **Agent E** | **Senior DevOps / SRE** | K8s, ArgoCD, GitOps, CI/CD, Helm, Kustomize, Observability (Prometheus/Grafana/Jaeger), Vault, KEDA, Argo Rollouts, Zero-Downtime | "Deployment có zero-downtime không? Monitoring đã cover chưa? Secret management an toàn chưa?" |
| 🧪 | **Agent F** | **QA Lead / Test Engineer** | Test strategy, E2E coverage, edge case identification, regression planning, table-driven tests, mock strategy, integration testing | "Happy path và sad path đã đủ chưa? Concurrent edge case nào chưa có test?" |
| 🗄️ | **Agent G** | **Database / Data Engineer** | Schema design, migrations, index strategy, query optimization (N+1), data consistency, denormalization trade-offs, partitioning | "Index có phủ query chính chưa? Denormalized field có cơ chế reconciliation không?" |

---

## Auto-Select Logic

Skill tự chọn combo agents dựa trên **topic keywords**. 3 Core agents (A, B, C) luôn có mặt:

| Topic chứa từ khóa | Panel (Core + Contextual) |
|---|---|
| `service`, `logic`, `flow`, `feature`, `checkout`, `payment`, `order` | A + B + C + **📋 BA** |
| `gitops`, `k8s`, `deploy`, `infra`, `helm`, `argocd`, `cicd` | A + B + C + **🛠️ DevOps** |
| `test`, `coverage`, `e2e`, `tính năng mới`, `regression` | A + B + C + **🧪 QA** |
| `schema`, `migration`, `query`, `database`, `index`, `table` | A + B + C + **🗄️ Data Engineer** |
| `stock`, `pricing`, `promotion`, `discount` (sensitive data + complex rules) | A + B + C + **📋 BA** + **🗄️ Data Engineer** |
| `auth`, `security`, `rbac`, `jwt`, `oauth` | A + B + C + **📋 BA** + **🛠️ DevOps** |
| `new feature`, `chức năng mới`, `thiết kế mới` | A + B + C + **📋 BA** + **🧪 QA** |

> **Override**: User luôn có thể yêu cầu thêm/bớt agent. Ví dụ: "họp review gitops, thêm agent QA luôn"

---

## Execution Process

### Step 1: Understand the Topic

1. **Parse user's request** — xác định vấn đề/module cần review
2. **Auto-select panel** — chọn combo agents phù hợp theo bảng trên
3. Nếu user chỉ nói chung chung (e.g. "review order service"), hỏi clarify:
   - Review toàn bộ service hay chỉ 1 phần?
   - Focus vào logic nào? (routing, event flow, data layer, security, performance...)
   - Có concern cụ thể nào không?

### Step 2: Index the Codebase

1. **Identify target files** — dùng `find_by_name`, `list_dir` để tìm các file liên quan
2. **Read key files** — dùng `view_file_outline` trước, rồi `view_file` cho các file quan trọng
3. **Trace dependencies** — dùng `grep_search` để hiểu data flow và dependencies
4. **Check config** — đọc config files liên quan (yaml, proto, migrations)
5. **Target coverage**: Đọc tối thiểu:
   - Entry point (`cmd/*/main.go`, `cmd/*/wire.go`)
   - Business logic (`internal/biz/`)
   - Data layer (`internal/data/`)
   - API layer (`internal/service/`)
   - Event handlers (`internal/worker/`, `internal/events/`)
   - Config (`configs/`, `api/*/v1/*.proto`)
   - Relevant docs (`docs/`)

### Step 3: Conduct the Meeting Review

Tạo một **Artifact (.md)** với cấu trúc sau. Mỗi section phải có **thảo luận thật sự giữa các agents** — không chỉ liệt kê issues mà phải có:
- Agent tranh luận, phản bác nhau
- Agent bổ sung ý cho nhau
- Agent từ góc nhìn khác (BA vs Dev, DevOps vs Architect) đánh giá cùng 1 issue

#### Artifact Structure:

```markdown
# 🏛️ [Topic] — Multi-Agent Meeting Review

> **Date**: YYYY-MM-DD
> **Topic**: [Mô tả ngắn chủ đề review]
> **Scope**: [Files/modules được review]
> **Panel**: [Danh sách agents được chọn và lý do]

---

## 👥 Panel Members
[Bảng agents với vai trò — chỉ liệt kê agents ĐƯỢC CHỌN cho session này]

---

## 1. [Section Name — e.g. Architecture Overview]

### 📐 Agent A (Architect):
> [Nhận xét từ góc nhìn kiến trúc]

### 💻 Agent C (Senior Dev):
> [Nhận xét từ góc nhìn code quality]

### � Agent D (BA/Domain Expert):
> [Nhận xét từ góc nhìn business rules & edge cases]

---

## 2. [Section Name — e.g. Core Logic Review]

### 🚨 Issue 2.1 — [Tên Issue] (P0/P1/P2)

**Vị trí**: `file.go` (Lines X-Y)

**📐 Agent A**: [Phân tích kiến trúc]
**🛡️ Agent B**: [Phân tích security/perf]
**💻 Agent C**: [Phân tích code, đề xuất fix cụ thể]
**� Agent D**: [Đánh giá business impact & edge cases]

---

## N. 🚩 PENDING ISSUES (Consolidated)

### 🚨 Critical (P0)
| # | Issue | Impact (Business) | Action Required |
|---|---|---|---|

### 🟡 High Priority (P1)
| # | Issue | Impact (Business) |
|---|---|---|

### 🔵 Nice to Have (P2)
| # | Issue | Value |
|---|---|---|

---

## 🎯 Executive Summary

### Agent A (Architect): [1-2 câu kết luận]
### Agent B (Sec/Perf): [1-2 câu kết luận]
### Agent C (Senior Dev): [1-2 câu kết luận]
### Agent D/E/F/G: [Kết luận từ contextual agent được chọn]
```

### Step 4: Generate Action Items (Optional)

Nếu user yêu cầu, tạo thêm **task file** (`AGENT-XX-*.md`) trong:
```
docs/10-appendix/checklists/workflow/agent-tasks/
```

Task file phải có:
- [ ] Checklist cho từng issue
- Exact file + line locations
- Code snippets (BEFORE → AFTER)
- Validation commands (`go test`, `go build`, `curl`)
- Pre-commit checklist
- Commit message template

---

## Agent Behavior Rules

### All Agents MUST:
1. **Reference exact file paths và line numbers** — không nói chung chung
2. **Cite code snippets** khi chỉ ra lỗi
3. **Disagree constructively** — agents phải tranh luận, không chỉ đồng ý
4. **Prioritize using P0/P1/P2** severity from the project's coding standards

### 📐 Agent A (Architect) MUST:
- Đánh giá Clean Architecture boundaries (biz/data/service layers)
- Check component coupling và dependency direction
- Evaluate scalability implications
- Review DDD patterns (bounded contexts, aggregates)

### 🛡️ Agent B (Security/Perf) MUST:
- Check OWASP Top 10 vulnerabilities
- Identify race conditions, goroutine leaks, memory issues
- Evaluate circuit breaker, retry, timeout configurations
- Check authorization/authentication at every entry point
- Assess performance under load (N+1, unbounded queries, cache effectiveness)

### 💻 Agent C (Senior Dev) MUST:
- Evaluate Go idioms (error handling, interfaces, context propagation)
- Check testability (can this code be unit tested without external deps?)
- Identify DRY violations and code duplication
- Review Kratos framework usage (proper middleware, transport layer)
- Check `common` library usage (don't reinvent what exists)
- Assess code readability and maintainability

### 📋 Agent D (BA / Domain Expert) MUST:
- Phát hiện **edge cases** mà developer dễ bỏ qua (concurrent state, timeout giữa flow)
- Kiểm tra **business rules** khớp với spec/requirements
- Đánh giá **backward compatibility** với clients/frontends hiện tại
- Xác định **cross-domain side effects** (e.g. stock → pricing → checkout)
- Translate technical issues thành **revenue/UX impact**
- Hỏi: "Nếu X xảy ra giữa chừng thì Y xử lý thế nào?" (If-then edge cases)

### 🛠️ Agent E (DevOps / SRE) MUST:
- Đánh giá deployment strategy (Rolling vs Canary vs Blue-Green)
- Check GitOps alignment (Kustomize overlays, ArgoCD sync policies)
- Review observability (logs structured? trace propagation? metrics exposed?)
- Evaluate secret management (Vault, SealedSecrets, env vars)
- Check graceful shutdown, health probes, resource limits
- Assess disaster recovery và auto-healing mechanisms

### 🧪 Agent F (QA Lead) MUST:
- Đánh giá test coverage: unit, integration, E2E
- Identify untested edge cases và propose test scenarios
- Review mock strategy (proper interface mocking vs brittle mocks)
- Check table-driven test patterns (Go convention)
- Evaluate regression risk of proposed changes
- Ask: "Nếu deploy bản này, test nào sẽ catch regression?"

### 🗄️ Agent G (Data Engineer) MUST:
- Review schema design (normalization vs denormalization trade-offs)
- Check index coverage cho hot queries
- Identify N+1 query patterns
- Evaluate migration safety (backward compatible? rollback plan?)
- Assess data consistency mechanisms (transactions, reconciliation jobs)
- Review partition/sharding strategy cho large tables

---

## Discussion Style Guide

### DO:
```markdown
**💻 Agent C**: Tôi không đồng ý với Agent A ở điểm này. Mặc dù tách 
module sẽ clean hơn, nhưng với codebase hiện tại chỉ có 3 developer, 
việc tách quá nhỏ sẽ tạo overhead không cần thiết. Tôi đề xuất...

**� Agent D (BA)**: Agent B, race condition này xảy ra cụ thể khi nào? 
Nếu user checkout 2 tab cùng lúc dùng cùng coupon, system trả kết quả 
gì? Spec hiện tại không ghi rõ case này...

**🛠️ Agent E (DevOps)**: Agent A đề xuất tách service, nhưng GitOps 
hiện tại đã có 26 apps. Thêm 1 service nữa nghĩa là thêm namespace, 
configmap, secrets, HPA, PDB. Overhead vận hành đáng kể.
```

### DON'T:
```markdown
❌ Tất cả agents đồng ý đây là vấn đề. 
❌ Agent A: Tốt. Agent B: Tốt. Agent C: Tốt. Agent D: Tốt.
```

Agents phải có **distinct voices** và **real disagreements** khi thích hợp.

---

## Example Triggers

| User says | Auto-selected Panel |
|---|---|
| "meeting review order service" | A + B + C + **📋 BA** |
| "họp review về event flow" | A + B + C + **📋 BA** |
| "discuss về payment security" | A + B + C + **📋 BA** + **🛠️ DevOps** |
| "review kiến trúc catalog" | A + B + C + **📋 BA** |
| "thảo luận checkout flow" | A + B + C + **📋 BA** + **🗄️ Data** |
| "họp review gitops" | A + B + C + **🛠️ DevOps** |
| "review DB schema warehouse" | A + B + C + **🗄️ Data Engineer** |
| "review tính năng mới loyalty" | A + B + C + **📋 BA** + **🧪 QA** |
| "review test coverage order" | A + B + C + **🧪 QA** |

---

## Output Artifacts

1. **Review Report** → saved to artifact directory (`gateway_logic_review.md`, `order_review.md`, etc.)
2. **Task File** (optional) → saved to `docs/10-appendix/checklists/workflow/agent-tasks/AGENT-XX-*.md`
