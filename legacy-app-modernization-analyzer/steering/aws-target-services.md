---
inclusion: always
---

# AWS Target Services for Modernization

This guide maps common legacy components to AWS-native services.

## Compute Services

| Legacy Component | AWS Service | Notes |
|------------------|-------------|-------|
| Application Server (WebLogic, WebSphere, IIS) | Amazon ECS / EKS | Container orchestration |
| Virtual Machines | Amazon EC2 / Fargate | Serverless containers preferred |
| Batch Processing | AWS Batch / Step Functions | Managed batch workloads |
| Scheduled Jobs | Amazon EventBridge / Lambda | Serverless scheduling |

### Container Recommendations

- **ECS Fargate**: Simplified container deployment, no server management
- **EKS**: Kubernetes-based orchestration for complex workloads
- **Graviton Processors**: Up to 40% cost savings with ARM64

## Database Services

| Legacy Database | AWS Service | Migration Path |
|-----------------|-------------|----------------|
| SQL Server | Amazon RDS SQL Server | Lift-and-shift |
| SQL Server | Aurora PostgreSQL | Cost optimization (no licensing) |
| Oracle | Amazon RDS Oracle | Lift-and-shift |
| Oracle | Aurora PostgreSQL | Cost optimization |
| DB2 | Amazon RDS | Via DMS migration |
| MySQL | Amazon RDS MySQL / Aurora MySQL | Direct migration |

### Database Migration Tools

- **AWS Schema Conversion Tool (SCT)**: Schema and stored procedure conversion
- **AWS Database Migration Service (DMS)**: Data migration with minimal downtime
- **pgLoader**: Open-source alternative for PostgreSQL migration

### Cost Optimization

Database licensing is often the largest cost component:
- SQL Server licensing: Very High ongoing cost
- Oracle licensing: Very High ongoing cost
- Aurora PostgreSQL: No licensing fees, High savings potential

## Messaging Services

| Legacy Messaging | AWS Service | Use Case |
|------------------|-------------|----------|
| MSMQ | Amazon SQS | Point-to-point queuing |
| WebSphere MQ | Amazon SQS / Amazon MQ | Enterprise messaging |
| WebLogic JMS | Amazon SQS / MSK | JMS replacement |
| RabbitMQ | Amazon MQ | Managed RabbitMQ |
| Kafka | Amazon MSK | Managed Kafka |
| Pub/Sub | Amazon SNS | Fan-out messaging |
| Event-Driven | Amazon EventBridge | Event bus |

## Security Services

| Legacy Security | AWS Service | Notes |
|-----------------|-------------|-------|
| Windows Auth | Amazon Cognito | OAuth 2.0/OIDC |
| LDAP | Amazon Cognito / Directory Service | Identity management |
| Custom Auth | Amazon Cognito | User pools |
| Secrets Storage | AWS Secrets Manager | Credential management |
| Certificate Management | AWS Certificate Manager | SSL/TLS certificates |

## Configuration & Storage

| Legacy Component | AWS Service | Notes |
|------------------|-------------|-------|
| Config Files | AWS Systems Manager Parameter Store | Centralized config |
| File Storage | Amazon S3 | Object storage |
| Session State | Amazon ElastiCache / DynamoDB | Distributed sessions |
| Caching | Amazon ElastiCache | Redis/Memcached |

## Observability

| Legacy Monitoring | AWS Service | Notes |
|-------------------|-------------|-------|
| Application Logs | Amazon CloudWatch Logs | Centralized logging |
| Metrics | Amazon CloudWatch Metrics | Application metrics |
| Tracing | AWS X-Ray | Distributed tracing |
| APM | CloudWatch Application Insights | Application monitoring |

## Networking

| Legacy Component | AWS Service | Notes |
|------------------|-------------|-------|
| Load Balancer | Application Load Balancer (ALB) | Layer 7 load balancing |
| DNS | Amazon Route 53 | DNS management |
| CDN | Amazon CloudFront | Content delivery |
| VPN | AWS VPN / Direct Connect | Hybrid connectivity |

## AWS Well-Architected Alignment

### Operational Excellence
- Infrastructure as Code (CloudFormation, CDK)
- Automated deployment pipelines (CodePipeline)
- Observability (CloudWatch, X-Ray)

### Security
- Secrets management (Secrets Manager)
- IAM roles for service authentication
- Encryption in transit and at rest
- VPC isolation and security groups

### Reliability
- Multi-AZ deployment
- Auto-scaling
- Circuit breakers (with application code)
- Graceful degradation patterns

### Performance Efficiency
- Graviton processors for cost-optimized performance
- Right-sizing based on workload
- Caching strategies

### Cost Optimization
- Graviton instances (up to 40% savings)
- Spot instances for non-critical workloads
- Reserved capacity for predictable workloads
- License elimination (Aurora PostgreSQL vs SQL Server)

## Recommended Migration Tools

| Tool | Purpose |
|------|---------|
| AWS Application Discovery Service | Discover on-premises applications |
| AWS Migration Hub | Track migration progress |
| AWS App2Container | Containerize .NET and Java apps |
| AWS Transform | .NET modernization assistance |
| Kiro | AI-powered migration assistance |
