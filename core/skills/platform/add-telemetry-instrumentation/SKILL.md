---
name: add-telemetry-instrumentation
description: Add or update logging, metrics, and tracing by following the repo's observability patterns and OpenTelemetry (OTel) GenAI Semantic Conventions. Use when a service, feature, endpoint, job, or integration needs operational visibility — including AI/LLM features requiring token-level tracing (gen_ai.usage.input_tokens, gen_ai.request.model), multi-agent workflow correlation, RAG step spans, and tool invocation traces.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Add Telemetry Instrumentation

Use this skill when code changes need matching observability so operators can understand traffic, failures, latency, and dependency behavior.

## When to Use

- a service/endpoint/feature needs visibility
- adding logs, metrics, or traces (OTel)
- tracing AI/LLM token usage and RAG steps
- correlating multi-agent workflow spans

## Core Rules

- follow the repo's existing logging, metrics, and tracing patterns
- instrument important boundaries rather than every line of code
- keep telemetry names, labels, and dimensions stable enough for dashboards and alerts
- avoid high-cardinality labels unless the repo explicitly supports them
- never log secrets, credentials, tokens, or unnecessary sensitive data
- use stable OpenTelemetry GenAI conventions (opt in via `OTEL_SEMCONV_STABILITY_OPT_IN=genai`) for LLM/agent tracking; required attributes: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
- source GenAI conventions from the **dedicated `open-telemetry/semantic-conventions-genai` repository** (the old location in `semantic-conventions` is a moved-notice): include **agent spans** (`invoke_agent`, `execute_tool`) and **MCP spans** (`gen-ai-mcp`) for agent and MCP-server work; emit `gen_ai.response.finish_reasons` and opt-in content capture (`gen_ai.input.messages`) only when classification policy allows
- design hierarchical trace spans using `create_agent` operation types and step attributes (`agent.name`, `agent.step_type`) for agent reasoning
- configure Cloudflare Workers native observability using the `observability` block in `wrangler.jsonc` and OTLP push
- capture GPU infrastructure metrics prefixed with `hw.gpu.*` via OTel Collector and DCGM exporter integration
- **OTEL-PROFILING-4TH-PILLAR**: OTel Profiling is now the fourth observability pillar alongside logs/metrics/traces — use Pyroscope or eBPF-based profilers (Beyla) for continuous CPU/memory profiling and emit via OTLP profiling signal; do not rely solely on K8s `kubectl top` for performance diagnosis
- **NATIVE-HISTOGRAMS**: Replace classic Prometheus fixed-bucket histograms with Native Histograms (Prometheus 2.40+, OTel exponential histograms) for dynamic bucket resolution; eliminates the "wrong bucket count" problem and reduces cardinality overhead
- **DORA-METRIC-SPANS**: Emit CI/CD spans with semantic conventions (`cicd.pipeline.run.*`, `deploy.environment`) to enable automated DORA metric computation (Lead Time, MTTR) from trace data without manual aggregation

## Suggested Process

### 1. Identify Critical Paths

Determine the key entrypoints, dependency calls, background jobs, and failure domains that need visibility.

### 2. Add Structured Logging

Add logs for meaningful state changes, warnings, and errors.

Prefer repo-local conventions for:

- log levels
- correlation IDs or request IDs
- structured fields
- error wrapping or stack capture

### 3. Add Metrics

Add or update metrics that help answer operational questions:

- request, job, or event counts
- latency or duration distributions
- failure counts by stable reason
- dependency call outcomes

### 4. Add Tracing

Instrument spans across service boundaries, external API calls, database queries, or long-running internal operations when the repo uses tracing.

### 5. Check Operational Usefulness

Verify that the telemetry can support dashboards, alerts, incident triage, and release verification without creating noise.

### 6. Validate Sensitive Data Handling

Confirm that logs, metrics labels, and trace attributes do not expose secrets, credentials, tokens, or unnecessary personal data.

## Checklist

- [ ] existing telemetry pattern reviewed
- [ ] critical paths identified
- [ ] structured logs added or updated
- [ ] metrics added or updated
- [ ] tracing added or updated when the repo uses tracing
- [ ] sensitive data exposure checked
- [ ] dashboards, alerts, or runbooks updated when needed
- [ ] OpenTelemetry GenAI semantic conventions applied and enabled via `OTEL_SEMCONV_STABILITY_OPT_IN`
- [ ] agent reasoning steps traced hierarchically under a root `create_agent` span with `agent.name` and `agent.step_type`
- [ ] Cloudflare Workers telemetry configured with wrangler `observability` block and OTLP push
- [ ] GPU metrics (`hw.gpu.*`) scraped via OTel Collector and DCGM exporter

## Failure Modes

- **Instrumentation added without a dashboard**: a metric is emitted but no dashboard consumes it. **Mitigation:** require a dashboard at every instrumentation point; reject metrics without a dashboard.
- **PII in span attributes**: a span attribute contains PII or a credential. **Mitigation:** classify every span attribute with `data-classification.yaml`; redact restricted fields before persistence.
- **OTel SDK version drift**: an instrumentation library is updated without re-pinning the OTel registry. **Mitigation:** re-validate every span attribute against the current OTel GenAI convention on SDK upgrade; surface the drift.
- **Alert noise**: a new alert is added with no runbook. **Mitigation:** require a runbook at every alert; reject alerts without a runbook link.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: telemetry payloads may include PII or credentials; classify with `data-classification.yaml` and redact restricted fields.
- **ASI04 Supply Chain**: OTel SDKs, exporters, and collectors must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct telemetry processors or exporters from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: telemetry is consumed by SRE and security roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a telemetry rollout as "complete" without the verification run; surface the residual risk.

## Related Skills

- **debug-runtime-platform**: Investigate runtime behavior using telemetry evidence
- **setup-deployment**: Wire telemetry config into runtime source of truth
- **performance-profiling**: Measure latency, throughput, or resource bottlenecks
- **security-audit**: Review sensitive data exposure risk
- **commit-code**: Prepare telemetry changes for delivery
