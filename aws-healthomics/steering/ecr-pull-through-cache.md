# AWS HealthOmics ECR Pullthrough and Container Registry Maps

## Overview

HealthOmics requires that containers used for workflow tasks come from PRIVATE ECR repositories with permissions correctly set to allow the HealthOmics service to access these containers. In many public workflow definitions it is common to use container images from public sources like Dockerhub, ECR Public Gallery, Quay.io, Seqera Wave etc. To use these containers they must either be cloned to an ECR private registry AND their URIs updated in the workflow definition - Or you can make use of ECR Pull Through Caches to automatically clone the images as well as Container Registry maps that translate the public image URI in the workflow definition to the ECR private URI in ECR. 


ECR Pull through cache setup and container registry mapping are two distinct but related concepts. If you setup pull through caches your
workflows will automatically pull containers from the upstream registries and cache them in your ECR repositories. You will reference these
containers using ECR private URIs in your workflow definitions. If you also add a container registry map (recommended) then you can use the original
public registry URIs in your workflow definitions and HealthOmics will automatically map them to your ECR private URIs. Container registry maps can be used to avoid changing all container URIs in the workflow.

**Key Concepts:**
- **ECR Pull-Through Cache**: Automatically pulls and caches containers from upstream registries. Workflows reference containers using ECR private URIs.
- **Container Registry Map**: Optional mapping that allows workflows to use original public registry URIs while HealthOmics automatically redirects to your ECR pull-through caches.

**When to use each approach:**
- **New workflows**: Use ECR pull-through caches with private ECR URIs (registry maps not needed)
- **Migrating existing workflows**: Use container registry maps to avoid changing container URIs in workflow definitions

## Prerequisites

- AWS credentials configured with appropriate IAM permissions for ECR and HealthOmics
- For Docker Hub: A Docker Hub access token (obtain from https://docs.docker.com/security/access-tokens/)

## MCP Tools Reference

This guide uses the following MCP tools from the `aws-healthomics` server:

| Tool | Purpose |
|------|---------|
| `ValidateHealthOmicsECRConfig` | Validate ECR configuration for HealthOmics |
| `ListPullThroughCacheRules` | List existing PTC rules with HealthOmics usability status |
| `CreatePullThroughCacheForHealthOmics` | Create PTC rules pre-configured for HealthOmics |
| `ListECRRepositories` | List available ECR private repositories with HealthOmics accessibility status |
| `CheckContainerAvailability` | Check if a container is available and accessible by HealthOmics |
| `CloneContainerToECR` | Clone containers to ECR with HealthOmics access permissions |
| `GrantHealthOmicsRepositoryAccess` | Grant HealthOmics access to an ECR repository |
| `CreateContainerRegistryMap` | Generate container registry maps for workflows |


## Regions
You should configure your ECR registry and HealthOmics workflows in the same region. If you will use multiple regions then repeat these steps in each region.

## Step 1: Validate Current ECR Configuration

Before making changes, validate your current ECR setup:

**Use `ValidateHealthOmicsECRConfig`** to check:
- Existing pull-through cache rules
- Registry permissions policy for HealthOmics
- Repository creation templates
- Required permissions for each prefix

The tool returns a list of issues with specific remediation steps.

---

## Step 2: Create Secrets for Authenticated Registries

Some registries require authentication. Create secrets in AWS Secrets Manager before creating pull-through cache rules.

**Docker Hub Secret** (required for Docker Hub):
```bash
aws secretsmanager create-secret \
    --name "ecr-pullthroughcache/docker-hub" \
    --description "Docker Hub credentials for ECR pull through cache" \
    --secret-string '{"username": "your-docker-username", "accessToken": "your-docker-access-token"}' \
    --region us-east-1
```

**Quay.io Secret** (only for private Quay repositories):
```bash
aws secretsmanager create-secret \
    --name "ecr-pullthroughcache/quay" \
    --description "Quay.io credentials for ECR pull through cache" \
    --secret-string '{"username": "your-quay-username", "accessToken": "your-quay-access-token"}' \
    --region us-east-1
```

---

## Step 3: Create Pull-Through Cache Rules

**Use `ListPullThroughCacheRules`** to see existing pull-through cache rules and their HealthOmics usability status. If there is already a valid cache for the upstream registry you need then you can re-use it and don't need to create another one.

**Use `CreatePullThroughCacheForHealthOmics`** to create pull-through cache rules that are automatically configured for HealthOmics. This tool:

1. Creates the pull-through cache rule
2. Updates the registry permissions policy to allow HealthOmics to create repositories and import images
3. Creates a repository creation template that grants HealthOmics image pull permissions

**Parameters:**
- `upstream_registry`: Registry type (`docker-hub`, `quay`, or `ecr-public`)
- `ecr_repository_prefix`: Optional custom prefix (defaults to registry type name)
- `credential_arn`: Optional Secrets Manager ARN (required for `docker-hub`)

**Example configurations:**

| Registry | upstream_registry | credential_arn | Notes |
|----------|------------------|----------------|-------|
| Docker Hub | `docker-hub` | Required | Use secret ARN from Step 2 |
| Quay.io | `quay` | Optional | Only needed for private repos |
| ECR Public | `ecr-public` | Not needed | Public access |

---

## Step 4: Verify Pull-Through Cache Configuration

**Use `ListPullThroughCacheRules`** to verify your pull-through cache rules are properly configured. The tool shows:

- All pull-through cache rules in the region
- HealthOmics usability status for each rule
- Missing permissions or configuration issues

A rule is usable by HealthOmics when:
1. Registry permissions policy grants HealthOmics required permissions
2. Repository creation template exists for the prefix
3. Template grants HealthOmics image pull permissions

---

## Step 5: Check Container Availability

Before running workflows, verify containers are accessible:

**Use `CheckContainerAvailability`** to check:
- Whether the container image exists in ECR
- Whether HealthOmics can access the image
- Pull-through cache status

**Parameters:**
- `repository_name`: ECR repository name (e.g., `docker-hub/library/ubuntu`)
- `image_tag`: Image tag (default: `latest`)
- `initiate_pull_through`: Set to `true` to trigger pull-through for missing images (recommended)

**Example repository names for pull-through caches:**
- Docker Hub official: `docker-hub/library/ubuntu`
- Docker Hub user: `docker-hub/broadinstitute/gatk`
- Quay.io: `quay/biocontainers/samtools`
- ECR Public: `ecr-public/lts/ubuntu`

---

## Step 6: Clone Containers (Alternative Approach)

If you need to copy containers without pull-through cache, or want to use containers from registries not supported by pull through cache such as Seqera Wave containers:

**Use `CloneContainerToECR`** to:
1. Parse source image references (handles Docker Hub shorthand)
2. Use existing pull-through cache rules when available
3. Grant HealthOmics access permissions automatically
4. Return the ECR URI and digest for workflow use

**Supported image reference formats:**
- `ubuntu:latest` → Docker Hub official image
- `myorg/myimage:v1` → Docker Hub user image
- `quay.io/biocontainers/samtools:1.17` → Quay.io image
- `public.ecr.aws/lts/ubuntu:22.04` → ECR Public image

Image URIs with hashes (e.g., `sha256:...`) are also supported by the tool.

---

## Step 7: Grant HealthOmics Access to Existing Repositories

To verify what repositories already exist and their accessiblity to HealthOmics:

**Use `ListECRRepositories`** to:
- List all ECR repositories in the region
- Check HealthOmics accessibility status for each repository
- Filter to show only HealthOmics-accessible repositories

For repositories not created through pull-through cache:

**Use `GrantHealthOmicsRepositoryAccess`** to add the required permissions to the repository:
- `ecr:BatchGetImage`
- `ecr:GetDownloadUrlForLayer`

The tool preserves existing repository policies while adding HealthOmics permissions.


**Parameters:**
- `filter_healthomics_accessible`: Set to `true` to only show accessible repositories

---


## Step 8: Create Container Registry Maps (Optional)

Container registry maps are useful when migrating existing workflows that reference public container URIs.

**Use `CreateContainerRegistryMap`** to generate a registry map that:
1. Discovers all HealthOmics-usable pull-through cache rules
2. Creates registry mappings for each discovered cache
3. Supports additional custom mappings and image overrides

**Parameters:**
- `include_pull_through_caches`: Auto-discover and include PTC rules (default: `true`)
- `additional_registry_mappings`: Custom registry mappings
- `image_mappings`: Specific image overrides (take precedence over registry mappings)

**Using the generated map:**
- Pass directly to `CreateAHOWorkflow` via `container_registry_map` parameter
- Or upload to S3 and reference via `container_registry_map_uri` parameter

**Example container registry map for common upstream registries**

The `ecrRepositoryPrefix` values in the registry map should match the `ecr_repository_prefix` values used when creating the pull-through cache rules.

```json
{
    "registryMappings": [
        {
          "upstreamRegistryUrl": "registry-1.docker.io",
          "ecrRepositoryPrefix": "docker-hub"
        },
        {
          "upstreamRegistryUrl": "quay.io",
          "ecrRepositoryPrefix": "quay"
        },
        {
          "upstreamRegistryUrl": "public.ecr.aws",
          "ecrRepositoryPrefix": "ecr-public"
        }
      ]
  }
```

**Example image mappings for specific overrides:**
```json
{
    "imageMappings": [
        {
            "sourceImage": "ubuntu",
            "destinationImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/docker-hub/library/ubuntu:20.04"
        },
        {
            "sourceImage": "quay.io/biocontainers/bwa:0.7.17",
            "destinationImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/quay/biocontainers/bwa:0.7.17"
        }
    ]
}
```

**Example combined mapping***

Registry mappings and image mappings can be combined. Image mappings will override any matching registry mapping.

In the following example, docker hub images will use the registry mapping except for the `ubuntu` image which will use the custom
mapping.

```json
{
    "registryMappings": [
        {
          "upstreamRegistryUrl": "registry-1.docker.io",
          "ecrRepositoryPrefix": "docker-hub"
        }
      ]
    }

    "imageMappings": [
        {
            "sourceImage": "ubuntu",
            "destinationImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/myrepo/library/ubuntu:20.04"
        }
    ]
```


---

## Step 9: Configure HealthOmics Service Role

The HealthOmics service role used during workflow runs must have ECR permissions. Add these permissions to your service role policy:

```json
{
    "Effect": "Allow",
    "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchCheckLayerAvailability"
    ],
    "Resource": [
        "arn:aws:ecr:us-east-1:123456789012:repository/docker-hub/*",
        "arn:aws:ecr:us-east-1:123456789012:repository/quay/*",
        "arn:aws:ecr:us-east-1:123456789012:repository/ecr-public/*"
    ]
}
```

Adjust the repository ARN patterns to match your pull-through cache prefixes.

---

## Quick Reference: Common Workflows

### New Workflow with Pull-Through Cache

1. `CreatePullThroughCacheForHealthOmics` - Create PTC rule for needed registries
2. `ValidateHealthOmicsECRConfig` - Verify configuration
3. Use ECR URIs in workflow (e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com/docker-hub/library/ubuntu:latest`) or use container registry mapping

### Migrate Existing Workflow

1. `CreatePullThroughCacheForHealthOmics` - Create required PTC rules
2. `CreateContainerRegistryMap` - Generate registry map
3. `CloneContainerToECR` - Clone any containers from registries not supported by pull-through caches
3. `CreateAHOWorkflow` with `container_registry_map` parameter

### Verify Container Access

1. `CheckContainerAvailability` with `initiate_pull_through: true`
2. `ListECRRepositories` with `filter_healthomics_accessible: true`

### Troubleshoot Access Issues

1. `ValidateHealthOmicsECRConfig` - Check for configuration issues
2. `ListPullThroughCacheRules` - Verify PTC rule status
3. `GrantHealthOmicsRepositoryAccess` - Fix repository permissions