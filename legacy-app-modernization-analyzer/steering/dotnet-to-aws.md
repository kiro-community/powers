---
inclusion: manual
---

# .NET Framework to .NET 8 + AWS Modernization

## Platform Detection

### .NET-Specific Files to Detect

- `.sln` - Solution files
- `.csproj` / `.vbproj` - Project files
- `web.config` / `app.config` - Configuration files
- `packages.config` - Legacy NuGet packages
- `appsettings.json` - Modern configuration
- `Global.asax` - ASP.NET application file

### .NET-Specific Dependencies

- `System.Web.*` - ASP.NET Web Forms
- `System.Data.SqlClient` / `Microsoft.Data.SqlClient` - SQL Server
- `System.ServiceModel.*` - WCF
- `EntityFramework` / `Microsoft.EntityFrameworkCore` - ORM

### Target Framework Detection

Extract from `.csproj` files:
- `<TargetFramework>net48</TargetFramework>` - .NET Framework 4.8
- `<TargetFramework>net6.0</TargetFramework>` - .NET 6
- `<TargetFramework>net8.0</TargetFramework>` - .NET 8

## Migration Strategy Bank

### API & Library Modernization

| Current | Target | Notes |
|---------|--------|-------|
| EF6 | EF Core 8 | Modern ORM with better performance |
| Web Forms | ASP.NET Core MVC/Razor | Modern web framework |
| WCF | gRPC or REST APIs | Cloud-native communication |
| ADO.NET | Dapper or EF Core | Simplified data access |
| ASP.NET MVC 5 | ASP.NET Core MVC | Cross-platform MVC |
| Web API 2 | ASP.NET Core Web API | Modern REST APIs |

### Architecture Transformation

| Current | Target | Notes |
|---------|--------|-------|
| Monolith | Microservices | Containerized, independently deployable |
| IIS-hosted | Docker/ECS/EKS | Linux containers on AWS |
| Traditional MVC | API + SPA | Modern frontend separation |
| x86 | ARM (Graviton) | Cost optimization |
| Windows Server | Linux | Cost savings, better container support |

### Database Modernization

| Current | Target | Notes |
|---------|--------|-------|
| SQL Server | Aurora PostgreSQL | Cost optimization (no licensing) |
| SQL Server | Amazon RDS SQL Server | Managed service |
| LINQ to SQL | EF Core | Modern data access |
| Stored Procedures | Application code | Better testability |

### Messaging & Integration

| Current | Target | Notes |
|---------|--------|-------|
| MSMQ | Amazon SQS/SNS | Cloud-native messaging |
| Azure Service Bus | Amazon SQS/EventBridge | AWS event-driven |
| NServiceBus | MassTransit | Modern service bus |
| SignalR | SignalR on AWS | Real-time communication |

### Security Modernization

| Current | Target | Notes |
|---------|--------|-------|
| Windows Auth | AWS Cognito | OAuth 2.0/OIDC |
| ASP.NET Membership | ASP.NET Core Identity | Modern identity |
| Forms Auth | JWT/OAuth2 | Token-based auth |
| Machine Keys | AWS KMS | Key management |

### Cloud-Native Patterns

| Current | Target | Notes |
|---------|--------|-------|
| web.config | AWS Parameter Store | Centralized config |
| File storage | Amazon S3 | Scalable object storage |
| Session State | ElastiCache/DynamoDB | Distributed sessions |
| Logging | AWS CloudWatch | Centralized logging |
| Caching | ElastiCache | Distributed caching |

## .NET-Specific Evaluation Areas

### Platform & Framework Assessment

- **Target Framework Version**: v4.x vs .NET Core/5+/6+/8
- **Windows-Only Dependencies**: Identify Windows-specific APIs
- **32-bit vs 64-bit**: Architecture compatibility
- **Framework EOL Status**: Support lifecycle assessment

### ASP.NET Web Forms Assessment

If Web Forms detected:
- Count of `.aspx` pages
- ViewState usage complexity
- Code-behind patterns
- User controls and custom controls
- Master pages structure

Migration options:
1. **Incremental**: Add ASP.NET Core alongside Web Forms
2. **Rewrite**: Full rewrite to Blazor or React
3. **Strangler Fig**: Gradually replace pages

### WCF Assessment

If WCF detected:
- Service contracts (`[ServiceContract]`)
- Data contracts (`[DataContract]`)
- Binding configurations
- Security modes (Transport, Message)
- Duplex/callback patterns

Migration options:
1. **gRPC**: For internal service communication
2. **REST API**: For external/public APIs
3. **CoreWCF**: For minimal changes (limited)

### Entity Framework Assessment

If EF6 detected:
- DbContext implementations
- Code-First vs Database-First
- Migration history
- Lazy loading usage
- Complex relationships

Migration to EF Core:
- Breaking changes in EF Core
- Removed features (lazy loading proxy differences)
- New features (split queries, compiled queries)

## NuGet License Verification

For each NuGet package, verify license via NuGet.org API:

1. Query: `https://api.nuget.org/v3/registration5-gz-semver2/{package-id}/index.json`
2. Extract `catalogEntry` URL
3. Fetch catalog entry and extract `licenseExpression` (SPDX identifier)

Include verification note in report:
> 📋 **License Verification**: All NuGet package licenses were verified by querying the NuGet.org Catalog API.

## SQL Server to PostgreSQL Migration

### T-SQL to PostgreSQL Conversion

| T-SQL | PostgreSQL | Notes |
|-------|------------|-------|
| `GETDATE()` | `NOW()` or `CURRENT_TIMESTAMP` | |
| `ISNULL(a, b)` | `COALESCE(a, b)` | |
| `CONVERT(type, value)` | `CAST(value AS type)` | |
| `TOP n` | `LIMIT n` | Move to end of query |
| `DATEADD(day, n, date)` | `date + INTERVAL 'n days'` | |
| `DATEDIFF(day, a, b)` | `DATE_PART('day', b - a)` | |
| `nvarchar(max)` | `TEXT` | |
| `uniqueidentifier` | `UUID` | |
| `datetime2` | `TIMESTAMP` | |
| `money` | `DECIMAL(19,4)` | |

### Migration Tools

- **AWS Schema Conversion Tool (SCT)**: Schema and stored procedure conversion
- **AWS Database Migration Service (DMS)**: Data migration
- **pgLoader**: Open-source data migration

## Recommended Tools

Prioritize AWS Transform tools in this order:

| Tool | Purpose | Priority |
|------|---------|----------|
| AWS Transform for Windows Full Stack | End-to-end .NET modernization including framework upgrade + database migration | 1st - Use when both app and DB migration needed |
| AWS Transform for .NET | .NET Framework to .NET Core/8 porting, EF6 → EF Core migration | 2nd - Use for application-only migration |
| AWS Schema Conversion Tool (SCT) | Database schema conversion analysis (SQL Server → PostgreSQL) | 3rd - Use for database-only scenarios |
| AWS Database Migration Service (DMS) | Data migration with minimal downtime | 3rd - Use with SCT for database migration |
| AWS App2Container | Containerization of existing .NET applications | 4th - Use for lift-and-shift containerization |
| Kiro | AI-assisted code migration and refactoring | Supplementary - Use throughout all phases |

**Tool Selection Guidance:**
- For full modernization (.NET upgrade + SQL Server → Aurora PostgreSQL): Use **AWS Transform for Windows Full Stack**
- For .NET framework upgrade only (keeping SQL Server): Use **AWS Transform for .NET**
- For database migration only (keeping .NET Framework): Use **SCT + DMS**
- For containerization without code changes: Use **AWS App2Container**

## Code Migration Examples

### web.config to appsettings.json

**Before (web.config):**
```xml
<connectionStrings>
  <add name="DefaultConnection" 
       connectionString="Server=myserver;Database=mydb;User Id=user;Password=pass;" />
</connectionStrings>
<appSettings>
  <add key="ApiKey" value="secret123" />
</appSettings>
```

**After (appsettings.json):**
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=myserver;Database=mydb;Username=user;Password=pass;"
  },
  "ApiKey": "secret123"
}
```

### ASP.NET MVC to ASP.NET Core

**Before (ASP.NET MVC 5):**
```csharp
public class HomeController : Controller
{
    public ActionResult Index()
    {
        return View();
    }
}
```

**After (ASP.NET Core):**
```csharp
public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    
    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }
    
    public IActionResult Index()
    {
        return View();
    }
}
```

### EF6 to EF Core

**Before (EF6):**
```csharp
public class MyDbContext : DbContext
{
    public MyDbContext() : base("DefaultConnection") { }
    public DbSet<Customer> Customers { get; set; }
}
```

**After (EF Core):**
```csharp
public class MyDbContext : DbContext
{
    public MyDbContext(DbContextOptions<MyDbContext> options) : base(options) { }
    public DbSet<Customer> Customers { get; set; }
}
```
