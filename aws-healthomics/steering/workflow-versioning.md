# Workflow Versioning Guide

## Overview

When a customer is modifying an existing HealthOmics workflow, **always use `CreateAHOWorkflowVersion`** to create a new version rather than creating an entirely new workflow. This preserves workflow history, maintains consistent workflow IDs for downstream integrations, and follows AWS HealthOmics best practices.

## When to Use Workflow Versioning

**Use `CreateAHOWorkflowVersion` when:**
- Fixing bugs in an existing workflow
- Adding new features or tasks to a workflow
- Updating container images or versions
- Modifying resource allocations (CPU, memory)
- Changing workflow parameters or outputs
- Optimizing workflow performance after analyzing run metrics
- Applying fixes after diagnosing run failures

**Use `CreateAHOWorkflow` only when:**
- Creating a brand new workflow that doesn't exist yet
- The workflow represents fundamentally different functionality
- The customer explicitly requests a new workflow ID

## Workflow Modification Process

1. **Identify the existing workflow**
   - Use `ListAHOWorkflows` to find the workflow
   - Use `GetAHOWorkflow` to retrieve current workflow details including the workflow ID

2. **Make modifications locally**
   - Edit the workflow definition files
   - Use `LintAHOWorkflowDefinition` or `LintAHOWorkflowBundle` to validate changes

3. **Package the updated workflow**
   - Use `PackageAHOWorkflowDefinition` for single-file workflows
   - Use `PackageAHOWorkflowBundle` for multi-file workflows

4. **Create a new version**
   - Use `CreateAHOWorkflowVersion` with the existing workflow ID
   - Apply semantic versioning (e.g., `1.0.0` → `1.0.1` for patches, `1.1.0` for features)
   - Include a meaningful description of changes

5. **Verify the new version**
   - Use `GetAHOWorkflow` to confirm the version was created successfully
   - Check that the workflow status is `ACTIVE`

## Version Naming Conventions

Follow semantic versioning for workflow versions:
- **MAJOR.MINOR.PATCH** (e.g., `1.0.0`, `2.1.3`)
- **MAJOR**: Breaking changes to inputs/outputs
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, performance improvements

## Benefits of Versioning

- **Audit Trail**: Complete history of workflow changes
- **Rollback Capability**: Easy to revert to previous versions if issues arise
- **Consistent Integration**: Downstream systems can reference the same workflow ID
- **Cost Tracking**: All runs grouped under a single workflow for billing analysis
- **Compliance**: Maintains lineage for regulatory requirements in genomics workflows

## Common Scenarios

### After Diagnosing a Run Failure
When `DiagnoseAHORunFailure` identifies an issue:
1. Fix the workflow definition
2. Create a new version with `CreateAHOWorkflowVersion`
3. Re-run using the updated workflow version

### After Performance Optimization
When `AnalyzeAHORunPerformance` suggests improvements:
1. Apply recommended resource adjustments
2. Create a new version with `CreateAHOWorkflowVersion`
3. Run the optimized version to validate improvements

### Updating Container Images
When updating to newer container versions:
1. Update container references in task definitions
2. Test locally if possible
3. Create a new version with `CreateAHOWorkflowVersion`
