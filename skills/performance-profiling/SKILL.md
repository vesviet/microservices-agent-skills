---
name: performance-profiling
description: Profile and optimize Go microservice performance using pprof, benchmarks, and load testing
---

# Performance Profiling Skill

Use this skill when investigating performance issues, optimizing hot paths, or conducting load tests on microservices.

## When to Use
- Service response time is slow or increasing
- High memory usage or suspected memory leaks
- CPU spikes under load
- Before/after performance comparison for optimizations
- Capacity planning for production

---

## ⚠️ CRITICAL RULES

1. **Profile in dev K8s first** — never profile production without approval
2. **Use `pprof`** built into Go — don't install third-party profilers
3. **Benchmark with `go test -bench`** — not manual timing
4. **Load test with K6 or vegeta** — not manual curl loops
5. **Always baseline first** — measure before optimizing
6. **Focus on biz layer** — most bottlenecks are in business logic, not framework

---

## Tool 1: pprof (CPU & Memory Profiling)

### Enable pprof on Service

Most Kratos services already expose pprof at `/debug/pprof/` via HTTP. If not:

```go
// In internal/server/http.go
import _ "net/http/pprof"

// Or add explicit route
import "net/http/pprof"

srv.HandleFunc("/debug/pprof/", pprof.Index)
srv.HandleFunc("/debug/pprof/profile", pprof.Profile)
srv.HandleFunc("/debug/pprof/heap", pprof.Handler("heap").ServeHTTP)
```

### Capture CPU Profile (30 seconds)

```bash
# Port-forward the service HTTP port
ssh tuananh@dev.tanhdev.com -p 8785 \
  "kubectl port-forward -n <service>-dev svc/<service>-service 80XX:80XX &"

# Capture 30-second CPU profile
go tool pprof http://localhost:80XX/debug/pprof/profile?seconds=30

# Interactive mode commands:
# top10        → top 10 functions by CPU
# list FuncName → show line-by-line cost
# web          → open flamegraph in browser (requires graphviz)
```

### Capture Memory Profile

```bash
# Current heap allocations
go tool pprof http://localhost:80XX/debug/pprof/heap

# Alloc objects (total allocations, not just live)
go tool pprof -alloc_objects http://localhost:80XX/debug/pprof/heap

# Interactive:
# top10 -cum    → top by cumulative allocations
# list FuncName → line-by-line allocations
```

### Capture Goroutine Profile

```bash
# Current goroutine stack traces (detect leaks)
go tool pprof http://localhost:80XX/debug/pprof/goroutine

# Or raw dump:
curl http://localhost:80XX/debug/pprof/goroutine?debug=2
```

### Compare Before/After

```bash
# Capture baseline
go tool pprof -proto http://localhost:80XX/debug/pprof/heap > /tmp/before.pb.gz

# ... apply optimization ...

# Capture after
go tool pprof -proto http://localhost:80XX/debug/pprof/heap > /tmp/after.pb.gz

# Compare (shows diff)
go tool pprof -base /tmp/before.pb.gz /tmp/after.pb.gz
```

---

## Tool 2: Go Benchmarks

### Write Benchmark Tests

```go
// internal/biz/calculation/calculation_bench_test.go
package calculation

import "testing"

func BenchmarkCalculatePrice(b *testing.B) {
	uc := setupTestUsecase() // Create usecase with mock deps
	ctx := context.Background()
	req := &PriceCalculationRequest{
		ProductID: "prod-1",
		SKU:       "SKU-001",
		Quantity:  1,
		Currency:  "VND",
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, err := uc.CalculatePrice(ctx, req)
		if err != nil {
			b.Fatal(err)
		}
	}
}

func BenchmarkCalculatePrice_Parallel(b *testing.B) {
	uc := setupTestUsecase()
	ctx := context.Background()

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			req := &PriceCalculationRequest{
				ProductID: "prod-1",
				Quantity:  1,
			}
			uc.CalculatePrice(ctx, req)
		}
	})
}
```

### Run Benchmarks

```bash
# Run all benchmarks in a package
go test -bench=. -benchmem ./internal/biz/calculation/...

# Run specific benchmark
go test -bench=BenchmarkCalculatePrice -benchmem -count=5 ./internal/biz/calculation/

# Compare results (with benchstat)
go install golang.org/x/perf/cmd/benchstat@latest
go test -bench=. -benchmem -count=10 ./internal/biz/... > /tmp/before.txt
# ... optimize ...
go test -bench=. -benchmem -count=10 ./internal/biz/... > /tmp/after.txt
benchstat /tmp/before.txt /tmp/after.txt
```

### Reading Benchmark Output

```
BenchmarkCalculatePrice-8    500000    2345 ns/op    1024 B/op    12 allocs/op
│                        │    │         │              │            │
│                        │    │         │              │            └── allocations per op
│                        │    │         │              └── bytes allocated per op
│                        │    │         └── nanoseconds per operation
│                        │    └── iterations run
│                        └── GOMAXPROCS
└── benchmark name
```

---

## Tool 3: Load Testing

### Using K6

```bash
# Install k6
brew install k6

# Create test script
cat > /tmp/load_test.js << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up to 20 VUs
    { duration: '1m', target: 50 },     // Stay at 50 VUs
    { duration: '30s', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],   // 95% under 500ms
    http_req_failed: ['rate<0.01'],     // <1% error rate
  },
};

export default function () {
  const res = http.get('http://localhost:80XX/api/v1/<service>/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
EOF

# Run load test
k6 run /tmp/load_test.js
```

### Using vegeta (simpler)

```bash
# Install
brew install vegeta

# Run 100 req/sec for 30 seconds
echo "GET http://localhost:80XX/api/v1/<service>/health" | \
  vegeta attack -rate=100 -duration=30s | \
  vegeta report

# With JSON output for analysis
echo "GET http://localhost:80XX/api/v1/<service>/health" | \
  vegeta attack -rate=100 -duration=30s | \
  vegeta report -type=json
```

---

## Common Performance Issues & Fixes

| Symptom | Likely Cause | How to Detect | Fix |
|---------|-------------|---------------|-----|
| Slow API response | N+1 queries | pprof CPU → `gorm` in top | Add `Preload()` or `Joins()` |
| Memory grows indefinitely | Goroutine leak | pprof goroutine count growing | Add `ctx.Done()` checks, use `errgroup` |
| CPU spike on bulk ops | Unbounded loop | pprof CPU → biz function | Add pagination/batching with LIMIT |
| Slow under concurrent load | Lock contention | pprof block/mutex profile | Reduce lock scope, use `sync.RWMutex` |
| High allocs/op in benchmark | Excessive object creation | `-benchmem` output | Reuse objects, use `sync.Pool` |
| Slow JSON marshal | Large payload | pprof CPU → `encoding/json` | Use pagination, exclude unnecessary fields |

---

## Checklist

### Profiling
- [ ] pprof enabled on service
- [ ] CPU profile captured (30s under load)
- [ ] Heap profile captured
- [ ] Goroutine count checked (no leaks)
- [ ] Top 5 hot functions identified

### Benchmarks
- [ ] Benchmark tests written for critical paths
- [ ] Baseline measurements recorded
- [ ] Optimization applied
- [ ] Before/after comparison done (benchstat)

### Load Testing
- [ ] Load test script created
- [ ] Baseline throughput measured (RPS)
- [ ] P95 latency measured
- [ ] Error rate under load checked

---

## Related Skills

- **troubleshoot-service**: Debug runtime issues
- **review-code**: Review code for performance issues
- **write-tests**: Write benchmark tests
- **debug-k8s**: Access service for profiling
- **meeting-review**: Review with Security/Perf agent perspective
