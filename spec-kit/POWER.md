---
name: "spec-kit"
displayName: "Spec-Driven Development"
description: "Complete SDD methodology power with 10 workflows: Steering, Specify, Clarify, Plan, Tasks, Implement, Analyze, Checklist, Sync, and Discover - transforming specifications into executable code"
keywords: ["specification", "SDD", "requirements", "planning", "implementation", "TDD", "code generation", "PRD", "user stories", "acceptance criteria", "steering", "specify", "clarify", "plan", "tasks", "implement", "analyze", "checklist", "sync", "discover", "reverse", "retrospective", "spec-kit", "speckit", "功能规格", "需求文档", "技术设计", "同步", "回顾", "逆向", "发现"]
author: "Kiro User"
---

# Spec-Driven Development Power

**CRITICAL - MANDATORY FIRST STEP**: You MUST read and load `steering/00-interaction-protocol.md` BEFORE proceeding with ANY other action. This is NON-NEGOTIABLE. Do NOT respond to users, do NOT start any workflow until you have loaded this file. Failure to load this file first is a violation of this power's protocol.

A comprehensive methodology power that guides you through the complete Spec-Driven Development (SDD) lifecycle - from project steering to implementation.

## Overview

**Spec-Driven Development inverts the traditional development paradigm**: Specifications don't serve code - code serves specifications.

This power embodies the SDD philosophy where:
- Specifications are the primary artifact
- Code is the generated output that serves the specification
- Natural language intent drives development
- Multi-step refinement over one-shot generation

## Core Principles

### The Power Inversion
Traditional development treats specifications as scaffolding - built and discarded once coding begins. SDD eliminates the gap between specification and implementation by making specifications executable.

### Executable Specifications
Specifications must be precise, complete, and unambiguous enough to generate working systems. The specification becomes the source of truth, with code as its expression.

### Steering Governance
Every project operates under steering files - guiding principles split into product, technology, and structure concerns, ensuring consistency, simplicity, and quality.

### Template-Driven Quality
Templates constrain AI behavior toward higher-quality specifications through:
- Preventing premature implementation details
- Forcing explicit uncertainty markers
- Structured thinking through checklists
- Steering compliance through gates

## Methodology Overview

### Phase 1: Foundation (Steering)
Establish guiding principles split into three files:
- **product.md** - Product vision, business constraints
- **tech.md** - Technology stack, development principles
- **structure.md** - Project layout, naming conventions

### Phase 2: Specification (Specify + Clarify)
Transform ideas into executable specifications:
- User stories with priorities
- Acceptance scenarios (Given-When-Then)
- Functional requirements
- Success criteria (measurable, technology-agnostic)

### Phase 3: Planning (Plan + Tasks)
Convert business requirements to technical architecture:
- Technology stack selection
- Data models and API contracts
- Task breakdown with dependencies
- Parallel execution markers

### Phase 4: Execution (Implement)
Execute tasks following the plan:
- Phase-by-phase execution
- TDD approach
- Progress tracking
- Validation checkpoints

### Phase 5: Quality (Analyze + Checklist)
Ensure consistency and completeness:
- Cross-artifact validation
- Coverage analysis
- Domain-specific quality checklists

### Phase 6: Retrospective (Sync)
Synchronize documentation with implementation:
- Compare planned vs actual implementation
- Update documentation to reflect reality
- Generate lessons learned and retrospective report
- Capture technical debt and recommendations

### Phase 0: Discovery (Discover) - For Existing Projects
Bootstrap SDD for existing codebases:
- Analyze existing code to extract product context
- Reverse engineer technology stack and patterns
- Generate steering files (product.md, tech.md, structure.md)
- Create comprehensive product specification

## Steering Files

Detailed methodologies for each workflow are available in the steering files:
- `00-interaction-protocol.md` - **MUST LOAD FIRST** - Interaction guidelines (mandatory before any action)
- `01-steering-workflow.md` - Project principles establishment
- `02-specify-workflow.md` - Feature specification creation
- `03-clarify-workflow.md` - Ambiguity elimination process
- `04-plan-workflow.md` - Technical planning workflow
- `05-tasks-workflow.md` - Task generation process
- `06-implement-workflow.md` - Implementation execution
- `07-analyze-workflow.md` - Consistency analysis
- `08-checklist-workflow.md` - Quality checklist generation
- `09-sync-workflow.md` - Documentation sync and retrospective
- `10-discover-workflow.md` - Project discovery and reverse engineering

Template files:
- `templates/requirements-template.md` - Feature requirements template
- `templates/clarifications-template.md` - Clarification log template
- `templates/design-template.md` - Technical design template
- `templates/tasks-template.md` - Task list template
- `templates/product-template.md` - Product steering template
- `templates/tech-template.md` - Technology steering template
- `templates/structure-template.md` - Structure steering template
- `templates/sync-report-template.md` - Sync report template
- `templates/product-spec-template.md` - Product specification template

## File Structure

All specification files are stored in `.kiro/specs/`:

```
.kiro/specs/
├── 000-product-spec/
│   └── product-spec.md      # Product specification (Discover workflow)
└── [###-feature-name]/
    ├── requirements.md      # Feature specification (Specify workflow)
    ├── clarifications.md    # Clarification Q&A log (Clarify workflow)
    ├── design.md            # Technical design (Plan workflow)
    ├── research.md          # Technology decisions
    ├── data-model.md        # Entity definitions
    ├── contracts/           # API specifications
    ├── quickstart.md        # Validation scenarios
    ├── tasks.md             # Task list (Tasks workflow)
    ├── checklists/          # Quality checklists
    └── sync-report.md       # Sync report (Sync workflow)
```
