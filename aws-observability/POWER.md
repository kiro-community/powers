---
name: "aws-observability"
displayName: "AWS Observability"
description: "Comprehensive AWS observability platform combining CloudWatch Logs, Metrics, Alarms, Application Signals (APM), CloudTrail security auditing, and automated codebase observability gap analysis, for complete monitoring, troubleshooting, and optimization."
keywords: ["cloudwatch", "logs", "metrics", "traces", "alarms", "alerts", "monitoring", "observability", "application signals", "apm", "distributed tracing", "x-ray", "opentelemetry", "otel", "slow", "latency", "performance", "bottleneck", "degradation", "timeout", "high latency", "slow api", "api performance", "service performance", "response time", "p50", "p90", "p95", "p99", "errors", "error rate", "fault rate", "failure rate", "5xx", "4xx", "exceptions", "availability", "uptime", "downtime", "outage", "sev1", "sev2", "slo", "sli", "service level", "error budget", "breach", "troubleshooting", "root cause", "rca", "investigate", "diagnose", "log analysis", "log insights", "log query", "log patterns", "audit", "cloudtrail", "security audit", "access logs", "iam changes", "change events", "service map", "cascading failure", "canary", "synthetic monitoring", "health check", "observability gaps", "missing instrumentation", "monitoring instrumentation", "structured logging", "silent failures", "logging gaps", "alarm investigation", "trace analysis", "span analysis", "request tracing"]
author: "AWS"
---

# Onboarding

## Prerequisites

1. **AWS CLI configured** with credentials (`aws configure` or `~/.aws/credentials`)
2. **Python 3.10+** and `uv` installed ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))
3. **Application Signals enabled** in your AWS account whenever applicable ([Getting started with Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Intro.html))
4. **Required AWS Permissions**: Your IAM user/role needs:
   - `cloudwatch:*` for CloudWatch Metrics and Alarms
   - `logs:*` for CloudWatch Logs operations (includes CloudTrail log querying)
   - `xray:*` for distributed tracing
   - `cloudtrail:*` for CloudTrail queries
   - `application-signals:*` for Application Signals (e.g., `ListServices`, `GetService`, `ListServiceOperations`, `ListServiceLevelObjectives`, `GetServiceLevelObjective`, `BatchGetServiceLevelObjectiveBudgetReport`, `ListAuditFindings`, `ListEntityEvents`, `ListServiceStates`)
   - `synthetics:GetCanary`, `synthetics:GetCanaryRuns` for canary analysis
   - `s3:GetObject`, `s3:ListBucket` for canary artifacts
   - `iam:GetRole`, `iam:ListAttachedRolePolicies`, `iam:GetPolicy`, `iam:GetPolicyVersion` for the enablement guide

## Configuration

After installing this power, update the MCP server configuration with your AWS profile and region:

1. Open Kiro Settings → MCP Servers (or edit `~/.kiro/settings/mcp.json`)
2. Find the `awslabs.cloudwatch-mcp-server` entry
3. Update the `env` section:

```json
"env": {
  "AWS_PROFILE": "your-profile-name",  // ← Change to your AWS profile
  "AWS_REGION": "us-east-1",           // ← Change to your region
  "FASTMCP_LOG_LEVEL": "ERROR"
}
```

**Default:** Uses `default` AWS profile and `us-east-1` region.

## Quick Test

After configuration, try: *"Show me my CloudWatch log groups"*

---

# Overview

The comprehensive AWS observability platform combining monitoring, troubleshooting, security, and optimization tools in one power.

**Key capabilities:**
- **CloudWatch Logs** - Query and analyze logs using CloudWatch Logs Insights
- **Metrics & Alarms** - Metric querying with Metrics Insights and intelligent alarm recommendations
- **Application Signals** - APM with distributed tracing, service maps, SLOs, and enablement guides
- **Codebase Observability Analysis** - Automated analysis of codebases to identify observability gaps and provide actionable recommendations
- **CloudTrail Integration** - Security auditing and compliance tracking
- **AWS Documentation** - Direct access to official AWS docs for troubleshooting

**Authentication**: Requires AWS credentials (AWS CLI profile or IAM role).

## Core Capabilities

### 1. CloudWatch Logs

**Primary Use Case**: Query and analyze logs using CloudWatch Logs Insights

**Key Features**:
- CloudWatch Logs Insights query syntax for log analysis
- Multi-log-group queries across up to 50 log groups
- JSON field extraction with parse and filter commands
- Statistical functions and aggregations
- Pattern detection and anomaly analysis
- Log group discovery and metadata
- Saved queries support

**When to Use**:
- Searching and filtering log data across services
- Aggregations and statistical analysis
- Querying multiple log groups simultaneously
- Extracting structured data from JSON logs
- Troubleshooting distributed application issues

### 2. CloudWatch Metrics & Alarms

**Primary Use Case**: Monitor resource performance and set up intelligent alerting

**Key Features**:
- Retrieve metric data with multiple statistics (Average, Sum, Min, Max, percentiles)
- Metrics Insights for advanced filtering and grouping
- Analyze metric trends, seasonality, and anomalies
- Get recommended alarm configurations based on AWS best practices
- View active alarms and alarm history
- Support for custom metrics and composite alarms

**When to Use**:
- Monitoring EC2, Lambda, RDS, and other AWS service metrics
- Setting up performance baselines and thresholds
- Creating intelligent alarms with recommended configurations
- Investigating active alarms and reviewing alarm history
- Analyzing metric trends and detecting anomalies
- Troubleshooting performance degradation

### 3. Application Signals (APM)

**Primary Use Case**: Application performance monitoring with distributed tracing

**Key Features**:
- Service-level metrics and SLOs
- Distributed tracing with AWS X-Ray integration
- Service maps showing dependencies and call paths
- Error rate and latency tracking (P50, P90, P95, P99)
- Automatic service discovery
- SLO compliance monitoring and error budget tracking
- Enablement guide for setup assistance
- Primary audit tools (`audit_services`, `audit_slos`, `audit_service_operations`) as recommended entry points for all investigation workflows, with wildcard targeting and 7 auditor types (`slo`, `operation_metric`, `trace`, `log`, `dependency_metric`, `top_contributor`, `service_quota`)
- 100% Trace Visibility via `search_transaction_spans` querying OpenTelemetry spans through CloudWatch Logs Insights (vs X-Ray's 5% sampling)
- Canary Failure Analysis via `analyze_canary_failures` for root cause investigation of CloudWatch Synthetics canaries

**When to Use**:
- Monitoring microservices health and performance
- Troubleshooting latency and error rate issues
- Understanding service dependencies and bottlenecks
- Setting up and tracking SLOs
- Root cause analysis for distributed systems
- Getting started with Application Signals setup

### 4. CloudTrail Security Auditing

**Primary Use Case**: Security auditing, compliance, and governance

**Data Source Priority**: CloudTrail data is accessed through multiple sources in priority order:
1. **CloudTrail Lake** (Priority 1) - SQL-based querying with 7-year retention
2. **CloudWatch Logs** (Priority 2) - Real-time analysis with CloudWatch integration
3. **Lookup Events API** (Priority 3) - Fallback for basic queries (90-day limit)

See `cloudtrail-data-source-selection.md` steering file for detailed decision tree.

**Key Features**:
- API call history and analysis
- User activity tracking across AWS accounts
- Resource change tracking and audit trails
- IAM permission change monitoring
- Compliance reporting and security investigations
- Multiple data source options for flexibility

**When to Use**:
- Investigating security incidents
- Tracking resource modifications and deletions
- Compliance auditing and reporting
- Understanding who did what and when
- Detecting unauthorized access attempts
- Root cause analysis for configuration changes

### 5. Cost Explorer

**Primary Use Case**: AWS cost analysis, forecasting, and optimization

**Key Features**:
- Cost and usage data retrieval with flexible grouping
- Cost forecasting based on historical patterns
- Cost comparison between time periods
- Cost driver analysis to identify spending changes
- Support for filtering by service, region, tags, and more
- Dimension and tag value discovery

**When to Use**:
- Analyzing AWS spending patterns
- Forecasting future costs
- Identifying cost optimization opportunities
- Comparing costs across time periods
- Understanding what's driving cost changes
- Budget planning and cost allocation

### 6. AWS Documentation Access

**Primary Use Case**: Quick access to official AWS documentation

**Key Features**:
- Search AWS documentation directly
- Read documentation pages in markdown format
- Get content recommendations for related topics
- Access service-specific guides and API references

**When to Use**:
- Looking up AWS service documentation
- Understanding API parameters and behavior
- Finding best practices and tutorials
- Troubleshooting with official guidance

### 7. Codebase Observability Analysis

**Primary Use Case**: Automated analysis of application codebases to identify observability gaps

**Key Features**:
- Multi-language support (Python, Java, JavaScript/TypeScript, Go, Ruby, C#/.NET)
- Logging pattern analysis and gap identification
- Metrics instrumentation assessment
- Distributed tracing coverage evaluation
- Error handling review
- Health check and readiness probe validation
- Actionable recommendations with code examples
- Prioritized gap reports by severity

**When to Use**:
- Auditing existing applications for observability best practices
- Onboarding new services to observability standards
- Improving debugging and troubleshooting capabilities
- Preparing for production deployments
- Establishing observability baselines
- Training teams on observability patterns

## Available Steering Files

### 1. `incident-response.md`
**Troubleshooting and incident management workflows**

Load this when the user needs to:
- Respond to production incidents
- Troubleshoot application errors or performance issues
- Investigate service outages
- Perform root cause analysis
- Create incident reports and postmortems

Do NOT load this when:
- General log querying without an active incident (use `log-analysis.md`)
- Routine performance monitoring or SLO tracking (use `performance-monitoring.md`)
- Standalone security audits or compliance reviews (use `security-auditing.md`)
- Setting up or configuring alarms (use `alerting-setup.md`)

### 2. `log-analysis.md`
**Log querying and analysis patterns**

Load this when the user needs to:
- Query logs using CloudWatch Logs Insights
- Search and filter log events
- Extract structured data from JSON logs
- Aggregate log data with statistics
- Troubleshoot application issues using logs

Do NOT load this when:
- Active incident response with multi-tool correlation (use `incident-response.md`)
- CloudTrail-specific security analysis (use `security-auditing.md`)
- Application Signals APM metrics and traces (use `performance-monitoring.md`)

### 3. `alerting-setup.md`
**Creating intelligent alarms and notifications**

Load this when the user needs to:
- Set up new CloudWatch alarms
- Improve existing alarm configurations
- Reduce alarm fatigue and false positives
- Create intelligent alerting strategies
- Implement SLO-based alerting

Do NOT load this when:
- Investigating or responding to active alarms (use `incident-response.md`)
- General metric analysis without alarm creation (use `performance-monitoring.md`)

### 4. `performance-monitoring.md`
**Application Signals APM and performance tracking**

Load this when the user needs to:
- Monitor microservices health and performance
- Analyze distributed traces
- Set up Service Level Objectives (SLOs)
- Troubleshoot performance issues
- Understand service dependencies
- Track error rates and latency

Do NOT load this when:
- Active incident response requiring multi-tool triage (use `incident-response.md`)
- Log-only analysis without Application Signals (use `log-analysis.md`)
- Setting up or configuring alarms (use `alerting-setup.md`)

### 5. `security-auditing.md`
**CloudTrail security analysis and compliance**

Load this when the user needs to:
- Investigate security incidents
- Track API activity and resource changes
- Perform compliance audits
- Monitor IAM changes
- Detect unauthorized access attempts
- Generate audit reports

Do NOT load this when:
- Active incident response requiring multi-tool triage (use `incident-response.md`)
- General application log analysis (use `log-analysis.md`)

### 6. `observability-gap-analysis.md`
**Codebase observability analysis and recommendations**

Load this when the user needs to:
- Audit a codebase for observability best practices
- Identify missing instrumentation points
- Analyze logging patterns and gaps
- Review metrics collection coverage
- Assess distributed tracing implementation
- Get recommendations for observability improvements

### 7. `application-signals-setup.md`
**Step-by-step Application Signals enablement**

This steering file provides comprehensive guidance for setting up AWS Application Signals using the power's enablement guide feature. Always start by getting the official enablement guide from AWS using the `get_enablement_guide` tool.

### 8. `cloudtrail-data-source-selection.md`
**CloudTrail data source priority and selection strategy**

Referenced by `security-auditing.md` for CloudTrail data access priority logic. Not intended for direct loading in response to user queries.

## Quick Start Examples

### Example 1: Investigate High Error Rate

```
1. Check active alarms for service health
   - Identify services with elevated error rates
   - View service dependencies and call paths in Application Signals

2. Query CloudWatch Logs
   - Find error patterns and stack traces
   - Correlate errors across multiple services

3. Review CloudTrail for recent changes
   - Check for deployments or configuration changes
   - Identify who made changes and when

4. Analyze traces for root cause
   - Examine slow or failed traces
   - Identify bottlenecks in service dependencies

5. Check AWS Documentation
   - Look up error codes and troubleshooting steps
   - Review best practices for the affected services
```

### Example 2: Performance Optimization

```
1. Analyze CloudWatch Metrics
   - Review CPU, memory, and latency metrics
   - Identify performance trends and anomalies
   - Get recommended alarm thresholds

2. Query Application Signals
   - Check P95/P99 latency for services
   - Analyze service maps for bottlenecks
   - Review SLO compliance

3. Examine logs for patterns
   - Calculate percentiles and aggregations
   - Identify slow operations and outliers
```

### Example 3: Security Audit

```
1. Query CloudTrail events
   - Track IAM changes and permission modifications
   - Identify unauthorized access attempts
   - Review resource deletions

2. Correlate with CloudWatch Logs
   - Connect CloudTrail events with application logs
   - Analyze access patterns

3. Check Application Signals
   - Review service-to-service authentication
   - Identify unusual traffic patterns

4. Document findings
   - Access AWS documentation for security best practices
```

### Example 4: Codebase Observability Gap Audit

```
1. Analyze codebase structure
   - Identify entry points (API handlers, Lambda functions)
   - Map critical business operations
   - Review error handling patterns

2. Assess logging coverage
   - Check for structured logging implementation
   - Identify missing correlation IDs
   - Find silent failures and empty catch blocks

3. Evaluate metrics instrumentation
   - Review custom CloudWatch metrics
   - Check business metric coverage
   - Assess performance metric collection

4. Review distributed tracing
   - Verify X-Ray SDK integration
   - Check trace context propagation
   - Evaluate subsegment coverage

5. Generate actionable report
   - Prioritize gaps by severity
   - Provide code examples for fixes
   - Estimate implementation effort
```

## Log Query Patterns

The CloudWatch MCP server uses CloudWatch Logs Insights query syntax via the `execute_log_insights_query` tool. It also provides `analyze_log_group` for automated pattern and anomaly detection.

### Basic Error Search

```
fields @timestamp, @message, @logStream, level
| filter level = "ERROR"
| sort @timestamp desc
| limit 100
```

### Performance Analysis with Aggregations

```
stats count() as requestCount,
      avg(duration) as avgDuration,
      pct(duration, 95) as p95Duration,
      pct(duration, 99) as p99Duration
by endpoint
| filter requestCount > 10
| sort p95Duration desc
```

### JSON Field Extraction

```
fields @timestamp, @message
| parse @message '{"userId": "*", "action": "*"}' as userId, action
| stats count() as actionCount by userId, action
| sort actionCount desc
| limit 100
```

### Error Rate Over Time

```
stats count() as total,
      sum(statusCode >= 500) as errors,
      (sum(statusCode >= 500) / count()) * 100 as errorRate
by bin(5m) as timeWindow
| sort timeWindow
```

### Multi-Log-Group Query

Use the `log_group_identifiers` parameter to query across multiple log groups:
```
fields @timestamp, @message, @logStream
| filter @message like /ERROR|Exception/
| sort @timestamp desc
| limit 50
```

## Common Observability Workflows

### Workflow 1: Complete Incident Investigation

1. **Identify the Issue**
   - Check Application Signals for service health and SLO breaches
   - Review active CloudWatch alarms
   - Analyze metric trends for anomalies

2. **Gather Evidence**
   - Query logs to find error patterns
   - Examine distributed traces for failed requests
   - Check CloudTrail for recent changes

3. **Root Cause Analysis**
   - Correlate logs, metrics, and traces
   - Analyze service dependencies and bottlenecks
   - Review AWS documentation for known issues

4. **Document and Resolve**
   - Create runbooks for future incidents
   - Set up preventive alarms

### Workflow 2: Performance Optimization

1. **Baseline Current Performance**
   - Collect metrics for all services
   - Analyze Application Signals SLOs
   - Query logs for latency patterns

2. **Identify Bottlenecks**
   - Use log aggregations to find slow operations
   - Examine traces for long-running spans
   - Check service maps for dependency issues

3. **Implement and Monitor**
   - Set up alarms with recommended thresholds
   - Track SLO compliance

### Workflow 3: Security and Compliance Audit

1. **Collect Audit Data**
   - Query CloudTrail for IAM changes
   - Track resource modifications
   - Identify access patterns

2. **Analyze Activity**
   - Correlate CloudTrail with application logs
   - Check for unauthorized access attempts
   - Review permission changes

3. **Generate Reports**
   - Document findings with AWS documentation references
   - Track compliance metrics

4. **Remediate and Monitor**
   - Set up CloudTrail alarms for critical events
   - Implement preventive controls
   - Establish ongoing monitoring

## Best Practices

### CloudWatch Logs
1. Always include timestamp filters to minimize scan volume
2. Use specific log groups to improve query performance
3. Use LIMIT to prevent overwhelming result sets
4. Use `analyze_log_group` for automated pattern and anomaly detection
5. Test queries on small time windows first
6. Leverage `stats` and `parse` commands for structured analysis

### CloudWatch Metrics & Alarms
1. Use appropriate statistics for different metric types:
   - `Sum` for count metrics (Errors, Invocations)
   - `Average` for utilization metrics (CPUUtilization)
   - Percentiles (p95, p99) for latency metrics
2. Leverage Metrics Insights for complex queries
3. Use recommended alarm configurations as starting points
4. Monitor alarm history to tune thresholds

### Application Signals
1. Instrument applications with AWS X-Ray SDK
2. Define meaningful service names with environment prefixes
3. Set realistic SLOs aligned with business requirements
4. Use adaptive sampling for high-volume services
5. Always capture error traces for debugging

### CloudTrail
1. Enable CloudTrail in all regions
2. **Consider CloudTrail Lake** for long-term retention and SQL-based analysis
3. Integrate with CloudWatch Logs for real-time analysis and alerting
4. Set up alerts for critical security events
5. Regular audit log reviews
6. Use the data source priority approach for efficient querying

## Integration Patterns

### Logs + Metrics + Traces
```
# Correlate logs with Application Signals traces
fields @timestamp, requestId, traceId, @message, duration, statusCode
| filter traceId like /./
| filter duration > 1000
| sort @timestamp desc
| limit 50
```

### CloudTrail + Logs
```
# Find errors correlated with recent changes
fields @timestamp, @message, errorType, requestId
| filter level = "ERROR"
| sort @timestamp desc
| limit 50
```
Then cross-reference timestamps with CloudTrail events using the data source priority:
1. Query CloudTrail Lake event data store (if available)
2. Query CloudWatch Logs for CloudTrail events (if integrated)
3. Use `lookup_events` API (fallback)

This helps identify configuration changes that may have caused errors.

### Metrics + Cost
Use CloudWatch Metrics to identify high-utilization resources, then analyze their costs in Cost Explorer to find optimization opportunities.

## Troubleshooting

### Common Issues

1. **"Insufficient permissions" errors**
   - Verify IAM policies include all required actions
   - Check resource-based policies on log groups
   - Ensure Cost Explorer is enabled in your account

2. **"Query timeout" errors**
   - Reduce time range in queries
   - Use more specific filters
   - Query fewer log groups at once

3. **"No results found"**
   - Verify log group names and ARNs are correct
   - Check time range matches your data
   - Ensure field names are case-sensitive correct

4. **MCP server connection issues**
   - Verify uvx is installed: `pip install uv`
   - Check AWS credentials: `aws sts get-caller-identity`
   - Review MCP server logs (set FASTMCP_LOG_LEVEL=DEBUG)

5. **Audit log file location**
   - The `cloudwatch-applicationsignals-mcp-server` supports an `AUDITOR_LOG_PATH` environment variable that controls where audit tools write their log files (defaults to `/tmp`)

## Available MCP Servers

### awslabs.cloudwatch-mcp-server
CloudWatch Logs querying, Metrics, Alarms, and log group analysis.

### awslabs.cloudwatch-applicationsignals-mcp-server
Application Signals APM with service health, SLOs, and distributed tracing.

### awslabs.cloudtrail-mcp-server
CloudTrail security auditing and API activity tracking.

### awslabs.aws-documentation-mcp-server
Search and read official AWS documentation.

## License
This power integrates with CloudWatch MCP Server, CloudWatch Application Signals MCP Server, CloudTrail MCP Server, and AWS Documentation MCP Server from [AWS Labs](https://github.com/awslabs/mcp) (Apache-2.0 license). All steering files and power configuration are licensed under Apache-2.0.

---

**Source:** AWS Labs
**License:** Apache 2.0
**Documentation:** https://github.com/awslabs/mcp
