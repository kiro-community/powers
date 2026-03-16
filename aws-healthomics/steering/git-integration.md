# Git Integration for HealthOmics Workflows

## Overview

When a user provides a Git repository URL to create a HealthOmics workflow, **use the `definitionRepository` parameter** with `CreateAHOWorkflow` or `CreateAHOWorkflowVersion` instead of manually cloning, packaging, and uploading the workflow. This approach:
- Eliminates manual download, zip, and S3 staging steps
- Enables direct workflow creation from public or private repositories
- Supports GitHub, GitLab, and Bitbucket

## When to Use Git Integration

**Use `definitionRepository` when:**
- User provides a GitHub, GitLab, or Bitbucket repository URL
- User wants to create a workflow from a specific branch, tag, or commit
- User references a public workflow repository (e.g., nf-core pipelines)
- User wants to keep their workflow definition in source control

**Use traditional packaging when:**
- User has local workflow files not in a Git repository
- User provides an S3 URI for the workflow definition
- User explicitly requests local packaging

## Supported Git Providers

| Provider | Repository URL Format |
|----------|----------------------|
| GitHub | `https://github.com/owner/repo` |
| GitLab | `https://gitlab.com/owner/repo` |
| Bitbucket | `https://bitbucket.org/owner/repo` |
| GitLab Self-Managed | `https://gitlab.example.com/owner/repo` |
| GitHub Enterprise | `https://github.example.com/owner/repo` |

## Workflow for Git-Based Workflow Creation

### Step 1: Check for Existing Code Connections

Use `ListCodeConnections` to find existing connections for the Git provider:

```
ListCodeConnections(provider_type_filter="GitHub")  # or GitLab, Bitbucket, etc.
```

Look for a connection with status `AVAILABLE`. If found, use its `connection_arn`.

### Step 2: Create Code Connection (If Needed)

If no suitable connection exists:

1. **Create the connection:**
   ```
   CreateCodeConnection(
       connection_name="my-github-connection",
       provider_type="GitHub"  # GitHub, GitLab, Bitbucket, GitHubEnterpriseServer, GitLabSelfManaged
   )
   ```

2. **Inform the user** that they must complete OAuth authorization in the AWS Console:
   - The tool returns a `console_url` for completing authorization
   - Connection status will be `PENDING` until OAuth is completed
   - User must authorize the connection before it can be used

3. **Verify connection status:**
   ```
   GetCodeConnection(connection_arn="arn:aws:codeconnections:...")
   ```
   - Wait for status to become `AVAILABLE` before proceeding

### Step 3: Parse Repository Information

Extract from the user-provided URL:
- **fullRepositoryId**: `owner/repo` format (e.g., `nf-core/rnaseq`)
- **sourceReference**: Branch, tag, or commit
  - Type: `BRANCH`, `TAG`, or `COMMIT`
  - Value: The branch name, tag name, or commit SHA

### Step 4: Check for Container Registry Map

Before creating the workflow, check if the repository contains a container registry map file:
- Common locations: `container-registry-map.json`, `registry-map.json`, `.healthomics/container-registry-map.json`

**If a container registry map exists in the repository:**
- Pass `container_registry_map_uri` pointing to the S3 location if uploaded
- Or use `container_registry_map` parameter with the map contents

**If no container registry map exists:**
- Analyze the workflow definition for container references
- If containers reference public registries (Docker Hub, Quay.io, ECR Public):
  - Follow the [ECR Pull Through Cache](./ecr-pull-through-cache.md) steering guide
  - Use `CreateContainerRegistryMap` to generate a registry map
  - Use `ValidateHealthOmicsECRConfig` to verify ECR configuration
- If containers reference private ECR repositories:
  - Proceed without a container registry map (containers are already accessible)

### Step 5: Create the Workflow

Use `CreateAHOWorkflow` with the `definition_repository` parameter:

```
CreateAHOWorkflow(
    name="my-workflow",
    definition_repository={
        "connectionArn": "arn:aws:codeconnections:us-east-1:123456789012:connection/abc123",
        "fullRepositoryId": "owner/repo",
        "sourceReference": {
            "type": "BRANCH",  # or TAG, COMMIT
            "value": "main"   # branch name, tag, or commit SHA
        },
        "excludeFilePatterns": ["test/*", "docs/*"]  # optional
    },
    description="Workflow created from Git repository",
    parameter_template_path="parameters.json",  # optional: path within repo
    readme_path="README.md",  # optional: path within repo
    container_registry_map={...}  # if needed
)
```

### Step 6: Verify Workflow Creation

```
GetAHOWorkflow(workflow_id="1234567")
```

Check that:
- Status is `ACTIVE`
- Workflow type matches expected engine (WDL, NEXTFLOW, CWL)

## Parameter Reference

### definitionRepository Object

| Field | Required | Description |
|-------|----------|-------------|
| `connectionArn` | Yes | ARN of the CodeConnection to use |
| `fullRepositoryId` | Yes | Repository identifier in `owner/repo` format |
| `sourceReference.type` | Yes | `BRANCH`, `TAG`, or `COMMIT` |
| `sourceReference.value` | Yes | Branch name, tag name, or commit SHA |
| `excludeFilePatterns` | No | Glob patterns for files to exclude |

### Additional Parameters for Git Workflows

| Parameter | Description |
|-----------|-------------|
| `parameter_template_path` | Path to parameter template JSON within the repository |
| `readme_path` | Path to README markdown file within the repository |

## Common Scenarios

### Creating from nf-core Pipeline

```
# User: "Create a workflow from https://github.com/nf-core/rnaseq"

1. ListCodeConnections(provider_type_filter="GitHub")
2. If no connection: CreateCodeConnection(connection_name="github", provider_type="GitHub")
3. CreateAHOWorkflow(
       name="nf-core-rnaseq",
       definition_repository={
           "connectionArn": "...",
           "fullRepositoryId": "nf-core/rnaseq",
           "sourceReference": {"type": "TAG", "value": "3.14.0"}
       },
       container_registry_map={...}  # Use ECR pull-through cache mappings
   )
```

### Creating from Specific Branch

```
# User: "Create workflow from my-org/my-workflow on the develop branch"

CreateAHOWorkflow(
    name="my-workflow-dev",
    definition_repository={
        "connectionArn": "...",
        "fullRepositoryId": "my-org/my-workflow",
        "sourceReference": {"type": "BRANCH", "value": "develop"}
    }
)
```

### Creating from Specific Commit

```
# User: "Create workflow from commit abc123 in owner/repo"

CreateAHOWorkflow(
    name="my-workflow",
    definition_repository={
        "connectionArn": "...",
        "fullRepositoryId": "owner/repo",
        "sourceReference": {"type": "COMMIT", "value": "abc123def456"}
    }
)
```

## Error Handling

### Connection Not Available
If `GetCodeConnection` returns status `PENDING`:
- Remind user to complete OAuth authorization in AWS Console
- Provide the console URL from the connection creation response
- Wait for user confirmation before retrying

### Repository Access Denied
If workflow creation fails with access errors:
- Verify the connection has appropriate repository permissions
- For private repositories, ensure OAuth scope includes repo access
- Check that `fullRepositoryId` is correct

### Workflow Definition Not Found
If HealthOmics cannot find the workflow definition:
- Verify the repository contains a valid workflow file (main.wdl, main.nf, main.cwl)
- Check `excludeFilePatterns` isn't excluding the main workflow file
- Use `path_to_main` parameter if the main file isn't at the repository root

## Required IAM Permissions

Users need these permissions for Git integration:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "codeconnections:CreateConnection",
                "codeconnections:GetConnection",
                "codeconnections:ListConnections",
                "codeconnections:UseConnection"
            ],
            "Resource": "*"
        }
    ]
}
```

## References

- [AWS HealthOmics Git Integration Documentation](https://docs.aws.amazon.com/omics/latest/dev/workflows-git-integration.html)
- [CreateWorkflow API Reference](https://docs.aws.amazon.com/omics/latest/api/API_CreateWorkflow.html)
- [ECR Pull Through Cache Guide](./ecr-pull-through-cache.md)
