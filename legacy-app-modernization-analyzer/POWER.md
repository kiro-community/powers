---
name: "legacy-app-modernization-analyzer"
displayName: "Legacy App Modernization Analyzer"
description: "Analyzes legacy enterprise codebases (.NET, WebSphere, WebLogic) and generates comprehensive AWS modernization feasibility reports with visual architecture diagrams, dependency analysis, and migration pathways"
keywords: [".NET", "WebSphere", "WebLogic", "Spring Boot", "modernization", "migration", "legacy", "AWS", "containerization", "microservices", "J2EE", "Jakarta", "reactive"]
version: "2.0.0"
---

# Legacy App Modernization Analyzer

## Overview

This power provides elite-level enterprise architecture analysis for legacy application modernization projects. It supports multiple source platforms and generates comprehensive feasibility reports with visual diagrams, following a rigorous evaluation framework and migration strategy bank.

## Supported Modernization Paths

| Source Platform | Target Platform | Steering File |
|-----------------|-----------------|---------------|
| .NET Framework 4.x | .NET 8 + AWS | `steering/dotnet-to-aws.md` |
| IBM WebSphere | Spring Boot Reactive + AWS | `steering/websphere-to-springboot.md` |
| Oracle WebLogic | Spring Boot Reactive + AWS | `steering/weblogic-to-springboot.md` |

## Workflow

### Step 1: Platform Detection

Scan the codebase to identify the source platform:

**Detect .NET:**
- Look for: `.sln`, `.csproj`, `.vbproj`, `web.config`, `packages.config`, `appsettings.json`
- If found → Load `steering/dotnet-to-aws.md`

**Detect WebSphere:**
- Look for: `ibm-web-bnd.xml`, `ibm-web-ext.xml`, `ibm-application-bnd.xml`, `ibm-ejb-jar-bnd.xml`
- JAR dependencies: `com.ibm.websphere.*`, `com.ibm.ws.*`, `com.ibm.mq.*`
- If found → Load `steering/websphere-to-springboot.md`

**Detect WebLogic:**
- Look for: `weblogic.xml`, `weblogic-application.xml`, `weblogic-ejb-jar.xml`
- JAR dependencies: `weblogic.*`, `oracle.weblogic.*`, `com.bea.*`
- If found → Load `steering/weblogic-to-springboot.md`

### Step 2: Load Common Framework

ALWAYS load these steering files for any analysis:
- `steering/common/evaluation-framework.md` - Universal evaluation areas
- `steering/common/report-structure.md` - **AUTHORITATIVE** report format standards
- `steering/common/aws-target-services.md` - AWS service mappings

### Step 3: Execute Platform-Specific Analysis

Follow the loaded platform steering file for:
- Technology-specific detection patterns
- Migration strategy bank
- Code transformation examples
- Platform-specific risks and mitigations

## Analysis Methodology

### Exhaustive Analysis Mode

Generate the most detailed, comprehensive report possible. Assume the user demands extreme depth - this is $1M/project consulting-grade work.

### Incremental Codebase Scanning

To avoid context overflow when analyzing large codebases:

**Phase 1: Discovery (Lightweight)**
- First, scan ONLY for solution/project files
- Build a project inventory WITHOUT reading full file contents
- Identify the solution structure and project count

**Phase 2: Targeted Analysis (Per-Project)**
- Analyze ONE project at a time
- In the first pass, gather a map of all files to understand scope
- Read only files relevant to the current analysis step
- Summarize findings before moving to the next project

**Phase 3: Selective Deep Dives**
- Only read full file contents when specifically needed
- Use grep/search tools to FIND patterns first
- Avoid reading entire directories into context

**Memory Management Rules:**
- Summarize findings after each major component
- Do NOT load all source files simultaneously
- Process large codebases in batches of 5-10 files
- Prioritize: config files → project files → key source → supporting files

### Database Detection

Scan the codebase to identify database technology:
- SQL Server indicators: connection strings, `SqlConnection`, `SqlCommand`
- Oracle indicators: `Oracle.DataAccess`, `Oracle.ManagedDataAccess`
- DB2 indicators: `IBM.Data.DB2`
- If commercial database detected, prominently recommend Aurora PostgreSQL for cost optimization

### Proprietary Dependency Analysis

For EVERY proprietary/commercial library found:
- Detailed compatibility assessment table
- Code migration examples (before/after)
- Specific mitigation options with effort levels

## Bundled MCP Server

This power includes the `fetch` MCP server (configured in `mcp-config.json`) to query package registry APIs for license verification.

**Note**: Ensure `uvx` is installed (via `uv` Python package manager). See [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Prerequisites

- Access to codebase (local or repository)
- Familiarity with source platform (.NET, WebSphere, or WebLogic)
- Understanding of modernization goals (cloud-native, containerization, etc.)
- Awareness of proprietary/commercial library dependencies

## Trigger Phrases

This power activates when users mention:
- "analyze this codebase"
- "modernization assessment"
- "migration feasibility"
- "legacy application"
- "AWS migration"
- "containerize app"
- "modernize to Spring Boot"
- "modernize to .NET 8"
- ".NET modernization"
- "WebSphere migration"
- "WebLogic migration"
- "J2EE modernization"

## Output

Generate report in `yymmddhhmm_MODERNIZATION_REPORT.md` following the structure defined in `steering/common/report-structure.md`. As for yymmddhhmm, it is the current time's year for yy, month for mm, day for dd, hour for hh and minutes for mm (UTC Timezone).

**CRITICAL:** The `steering/common/report-structure.md` file is the SINGLE SOURCE OF TRUTH for all report formatting, section structure, visualization standards, and quality requirements. Do NOT deviate from it.
