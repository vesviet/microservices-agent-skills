---
description: Complete workflow for adding a new feature to a microservice
---

## Add New Feature Workflow

This workflow guides you through adding a new feature from design to deployment.

### Prerequisites
- Feature requirements clearly defined
- Service identified
- Latest code pulled

### Workflow Steps

#### 1. Design Phase

**Understand the requirements:**
- What is the business goal?
- What API endpoints are needed?
- What data models are required?
- What events need to be published/consumed?
- What external services need to be called?

**Check existing patterns:**
```bash
# Review similar features in the service
cd /home/user/microservices/<service>
grep -r "similar_feature" internal/
```

**Review standards:**
- [Coding Standards](../../docs/07-development/standards/coding-standards.md)
- [Team Lead Code Review Guide](../../docs/07-development/standards/TEAM_LEAD_CODE_REVIEW_GUIDE.md)

#### 2. Implementation Phase

**2.1 Define API Contract (if new endpoint)**

Use skill: `add-api-endpoint`

```bash
# Edit proto file
vim api/<service>/v1/<service>.proto

# Generate code
cd /home/user/microservices/<service> && make api
```

**2.2 Create Database Migration (if schema changes)**

Use skill: `create-migration`

```bash
cd /home/user/microservices/<service>
make migration name=add_feature_table
```

**2.3 Implement Business Logic**

Follow Clean Architecture layers:
1. Define domain entity in `internal/biz/<entity>.go`
2. Define repository interface in `internal/biz/<entity>.go`
3. Implement repository in `internal/data/<entity>.go`
4. Implement use case in `internal/biz/<entity>.go`
5. Implement service handler in `internal/service/<service>.go`

**2.4 Add Service Client (if calling other services)**

Use skill: `add-service-client`

**2.5 Add Event Handler (if consuming events)**

Use skill: `add-event-handler`

**2.6 Use Common Library**

Use skill: `use-common-lib`

Check `common/` for existing utilities before writing custom code.

#### 3. Testing Phase

**3.1 Write Tests**

Use skill: `write-tests`

```bash
# Run tests
cd /home/user/microservices/<service>
go test ./internal/biz/... -v
go test ./internal/service/... -v
go test ./internal/data/... -v
```

**3.2 Check Coverage**

```bash
go test ./internal/... -cover
```

Target: ≥60% for biz layer

#### 4. Quality Check Phase

**4.1 Lint**

```bash
cd /home/user/microservices/<service>
golangci-lint run
```

**4.2 Build**

```bash
go build ./...
```

**4.3 Regenerate Wire (if DI changed)**

```bash
cd cmd/<service> && wire
cd ../worker && wire  # if worker exists
```

#### 5. Documentation Phase

**5.1 Update CHANGELOG.md**

```markdown
## [Unreleased]
### Added
- New feature: <description>
- New API endpoint: `POST /api/v1/<service>/<resource>`
```

**5.2 Update README.md (if needed)**

Add new configuration, environment variables, or usage examples.

**5.3 Update Service Documentation (if significant change)**

Edit `docs/03-services/<group>/<service>-service.md`

#### 6. Review Phase

Use skill: `review-code`

Self-review checklist:
- [ ] Architecture layers respected (service → biz → data)
- [ ] Error handling comprehensive
- [ ] Input validation complete
- [ ] Context propagated through all layers
- [ ] No hardcoded values
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes (or versioned properly)

#### 7. Commit & Deploy Phase

Use skill: `commit-code`

```bash
cd /home/user/microservices/<service>

# Remove bin directory
rm -rf bin/

# Commit
git add -A
git commit -m "feat(<service>): add <feature_name>

- Added new API endpoint for <feature>
- Implemented business logic in biz layer
- Added database migration for <table>
- Updated documentation"

# Push (CI will build and deploy)
git push origin main
```

#### 8. Verification Phase

**8.1 Wait for CI/CD**

```bash
# Check if CI finished building
cd /home/user/microservices/gitops && git pull origin main
cat apps/<service>/base/kustomization.yaml | grep newTag
```

**8.2 Verify Deployment**

```bash
# Check pods
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl get pods -n <service>-dev"

# Check logs
ssh tuananh@dev.tanhdev.com -p 8785 "kubectl logs -n <service>-dev -l app=<service> --tail=50"
```

**8.3 Test the Feature**

```bash
# Test API endpoint
curl -X POST http://<service>-dev.tanhdev.com/api/v1/<service>/<resource> \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

### Common Issues & Solutions

**Issue: Wire generation fails**
```bash
# Check provider set in cmd/<service>/wire.go
# Ensure all dependencies are provided
cd cmd/<service> && wire
```

**Issue: Proto generation fails**
```bash
# Install proto tools
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest

# Copy third_party if missing
cp -r /home/user/microservices/user/third_party /home/user/microservices/<service>/
```

**Issue: Tests fail**
```bash
# Check test setup
# Ensure mocks are up to date
# Verify test data is correct
go test ./internal/... -v
```

### Related Workflows
- [Build & Deploy](build-deploy.md)
- [Service Review & Release](service-review-release.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills
- add-api-endpoint
- create-migration
- add-service-client
- add-event-handler
- write-tests
- review-code
- commit-code
