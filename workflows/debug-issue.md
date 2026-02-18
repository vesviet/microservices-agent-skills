---
description: Troubleshooting and debugging - optimized for problem-solving
---

# Debug Issue Workflow

Use this workflow for **investigating and resolving bugs, errors, and unexpected behavior** in microservices.

## When to Use

- Service crashes or errors
- Unexpected behavior in production or staging
- Failed deployments or pod issues
- Integration problems between services
- Performance issues
- Event delivery failures

## Approach

**Optimization**: Systematic problem-solving and investigation
- Follow the evidence, avoid assumptions
- Start broad, narrow down systematically
- Document findings for future reference

## Steps

1. **Gather information**
   - What is the observed behavior?
   - What is the expected behavior?
   - When did it start? What changed?
   - Is it reproducible? Under what conditions?
   - Which service(s) are affected?

2. **Check infrastructure first**
   - Use `debug-k8s` skill for Kubernetes issues
   - Check pod status, logs, and resource usage
   - Verify ConfigMaps and Secrets are correct
   - Check ArgoCD sync status

3. **Analyze logs**
   - Check service logs for errors and stack traces
   - Look for correlation IDs to trace requests
   - Check timestamps to identify when issues started
   - Review logs from related services

4. **Trace the flow**
   - For API issues: trace the request through all layers
   - For event issues: use `trace-event-flow` skill
   - For gRPC issues: check client and server logs
   - Verify data flow: delivery → biz → data

5. **Check configuration**
   - Verify environment variables
   - Check database connections
   - Verify external service endpoints
   - Review Dapr configuration

6. **Reproduce locally if possible**
   - Try to reproduce in local development
   - Use the same data if relevant
   - Compare local vs production configuration

7. **Use troubleshooting skill**
   - Use `troubleshoot-service` skill for common issues
   - Check for known patterns: build errors, connection failures, crashes

8. **Fix and verify**
   - Make minimal changes to fix the issue
   - Test the fix thoroughly
   - Deploy and monitor
   - Document the root cause and fix

9. **Prevent recurrence**
   - Add tests to catch this in the future
   - Update documentation if needed
   - Consider if architecture changes would help
   - Add monitoring/alerting if appropriate

## Common Issues & Quick Checks

### Service Won't Start
- Check environment variables
- Verify database connectivity
- Check for conflicting ports
- Review Init() errors in logs

### Event Not Being Consumed
- Verify Dapr subscription configuration
- Check topic names match exactly
- Review consumer logs for errors
- Use `trace-event-flow` skill

### gRPC Call Failing
- Verify service discovery configuration
- Check client-side configuration
- Review server logs for errors
- Validate proto compatibility

### Database Errors
- Check migration status
- Verify connection strings
- Review query logs for SQL errors
- Check for lock/deadlock issues

## Skills to Use

- `troubleshoot-service` - For common service issues
- `debug-k8s` - For Kubernetes deployment issues
- `trace-event-flow` - For event delivery problems
- `navigate-service` - To understand code flow

## Tips

- Don't change multiple things at once
- Keep notes of what you've tried
- Use correlation IDs to trace requests
- Check recent changes (git log, ArgoCD)
- Consider asking for help if stuck > 1 hour
- Document solutions for similar future issues
