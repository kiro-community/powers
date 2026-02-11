---
inclusion: always
---

# Modernization Report Structure

This defines the standard report structure for ALL modernization analyses (.NET, WebLogic, WebSphere).

## CRITICAL RULES - READ FIRST

**This file is the SINGLE SOURCE OF TRUTH for report formatting. Follow these rules exactly:**

1. **NO dollar amounts by default** - Use qualitative levels (Low/Medium/High/Very High) for cost estimates
2. **DUAL TIMELINE COMPARISON REQUIRED** - Always show Traditional vs Agentic AI-Accelerated timelines side-by-side to demonstrate the value of AWS Transform and Kiro
3. **NO real dates** - Gantt charts use generic weeks (Week 1, Week 2, etc.) with `axisFormat Week %S` (uppercase S) and `tickInterval 2`
4. **NO file counts or line counts** - Solution Structure is simple
5. **NO Appendix section** - Report ends with Conclusion
6. **Professional Advisory Notice goes at TOP** - Before Executive Summary, not at the end
7. **Cost-Benefit Analysis compares PATHWAYS** - Current vs Pathway 1 vs Pathway 2 vs Pathway 3 (NOT by component like Database/Compute/Storage)
8. **Legends REQUIRED** - Every architecture diagram must have a color legend after it
9. **Gantt chart for 3-Year costs** - Use Mermaid Gantt as stacked horizontal bars (NOT line chart, NOT pie chart)
10. **NO "Quick Wins" section** - Implementation timeline is based on recommended pathway phases only
11. **Pathway Theme required** - Each pathway needs a 3-5 sentence theme paragraph
12. **Pros and Cons required** - Each pathway needs a pros/cons table
13. **Parallel tasks in Gantt** - Show concurrent tasks and dependencies clearly
14. **ABSOLUTELY NO ASCII ART** - ALL diagrams MUST use Mermaid.js syntax ONLY
15. **Visual dot indicators for scoring** - Use ●●●●●●●●●○ (9) format in Pathway Scoring Matrix
16. **OPTIONAL detailed pricing** - User can request 1,000 vCPU assumption with real AWS HK region pricing (see Section 9 Appendix)

---

## VISUALIZATION REQUIREMENTS - MERMAID ONLY

**⛔ ASCII ART IS STRICTLY FORBIDDEN ⛔**

ALL diagrams in this report MUST be Mermaid.js diagrams. ASCII art diagrams are NOT ACCEPTABLE and will cause the report to FAIL quality checks.

### FORBIDDEN - DO NOT USE:
```
❌ ASCII art boxes:
+------------------+
|   Component      |
+------------------+
        |
        v
+------------------+
|   Another        |
+------------------+

❌ ASCII arrows: -->, ===>, |---> 
❌ ASCII boxes: [____], +----+, |    |
❌ Text-based flow diagrams
❌ Any diagram made with +, -, |, or > characters
```

### REQUIRED - USE ONLY MERMAID:
```mermaid
graph TD
    A[Component] --> B[Another]
```

**RULE: If you find yourself typing `+`, `-`, `|`, or `>` characters to draw boxes or arrows, STOP IMMEDIATELY and use Mermaid.js instead.**

---

## Report Sections

### 1. Professional Advisory Notice (TOP OF REPORT)

MUST include this EXACT notice at the VERY TOP of the report, before Executive Summary:

> 📋 **Professional Advisory Notice**: This report provides a high-level technical analysis based on automated codebase scanning and should be interpreted in consultation with AWS Modernization Specialists or authorized AWS Modernization Partners. The findings and recommendations herein are intended to inform strategic planning discussions and should not be acted upon directly without professional guidance. Implementation effectiveness is influenced by numerous factors that cannot be extracted from the codebase alone, including organizational readiness, team dynamics, business constraints, regulatory requirements, and market conditions. We recommend engaging with qualified modernization experts to develop a comprehensive implementation strategy tailored to your specific organizational context.

---

### 2. Executive Summary

MUST include:

- **Strategic Verdict Table**:
  | Dimension | Assessment |
  |-----------|------------|
  | Overall Modernization Feasibility | ✅/⚠️/❌ **RATING (X/10)** |
  | 7 Rs Classification | **Classification** (with brief description) |
  | Gartner TIME Model | **Classification** |
  | Recommended Target | Target platform description |
  | Risk Level | **LEVEL** - Brief description |

- **Modernization Areas Summary Table** (high-level by area):
  | Area | Status | Complexity | Key Action |
  |------|--------|------------|------------|
  | Platform & Framework | ⚠️/✅/🔴 Needs Work/Good/Critical | Low/Medium/High | Brief action |
  | Architecture | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Dependencies | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Code Quality | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Data Layer | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Database | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Authentication | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Infrastructure | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | DevOps | ⚠️/✅/🔴 | Low/Medium/High | Brief action |
  | Cloud Integration | ⚠️/✅/🔴 | Low/Medium/High | Brief action |

- **Positive Indicators** (bullet list of what's already good)
- **Critical Blockers** (bullet list of what must change)

- **Risk of Inaction Table** (MUST include Impact rating AND Probability):
  | Risk Category | Impact | Probability | Business Consequence |
  |---------------|--------|-------------|---------------------|
  | Risk name | 🔴 High / 🟠 Medium / 🟡 Low | High/Medium/Low/Certain | Detailed consequence description |

### 3. Visual Architecture State

MUST include Mermaid.js diagrams with color coding:

#### Current Architecture (Color-Coded by Modernization Risk)

Show all layers with technologies, color-coded by risk:
- Use `style NodeName fill:#ff6b6b` for 🔴 Critical blockers (must modernize)
- Use `style NodeName fill:#ffa94d` for 🟠 Concerns (should modernize)
- Use `style NodeName fill:#69db7c` for 🟢 Already modern (no changes needed)

Include a legend after the diagram:
```
**Legend:**
- 🔴 Red: Critical blockers, must modernize
- 🟠 Orange: Concerns, should modernize  
- 🟢 Green: Already modern, no changes needed
```

#### Target Architecture

Show modernized stack with color coding:
- Use `style NodeName fill:#69db7c` for 🟢 Modernized components
- Use `style NodeName fill:#74c0fc` for 🔵 AWS managed services

Include a legend after the diagram:
```
**Legend:**
- 🟢 Green: Modernized components
- 🔵 Blue: AWS managed services
```

#### Project Dependency Graph

Show project dependencies with color coding based on migration status.

### 4. Critical Findings Matrix

| # | Issue | Evaluation Area | Impact | Impact If Not Modernized | Priority |
|---|-------|-----------------|--------|--------------------------|----------|
| 1 | Issue description | Area | 🔴 High / 🟠 Medium / 🟡 Low | Detailed consequence | P0/P1/P2/P3 |

Priority levels:
- P0: Critical blocker - must fix before migration
- P1: High priority - address in first phase
- P2: Medium priority - address in subsequent phases
- P3: Low priority - nice to have

MUST include 10+ findings.

### 5. Proprietary Dependency Analysis

Include license verification note:
> 📋 **License Verification**: Package licenses were verified via [NuGet.org/Maven Central/etc.] package metadata. All identified packages use permissive open-source licenses compatible with commercial use.

**Summary Table**:
| Library | Version | License | [.NET Core/8 / Java 17] Status | AWS/Linux Impact | Mitigation Strategy |
|---------|---------|---------|-------------------------------|------------------|---------------------|

For EACH significant proprietary library requiring migration, provide:
- **Detailed Analysis** section with:
  - Current usage description
  - Migration complexity assessment (Low/Medium/High)
  - Breaking changes to address (if applicable)
  - Code migration examples (before/after)
  - Mitigation options table:
    | Option | Effort | Recommendation |
    |--------|--------|----------------|

### 6. Database Analysis & Migration Opportunity

**Database Detection Summary**:
| Aspect | Finding |
|--------|---------|
| Database Technology | **Database name** (Edition, Version if known) |
| Connection String Location | Config file locations |
| Data Access Pattern | ORM / Raw SQL / Stored Procedures |
| Stored Procedures | Count (None detected = ✅) |
| Database-Specific Features | List of vendor-specific features |
| Provider | Provider name |

**Migration Section** (e.g., SQL Server → Aurora PostgreSQL):
- Why This Matters (bullet points on cost/benefits)
- Migration Complexity Assessment table:
  | Component | Complexity | Notes |
  |-----------|------------|-------|
- Code Migration Examples (before/after for connection strings, EF config, etc.)
- Data Type Mapping Reference table
- Recommended Migration Tools
- Impact If Not Migrated

### 7. Recommended Pathways

Generate exactly 3 distinct pathways.

#### Pathway Recommendation Scoring Framework

Each pathway is evaluated using a weighted scoring system across 6 key factors. The **Recommendation Score** is a weighted average that balances all factors for decision-making.

**Scoring Factors & Weights:**

| Factor | Weight | Description |
|--------|--------|-------------|
| Long-term Value | 25% | Cost savings, performance gains, future-proofing potential |
| Implementation Risk | 20% | Technical complexity, failure probability, rollback difficulty |
| Cost Efficiency | 20% | Infrastructure savings, licensing elimination, operational overhead reduction |
| Time to Value | 15% | How quickly benefits are realized after migration |
| Team Readiness | 10% | Skills availability, training requirements, learning curve |
| Business Continuity | 10% | Disruption to operations during migration, parallel running capability |

**Pathway Scoring Matrix:**

Use visual dot indicators to show scores. Format: `●●●●●●●●●○ (9)` where filled dots = score, empty dots = remaining to 10.

| Factor (Weight) | Pathway 1: Full Modernization | Pathway 2: Lift & Optimize | Pathway 3: Containerize Only |
|-----------------|-------------------------------|---------------------------|------------------------------|
| Long-term Value (25%) | ●●●●●●●●●○ (9) | ●●●●●●○○○○ (6) | ●●●○○○○○○○ (3) |
| Implementation Risk (20%) | ●●●●●●○○○○ (6) | ●●●●●●●○○○ (7) | ●●●●●●●●●○ (9) |
| Cost Efficiency (20%) | ●●●●●●●●●○ (9) | ●●●●●○○○○○ (5) | ●●●○○○○○○○ (3) |
| Time to Value (15%) | ●●●●●○○○○○ (5) | ●●●●●●●○○○ (7) | ●●●●●●●●●○ (9) |
| Team Readiness (10%) | ●●●●●●○○○○ (6) | ●●●●●●●○○○ (7) | ●●●●●●●●●○ (9) |
| Business Continuity (10%) | ●●●●●●●○○○ (7) | ●●●●●●●●○○ (8) | ●●●●●●●●●○ (9) |
| **Recommendation Score** | **7.4/10** | **6.4/10** | **5.4/10** |

> 📋 **Scoring Note**: Higher scores are better for all factors. Implementation Risk is scored inversely (10 = lowest risk, 1 = highest risk). The Recommendation Score is calculated as the weighted average of all factors. Pathway 1 excels in long-term value and cost efficiency but requires more effort. Pathway 3 scores high on ease factors but low on value factors.

**Pathway Comparison Matrix** (Mermaid quadrantChart):
```mermaid
quadrantChart
    title Modernization Pathway Comparison
    x-axis Low Effort --> High Effort
    y-axis Low Value --> High Value
    quadrant-1 Strategic Wins
    quadrant-2 Quick Wins
    quadrant-3 Low Priority
    quadrant-4 Major Projects
    "Pathway 1: Name": [x, y]
    "Pathway 2: Name": [x, y]
    "Pathway 3: Name": [x, y]
```

---

For each pathway:

**Pathway N: [Name] (Recommendation Score: X.X/10)** - ✅ RECOMMENDED / ❌ NOT RECOMMENDED

- **7 Rs Classification:** Classification (with brief description)
- **Gartner TIME:** Classification

**Pathway Theme:**
A paragraph (3-5 sentences) describing the overall philosophy and approach of this pathway. Explain what makes this pathway unique, who it's best suited for, and the key trade-offs involved. This should help stakeholders quickly understand the essence of the pathway without reading all the details.

**Strategy Overview:**
Brief description of the approach.

**Migration Roadmap** (Mermaid flowchart with phases):
```mermaid
flowchart LR
    subgraph Phase1["Phase 1: Name"]
        A1[Task 1]
        A2[Task 2]
    end
    
    subgraph Phase2["Phase 2: Name"]
        B1[Task 1]
    end
    
    Phase1 --> Phase2
    
    style Phase1 fill:#color
    style Phase2 fill:#color
```

**Effort Breakdown** (NO time estimates, use relative sequencing):
| Phase | Complexity | Relative Sequence | Key Deliverables |
|-------|------------|-------------------|------------------|
| Phase 1: Name | Low/Medium/High | First | Deliverables |
| Phase 2: Name | Low/Medium/High | Second | Deliverables |

**Pros and Cons:**

| Pros | Cons |
|------|------|
| ✅ Benefit 1 | ❌ Drawback 1 |
| ✅ Benefit 2 | ❌ Drawback 2 |
| ✅ Benefit 3 | ❌ Drawback 3 |

**Risk Assessment:**
- Technical Risk: Level (description)
- Business Risk: Level (description)
- Rollback Capability: Level (description)

**When to Choose This Path:**
- Bullet points on when this pathway is appropriate

---

### 8. Next Steps: Recommended Pathway Implementation

This section details the implementation plan for the **recommended pathway** identified in Section 7. Do NOT include a separate "Quick Wins" section - all implementation details should be based on the recommended pathway phases.

#### Implementation Roadmap

> ⚠️ **Timeline Disclaimer**: The timeline shown in this roadmap is for **indicative conceptual visualization only** and does not represent a precise estimation. Actual timelines can vary significantly based on factors including modernization team experience, project priorities, resource allocation, organizational change management processes, testing requirements, and third-party dependencies.

Use generic week numbers (Week 1, Week 2, etc.) - NO real dates. The Gantt chart MUST show:
- Tasks from the recommended pathway phases
- Parallel execution where tasks can run concurrently
- Dependencies between tasks (stacked/sequential where required)
- Clear visualization of which tasks block others

**CRITICAL: Use explicit start/end positions, NOT `after` syntax.** The `after` keyword does not render correctly with `dateFormat X`. Always use `:taskId, startWeek, endWeek` format.

**CRITICAL: Use `axisFormat Week %S` (uppercase S), NOT `%s` (lowercase).** Lowercase `%s` causes axis label rendering issues. Always include `tickInterval 2` to prevent label crowding.

```mermaid
gantt
    title Recommended Pathway Implementation (Indicative Timeline)
    dateFormat X
    axisFormat Week %S
    tickInterval 2
    
    section Phase 1: [Name]
    Task 1 (Foundation)           :a1, 0, 2
    Task 2 (Can run parallel)     :a2, 0, 2
    Task 3 (Depends on Task 1)    :a3, 2, 3
    
    section Phase 2: [Name]
    Task 4 (Depends on Phase 1)   :b1, 3, 6
    Task 5 (Parallel with Task 4) :b2, 3, 5
    Task 6 (Depends on Task 4)    :b3, 6, 8
    
    section Phase 3: [Name]
    Task 7 (Depends on Phase 2)   :c1, 8, 10
    Task 8 (Parallel with Task 7) :c2, 8, 11
```

**Gantt Chart Syntax Rules:**
- **MUST use `axisFormat Week %S`** (uppercase S) — lowercase `%s` causes overlapping/garbled axis labels
- **MUST include `tickInterval 2`** to prevent x-axis label crowding
- Format: `:taskId, startWeek, endWeek` (e.g., `:a1, 0, 2` means Week 0 to Week 2)
- Parallel tasks: Same start week (e.g., `:a1, 0, 2` and `:a2, 0, 2`)
- Sequential tasks: Next task starts where previous ends (e.g., `:a3, 2, 3` follows `:a1, 0, 2`)
- **DO NOT use `after` keyword** - it doesn't render correctly with numeric date format

**Key:** Tasks with the same start week run in parallel. Sequential dependencies are shown by starting a task at the end week of its predecessor.

#### Phase Breakdown

Detail each phase from the recommended pathway:

| Phase | Key Activities | Complexity | Dependencies | Key Deliverables |
|-------|---------------|------------|--------------|------------------|
| Phase 1: [Name] | Activity list | Low/Medium/High | Prerequisites | Deliverables |
| Phase 2: [Name] | Activity list | Low/Medium/High | Phase 1 completion | Deliverables |
| Phase 3: [Name] | Activity list | Low/Medium/High | Phase 2 completion | Deliverables |

NO effort estimates in hours/days/weeks.

#### Immediate Actions

| Action | Owner | Complexity | Impact |
|--------|-------|------------|--------|
| Action description | Team/Role | Low/Medium/High | Impact description |

#### Decision Points & Dependencies

Mermaid flowchart showing decision flow and dependencies for the recommended pathway.

#### Timeline Comparison: Traditional vs Agentic AI-Accelerated

**ALWAYS include both timelines to demonstrate the value of AWS Transform and Kiro:**

##### Why Agentic AI Dramatically Reduces Timeline

| Task Category | Traditional Approach | With AWS Transform + Kiro | Acceleration Factor |
|---------------|---------------------|---------------------------|---------------------|
| Code Analysis | Manual review, days | Automated scanning, minutes | 100x+ |
| Framework Migration | Line-by-line rewrite, weeks | AWS Transform auto-conversion, hours | 50x+ |
| EF6 → EF Core | Manual refactoring, weeks | AWS Transform patterns, hours | 40x+ |
| Controller Migration | Manual per controller, days | Kiro batch migration, minutes | 100x+ |
| View Updates | Manual per view, days | Kiro pattern application, hours | 20x+ |
| Dockerfile Creation | Manual research + writing | Kiro generation, minutes | 50x+ |
| Test Generation | Manual writing, weeks | Kiro auto-generation, hours | 30x+ |

##### Dual Timeline Gantt Charts

**Traditional Approach (Without GenAI Tools):**
```mermaid
gantt
    title Traditional Migration Timeline
    dateFormat X
    axisFormat Week %S
    tickInterval 2
    
    section Analysis
    Manual code review           :a1, 0, 2
    Dependency analysis          :a2, 2, 3
    
    section Framework Migration
    Create .NET 8 projects       :b1, 3, 4
    Manual code conversion       :b2, 4, 10
    EF6 to EF Core (manual)      :b3, 10, 14
    
    section Web Layer
    Controller migration         :c1, 14, 18
    View updates                 :c2, 18, 21
    Auth migration               :c3, 21, 23
    
    section Database
    Schema conversion            :d1, 14, 16
    Data migration               :d2, 23, 25
    
    section Testing & Deploy
    Integration testing          :e1, 25, 28
    Performance testing          :e2, 28, 30
    Production cutover           :e3, 30, 32
```

**Agentic AI-Accelerated (With AWS Transform + Kiro):**
```mermaid
gantt
    title Agentic AI-Accelerated Timeline
    dateFormat X
    axisFormat Week %S
    tickInterval 1
    
    section Phase 1: Foundation
    AWS Transform analysis       :a1, 0, 0.5
    Auto-scaffold .NET 8         :a2, 0, 0.5
    Domain + Data migration      :a3, 0.5, 1
    
    section Phase 2: Parallel Migration
    EF Core (AWS Transform)      :b1, 1, 2
    Controllers (Kiro)           :b2, 1, 2
    Views (Kiro)                 :b3, 1, 2
    Aurora + SCT                 :b4, 1, 2
    
    section Phase 3: Integration
    Auth + DMS                   :c1, 2, 3
    Containerization (Kiro)      :c2, 2, 3
    
    section Phase 4: Validate
    AI-assisted testing          :d1, 3, 4
    Human review + fixes         :d2, 4, 5
    Production cutover           :d3, 5, 6
```

##### Timeline Comparison Summary

| Metric | Traditional | Agentic AI-Accelerated | Reduction |
|--------|-------------|------------------------|-----------|
| Total Duration | ~32 weeks | ~6 weeks | **81% faster** |
| Manual Coding Effort | Very High | Low (review-focused) | **~80% less** |
| Human Role | Write code | Review + validate | Shifted |
| Parallelization | Limited | Massive | Enabled by AI |
| Risk of Errors | Higher | Lower (consistent patterns) | Reduced |

> 📋 **Key Insight**: AWS Transform automates 70-80% of code conversion. Kiro handles repetitive migrations in parallel. Human effort shifts from writing code to reviewing AI-generated output. The bottleneck becomes testing and validation, not coding.

#### Recommended Tool Support (Automation Impact)

| Tool | Purpose | Automation Level | Time Savings |
|------|---------|------------------|--------------|
| AWS Transform for Windows Full Stack | End-to-end .NET + DB migration | 70-80% automated | Weeks → Days |
| AWS Transform for .NET | Framework + EF migration | 60-70% automated | Weeks → Days |
| Kiro | Code migration, refactoring, test generation | 80-90% automated | Days → Hours |
| AWS Schema Conversion Tool | Schema analysis + conversion | 90% automated | Days → Hours |
| AWS Database Migration Service | Data migration | 95% automated | Days → Hours |

> 📋 **Automation Reality**: With these tools, the migration work shifts from "writing code" to "reviewing and validating AI-generated code." A skilled team can review and approve changes much faster than writing from scratch.

Note: For .NET modernization, prefer AWS Transform for Windows Full Stack when both application and database migration are needed. Use individual tools (SCT, DMS, App2Container) only for specific scenarios or when Transform doesn't cover the use case.

### 9. Cost-Benefit Analysis

**CRITICAL: This section compares costs BY PATHWAY (Current vs Pathway 1 vs Pathway 2 vs Pathway 3), NOT by component (Database/Compute/Storage). Do NOT create charts showing cost by component.**

#### 3-Year Cost Comparison (Qualitative)

Use qualitative levels (Low/Medium/High/Very High) - NO dollar amounts by default:

| Cost Factor | Current | Pathway 1 | Pathway 2 | Pathway 3 |
|-------------|---------|-----------|-----------|-----------|
| Compute | Baseline | Low | Medium | High |
| Database | Baseline | Low | High | High |
| Licensing | High | None | Medium | High |
| Migration Effort | N/A | High | Medium | Low |
| Operational Overhead | High | Low | Medium | High |
| **Overall Recurring** | Baseline | **60-70% savings** | **30-40% savings** | **~0% savings** |

#### 3-Year Cost Visualization

Use a Mermaid Gantt chart to create stacked horizontal bars showing relative year-by-year costs:

**CRITICAL: Bars must be stacked, NOT starting from zero.** Each bar's start position must equal the previous bar's end position within the same section. This creates a visual stacking effect where Year 2 begins where Year 1 ends, and Year 3 begins where Year 2 ends.

✅ **CORRECT** (stacked — each bar starts where previous ends):
```
Year 1 - 45     :active, 0, 45
Year 2 - 25     :crit, 45, 70
Year 3 - 25     :70, 95
```

❌ **WRONG** (all bars start from 0 — not stacked):
```
Year 1 - 45     :active, 0, 45
Year 2 - 25     :crit, 0, 25
Year 3 - 25     :0, 25
```

```mermaid
gantt
    title 3-Year Relative Cost Comparison (Baseline = 100)
    dateFormat X
    axisFormat %s
    todayMarker off

    section Current (300)
    Year 1 - 100    :active, 0, 100
    Year 2 - 100    :crit, 100, 200
    Year 3 - 100    :200, 300

    section Pathway 1 (~100)
    Year 1 - 45     :active, 0, 45
    Year 2 - 25     :crit, 45, 70
    Year 3 - 25     :70, 95

    section Pathway 2 (~180)
    Year 1 - 70     :active, 0, 70
    Year 2 - 55     :crit, 70, 125
    Year 3 - 55     :125, 180

    section Pathway 3 (~305)
    Year 1 - 105    :active, 0, 105
    Year 2 - 100    :crit, 105, 205
    Year 3 - 100    :205, 305
```

**CRITICAL for 3-Year Cost Chart:** This chart uses `axisFormat %s` (lowercase) because the x-axis represents cost units (0-300+), NOT weeks. Do NOT use `%S` (uppercase) here — it caps at 59 and wraps. The stacking is achieved by chaining bar positions: Year 2 starts where Year 1 ends, Year 3 starts where Year 2 ends. Each bar within a section MUST start from the end of the previous bar, NOT from 0.

**Legend:** 🔵 Year 1 (active = blue) | 🔴 Year 2 (crit = red) | 🩵 Year 3 (no status = teal/cyan) — X-axis: Relative cost units (Current annual = 100). Bar length represents cumulative 3-year cost.

**Gantt Chart Color Reference:**
- `active` = blue
- `crit` = red
- (no status) = teal/cyan

#### Key Cost Drivers

| Driver | Impact | Pathway 1 | Pathway 2 | Pathway 3 |
|--------|--------|-----------|-----------|-----------|
| Database Licensing | Very High | ✅ Eliminated | ❌ Retained | ❌ Retained |
| OS Licensing | High | ✅ Eliminated | ✅ Eliminated | ❌ Retained |
| Graviton ARM64 | Medium | ✅ 20% savings | ❌ Not available | ❌ Not available |
| Serverless DB | Medium | ✅ Auto-scaling | ❌ Not used | ❌ Not used |

#### ROI Summary

| Metric | Pathway 1 | Pathway 2 | Pathway 3 |
|--------|-----------|-----------|-----------|
| Investment Level | High | Medium | Low |
| Returns Potential | Very High | Medium | None |
| Payback Period | Short-term (months) | Short-term (months) | N/A |
| Risk-Adjusted Value | High | Medium | Low |

**Key Value Drivers:**
- Pathway 1: Maximum savings from eliminating all licensing costs + Graviton compute
- Pathway 2: Moderate savings from OS license elimination only
- Pathway 3: No recurring savings; only operational benefits

#### Cost Optimization Opportunities

| Optimization | Potential Additional Savings |
|--------------|------------------------------|
| Compute Savings Plans (1-year) | Up to 17% |
| Compute Savings Plans (3-year) | Up to 52% |
| Reserved Capacity | Up to 35% on databases |
| Spot Instances | Up to 70% on eligible tasks |
| Right-sizing | 10-30% typical |

---

### OPTIONAL: Detailed Cost Simulation (1,000 vCPU Assumption)

> 📋 **User Request Required**: This section is ONLY included if the user explicitly requests detailed cost calculations. Ask: *"Would you like me to include a detailed cost simulation based on 1,000 vCPUs with real AWS Hong Kong region pricing?"*

If requested, include the following detailed analysis:

#### Baseline Assumption

> 📋 **Baseline Assumption**: This analysis assumes a production workload of **1,000 vCPUs** running continuously (24/7/365) in **Asia Pacific (Hong Kong)** region. All prices are based on on-demand pricing as of January 2025. Actual costs may vary based on Reserved Instance commitments, Savings Plans, and usage patterns.

#### Pricing Reference Sources

| Service | Pricing Source |
|---------|---------------|
| ECS Fargate | [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/) |
| RDS SQL Server | [AWS RDS SQL Server Pricing](https://aws.amazon.com/rds/sqlserver/pricing/) |
| Aurora PostgreSQL | [AWS Aurora Pricing](https://aws.amazon.com/rds/aurora/pricing/) |

#### Compute Pricing Breakdown (per vCPU-hour, HK Region)

| Platform | vCPU/hour | Memory/GB/hour | OS License/vCPU/hour | Total/vCPU/hour (with 2GB RAM) |
|----------|-----------|----------------|---------------------|-------------------------------|
| Fargate Linux/x86 | $0.0XXX | $0.00XXX | — | **$0.0XXX** |
| Fargate Linux/ARM (Graviton) | $0.0XXX | $0.00XXX | — | **$0.0XXX** |
| Fargate Windows/x86 | $0.0XXX | $0.0XXX | $0.0XX | **$0.1XXX** |

#### Database Pricing Breakdown (HK Region)

| Database | Instance/Capacity | Hourly Cost | Monthly Cost (730 hrs) | Notes |
|----------|-------------------|-------------|------------------------|-------|
| RDS SQL Server Standard (Multi-AZ) | db.m5.2xlarge | ~$X.XX/hr | ~$X,XXX | License included |
| Aurora PostgreSQL Serverless v2 | Per ACU | $0.XX/ACU-hour | $XX.XX/ACU | 1 ACU ≈ 2GB RAM |

> 📋 **Database Sizing Rationale**: For a typical web application, database compute is commonly 5-10% of application tier capacity. For 1,000 app vCPUs, 2 × db.m5.2xlarge (16 vCPU total) or 16 ACU Aurora is reasonable.

#### Detailed Cost Model per Pathway

**Current State:**
| Cost Component | Calculation | Monthly Cost | Annual Cost |
|----------------|-------------|--------------|-------------|
| Fargate Windows Compute | 1,000 vCPU × $X.XX/hr × 730 hrs | $XX,XXX | $XXX,XXX |
| Fargate Windows Memory | 2,000 GB × $X.XX/hr × 730 hrs | $XX,XXX | $XXX,XXX |
| Windows OS License | 1,000 vCPU × $X.XX/hr × 730 hrs | $XX,XXX | $XXX,XXX |
| RDS SQL Server (Multi-AZ) | 2 × db.m5.2xlarge × $X.XX/hr × 730 hrs | $X,XXX | $XXX,XXX |
| **Total Current State** | | **$XXX,XXX** | **$X,XXX,XXX** |

**Pathway 1 (Full Modernization):**
| Cost Component | Calculation | Monthly Cost | Annual Cost |
|----------------|-------------|--------------|-------------|
| Fargate Graviton Compute | 1,000 vCPU × $X.XX/hr × 730 hrs | $XX,XXX | $XXX,XXX |
| Fargate Graviton Memory | 2,000 GB × $X.XX/hr × 730 hrs | $X,XXX | $XX,XXX |
| Aurora PostgreSQL Serverless v2 | 16 ACU × $X.XX/hr × 730 hrs | $X,XXX | $XX,XXX |
| **Total Pathway 1 Recurring** | | **$XX,XXX** | **$XXX,XXX** |

**One-Time Migration Costs:**

| Migration Component | Internal Team | Professional Services | Tooling/Infra | Total |
|--------------------|---------------|----------------------|---------------|-------|
| Framework Migration | $XX,XXX | $XX,XXX | $XX,XXX | $XXX,XXX |
| Database Migration | $XX,XXX | $XX,XXX | $X,XXX | $XX,XXX |
| Testing & Validation | $XX,XXX | $XX,XXX | $XX,XXX | $XX,XXX |
| Training | $X,XXX | $XX,XXX | — | $XX,XXX |
| **Total One-Time** | **$XX,XXX** | **$XXX,XXX** | **$XX,XXX** | **$XXX,XXX** |

#### 3-Year TCO Comparison (Detailed)

| Pathway | Year 1 | Year 2 | Year 3 | 3-Year Total | vs Current |
|---------|--------|--------|--------|--------------|------------|
| **Current** | $X.XXM | $X.XXM | $X.XXM | **$X.XXM** | — |
| **Pathway 1** | $X.XXM | $X.XXM | $X.XXM | **$X.XXM** | **-XX%** |
| **Pathway 2** | $X.XXM | $X.XXM | $X.XXM | **$X.XXM** | **-XX%** |
| **Pathway 3** | $X.XXM | $X.XXM | $X.XXM | **$X.XXM** | **-X%** |

#### ROI Analysis (Detailed)

| Metric | Pathway 1 | Pathway 2 | Pathway 3 |
|--------|-----------|-----------|-----------|
| One-Time Investment | $XXX,XXX | $XXX,XXX | $XX,XXX |
| Annual Savings | $X,XXX,XXX | $XXX,XXX | $0 |
| Payback Period | **~X.X months** | **~X.X months** | N/A |
| 3-Year Net Savings | **$X,XXX,XXX** | **$X,XXX,XXX** | **-$XX,XXX** |
| 3-Year ROI | **X,XXX%** | **X,XXX%** | **-100%** |

> 📋 **Sources**: Pricing data sourced from AWS official pricing pages (January 2025). See linked URLs for current rates.

---

### 10. Solution Structure Summary

Simple table showing projects and migration complexity - NO file counts or line counts:

| Project | Current Framework | Target Framework | Migration Complexity |
|---------|------------------|------------------|---------------------|
| Project.Name | Current version | Target version | Low/Medium/High/None |

### 11. Conclusion

Brief summary including:
- Overall assessment statement with feasibility score
- Recommended pathway with key benefits
- Key success factors (bullet list)

---

*Report generated by [Platform] Modernization Analyzer Power*
*Analysis Date: [Date]*

## Visualization Standards

### Mermaid Diagram Types to Use

1. **Architecture Diagrams**: `graph TB` or `graph LR` with color-coded styles
2. **Dependency Graphs**: `graph TD` with color-coded styles
3. **Flowcharts**: `flowchart LR` or `flowchart TB` with subgraphs for phases
4. **Quadrant Charts**: `quadrantChart` for pathway comparison
5. **Gantt Charts**: `gantt` for both implementation timelines (dateFormat X, axisFormat Week %S, tickInterval 2) AND 3-year cost visualization (as horizontal stacked bars). **MUST use uppercase %S, NOT lowercase %s.**

### Color Coding Standards

Architecture diagrams:
- `fill:#ff6b6b` - Red: Critical blockers
- `fill:#ffa94d` - Orange: Concerns
- `fill:#69db7c` - Green: Modern/good
- `fill:#74c0fc` - Blue: AWS managed services
- `fill:#ffd43b` - Yellow: In progress/transitional

### Diagram Best Practices

- Use clear, descriptive labels
- Include legends for color coding
- Show clear boundaries between components
- Annotate with technology decisions
- Keep diagrams readable (not too complex)

## Quality Checklist

Before completing the report, verify:

**VISUALIZATION (CRITICAL):**
- [ ] ⛔ NO ASCII ART ANYWHERE - All diagrams use Mermaid.js ONLY (no +, -, |, > box drawings)
- [ ] At least 6 different Mermaid diagram types included
- [ ] Current Architecture diagram has color coding with legend
- [ ] Target Architecture diagram has color coding with legend

**STRUCTURE:**
- [ ] Professional Advisory Notice at TOP of report (before Executive Summary)
- [ ] Executive Summary includes feasibility score (X/10), 7Rs, Gartner TIME
- [ ] Risk of Inaction has Impact rating (High/Medium/Low) AND Probability columns
- [ ] All proprietary dependencies analyzed with migration examples
- [ ] Database technology detected and documented
- [ ] Critical Findings Matrix has 10+ findings

**PATHWAYS:**
- [ ] Exactly 3 pathways with full detail
- [ ] Pathway Scoring Matrix uses visual dot indicators: ●●●●●●●●●○ (9) format
- [ ] Scoring Note explains the weighted average calculation
- [ ] Each pathway has a "Recommendation Score" (weighted average, X.X/10)
- [ ] Each pathway has a "Pathway Theme" paragraph (3-5 sentences)
- [ ] Each pathway has a "Pros and Cons" table
- [ ] Pathway with highest Recommendation Score is marked ✅ RECOMMENDED

**NEXT STEPS:**
- [ ] NO "Quick Wins" section - implementation is based on recommended pathway only
- [ ] Next Steps section focuses on recommended pathway implementation
- [ ] Implementation Roadmap Gantt shows parallel tasks and dependencies
- [ ] Gantt chart has timeline disclaimer
- [ ] Gantt chart uses generic weeks (no real dates)

**TIMELINE COMPARISON:**
- [ ] BOTH Traditional and Agentic AI-Accelerated timelines shown
- [ ] Timeline comparison table with reduction percentages
- [ ] Tool automation levels documented with time savings
- [ ] Human role clearly defined as "review + validate" not "write"
- [ ] Acceleration factors table included

**COST-BENEFIT:**
- [ ] 3-Year Cost Comparison table uses qualitative levels (Low/Medium/High) by default
- [ ] 3-Year Cost Visualization uses Mermaid GANTT chart as stacked horizontal bars with RELATIVE units
- [ ] Gantt chart legend explains colors: 🔵 Year 1 (active) | 🔴 Year 2 (crit) | 🩵 Year 3 (no status)
- [ ] Key Cost Drivers table shows which costs are eliminated/retained per pathway
- [ ] ROI Summary uses qualitative assessments (High/Medium/Low, Short-term/Long-term)
- [ ] Cost Optimization Opportunities table included
- [ ] OPTIONAL: If user requests detailed pricing, include 1,000 vCPU simulation with HK region pricing

**FORBIDDEN:**
- [ ] NO dollar amounts in default Cost-Benefit section (use qualitative levels)
- [ ] NO effort estimates in hours/days/weeks
- [ ] NO file counts or line counts
- [ ] NO Appendix section (except optional detailed pricing if requested)
- [ ] NO ASCII art diagrams
- [ ] NO line charts or pie charts for cost visualization (use Gantt as horizontal bars)
- [ ] NO radar charts (use visual dot matrix instead)

**FINAL:**
- [ ] Solution Structure Summary is simple (no file/line counts)
- [ ] Conclusion section present
