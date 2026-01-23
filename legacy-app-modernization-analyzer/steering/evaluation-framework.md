---
inclusion: always
---

# Common Modernization Evaluation Framework

This framework applies to ALL modernization analyses regardless of source platform (.NET, WebSphere, WebLogic).

## Universal Evaluation Areas

### 1. Architecture Assessment

Evaluate the current architecture for modernization readiness:

- **Monolithic vs Modular**: Identify if application is monolithic or has modular components
- **Layering Patterns**: Assess Domain/Data/Web/Infrastructure separation
- **Coupling Analysis**: Measure inter-component dependencies
- **Layering Violations**: Identify cross-layer dependencies that violate architecture
- **Service Boundaries**: Identify potential microservice decomposition points

### 2. Code Quality

Assess codebase maintainability:

- **Cyclomatic Complexity**: Measure method/class complexity
- **Maintainability Index**: Overall code maintainability score
- **Code Duplication**: Identify duplicated code blocks
- **Technical Debt**: Estimate accumulated technical debt
- **Code Coverage**: Existing test coverage percentage

### 3. DevOps Readiness

Evaluate CI/CD and deployment maturity:

- **CI/CD Pipeline**: Existing automation for build/test/deploy
- **Container Readiness**: Dockerfile or containerization present
- **Infrastructure as Code**: CloudFormation, CDK, Terraform usage
- **Environment Parity**: Dev/staging/prod consistency
- **Deployment Frequency**: Current release cadence

### 4. Security Patterns

Assess security implementation:

- **Authentication Mechanisms**: Current auth patterns (LDAP, OAuth, custom)
- **Authorization Patterns**: Role-based access control implementation
- **Secrets Management**: How credentials are stored and accessed
- **Transport Security**: TLS/SSL configuration
- **Security Vulnerabilities**: Known CVEs in dependencies

### 5. Observability

Evaluate monitoring and logging:

- **Logging Patterns**: Structured vs unstructured logging
- **Log Aggregation**: Centralized logging solution
- **Metrics Collection**: Application and infrastructure metrics
- **Distributed Tracing**: Request tracing across services
- **Alerting**: Monitoring and alerting configuration

### 6. Database Layer

Assess data access patterns:

- **ORM Usage**: Entity Framework, Hibernate, JPA, etc.
- **Connection Patterns**: Connection pooling, transaction management
- **Stored Procedure Complexity**: Count and complexity of stored procedures
- **Database-Specific Features**: Vendor-specific SQL features in use
- **Data Model Complexity**: Relationship complexity, normalization level

### 7. Testing Maturity

Evaluate test coverage and quality:

- **Unit Test Coverage**: Percentage of code covered by unit tests
- **Integration Tests**: Presence of integration test suites
- **End-to-End Tests**: Automated E2E testing
- **Performance Tests**: Load and stress testing capability
- **Test Automation**: CI integration of test suites

### 8. Documentation Quality

Assess existing documentation:

- **Architecture Diagrams**: Current state documentation
- **API Documentation**: OpenAPI/Swagger or equivalent
- **Runbooks**: Operational documentation
- **Code Comments**: Inline documentation quality
- **README Files**: Project documentation completeness

## Risk of Inaction Framework

For EVERY finding, articulate the business impact if not modernized:

| Risk Category | Questions to Answer |
|---------------|---------------------|
| Security | What vulnerabilities will emerge? What compliance risks exist? |
| Performance | How will performance degrade over time? |
| Support Lifecycle | When do frameworks/libraries reach EOL? |
| Competitive Disadvantage | How does technical debt impact time-to-market? |
| Cost Implications | What are the ongoing maintenance costs? |
| Talent Acquisition | How hard is it to hire developers for legacy tech? |
| Scalability | Can the system handle future growth? |

## Strategic Alignment Frameworks

### AWS 7 Rs of Migration

Classify each modernization pathway:

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Rehost** | Lift-and-shift to cloud | Quick migration, minimal changes |
| **Replatform** | Lift-tinker-and-shift | Minor optimizations during migration |
| **Refactor** | Re-architect for cloud-native | Significant modernization needed |
| **Repurchase** | Move to SaaS | Replace with commercial solution |
| **Retire** | Decommission | Application no longer needed |
| **Retain** | Keep as-is | Not ready for migration |
| **Relocate** | Hypervisor-level migration | VMware to AWS migration |

### Gartner TIME Framework

Classify applications for portfolio decisions:

| Classification | Description | Action |
|----------------|-------------|--------|
| **Tolerate** | Keep running with minimal investment | Maintain only |
| **Invest** | Modernize and enhance | Active development |
| **Migrate** | Move to new platform | Platform change |
| **Eliminate** | Decommission or replace | Remove from portfolio |

## Cost-Benefit Analysis Framework

### Infrastructure Cost Comparison

Use qualitative levels (Low/Medium/High/Very High) for:

- Current infrastructure costs
- Modernized infrastructure costs
- Licensing costs (current vs target)
- Operational overhead
- Savings potential

### ROI Assessment

Evaluate return on investment:

- Investment level required
- Expected returns (cost savings, efficiency gains)
- Time to value realization
- Risk-adjusted returns

## Report Quality Standards

### Visualization Requirements

- Use Mermaid.js for ALL diagrams
- NEVER use ASCII art
- Include architecture diagrams (current and target state)
- Include dependency graphs
- Include migration roadmap visualizations

### Evidence-Based Analysis

- Reference actual files, packages, and patterns found
- Provide specific metrics (file counts, LOC, dependency counts)
- Include code examples for migration patterns
- Back all claims with codebase evidence
