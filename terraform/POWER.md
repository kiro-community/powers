---
name: "terraform"
displayName: "Terraform"
description: "Build and manage infrastructure as code with Terraform - access registry providers, modules, policies, and HCP Terraform workspace management"
keywords: ["terraform", "hashicorp", "infrastructure", "iac", "hcp", "providers", "modules", "registry"]
author: "HashiCorp"
---

# Terraform Power

## Overview

Access Terraform Registry APIs and HCP Terraform for IaC development. Search provider docs, discover modules, manage workspaces, and execute runs.

**Key capabilities:**
- **Provider Documentation**: Search and retrieve docs for resources, data sources, functions
- **Module Discovery**: Find verified and community modules from the Registry
- **HCP Terraform**: Workspace management, runs, variables, private registry
- **Sentinel Policies**: Access governance and compliance policies

## Available Steering Files

- **getting-started** - Interactive setup guide for new projects
- **terraform-best-practices** - Coding conventions and patterns (auto-loads for .tf files)

## Available MCP Servers

### terraform
**Package:** `hashicorp/terraform-mcp-server` | **Connection:** Docker stdio

**Provider Tools:**

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `search_providers` | Find provider docs | `provider_name`, `provider_namespace`, `service_slug`, `provider_document_type` (resources/data-sources/guides/functions) |
| `get_provider_details` | Get full resource docs | `provider_doc_id` (from search_providers) |
| `get_provider_capabilities` | List provider features | `namespace`, `name` |
| `get_latest_provider_version` | Get latest version | `namespace`, `name` |

**Module Tools:**

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `search_modules` | Find modules | `module_query` |
| `get_module_details` | Get module docs | `module_id` (from search_modules) |
| `get_latest_module_version` | Get latest version | `module_publisher`, `module_name`, `module_provider` |

**Policy Tools:**

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `search_policies` | Find Sentinel policies | `policy_query` |
| `get_policy_details` | Get policy docs | `terraform_policy_id` (from search_policies) |

**HCP Terraform Tools** (require `TFE_TOKEN`):

| Tool | Purpose |
|------|---------|
| `list_terraform_orgs`, `list_terraform_projects` | List orgs/projects |
| `list_workspaces`, `get_workspace_details`, `create_workspace`, `update_workspace` | Workspace management |
| `list_runs`, `get_run_details`, `create_run`, `action_run` | Run management |
| `list_variable_sets`, `create_variable_set`, `list_workspace_variables`, `create_workspace_variable` | Variables |
| `search_private_modules`, `search_private_providers` | Private registry |

## Examples

```javascript
// 1. Search for S3 bucket resource docs
search_providers({
  "provider_name": "aws",
  "provider_namespace": "hashicorp",
  "service_slug": "s3_bucket",
  "provider_document_type": "resources"
})
// Returns: provider_doc_id like "10735923"

// 2. Get full documentation
get_provider_details({ "provider_doc_id": "10735923" })

// 3. Search for VPC modules
search_modules({ "module_query": "vpc" })
// Returns: module_id like "terraform-aws-modules/vpc/aws/6.5.1"

// 4. Get module details
get_module_details({ "module_id": "terraform-aws-modules/vpc/aws/6.5.1" })

// 5. Get latest provider version
get_latest_provider_version({ "namespace": "hashicorp", "name": "aws" })
```

## Workflow: Research → Write Config

```javascript
// Step 1: Search provider docs
const results = search_providers({
  "provider_name": "aws",
  "provider_namespace": "hashicorp", 
  "service_slug": "lambda_function",
  "provider_document_type": "resources"
})

// Step 2: Get detailed docs using provider_doc_id from results
const docs = get_provider_details({ "provider_doc_id": "..." })

// Step 3: Get version for constraint
const version = get_latest_provider_version({ "namespace": "hashicorp", "name": "aws" })

// Now write accurate Terraform config
```

## Configuration

**Prerequisites:** Docker installed and running

### Enabling HCP Terraform Features

By default, this power only includes Terraform Registry tools (providers, modules, policies). To enable HCP Terraform workspace management, runs, and variables, you need to configure your API token.

**Step 1:** Generate an API token from [HCP Terraform](https://app.terraform.io/app/settings/tokens) or your Terraform Enterprise instance.

**Step 2:** Update the `mcp.json` in this power to include your token:

```json
{
  "mcpServers": {
    "terraform": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "TFE_TOKEN",
        "hashicorp/terraform-mcp-server"
      ],
      "env": {
        "TFE_TOKEN": "your-api-token-here"
      },
      "disabled": false
    }
  }
}
```

### Terraform Enterprise (Custom Endpoint)

For organizations using Terraform Enterprise with a custom endpoint, add the `TFE_ADDRESS` environment variable:

```json
{
  "mcpServers": {
    "terraform": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "TFE_TOKEN",
        "-e", "TFE_ADDRESS",
        "hashicorp/terraform-mcp-server"
      ],
      "env": {
        "TFE_TOKEN": "your-api-token-here",
        "TFE_ADDRESS": "https://terraform.your-company.com"
      },
      "disabled": false
    }
  }
}
```

### Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `TFE_TOKEN` | HCP Terraform or Terraform Enterprise API token (required for workspace/run tools) |
| `TFE_ADDRESS` | Custom Terraform Enterprise URL (omit for HCP Terraform at `app.terraform.io`) |
| `ENABLE_TF_OPERATIONS` | Set to `true` to enable destructive operations (apply/destroy) |

## Best Practices

**Do:** Always `search_*` before `get_*_details`, pin versions, use modules, review plans

**Don't:** Hardcode credentials, skip plan review, use `auto_approve` blindly

## Troubleshooting

| Error | Solution |
|-------|----------|
| Provider/Module not found | Use `search_*` first to get valid IDs |
| Unauthorized | Set `TFE_TOKEN` env var |
| Docker not running | Start Docker daemon |

## Resources

[Terraform Docs](https://developer.hashicorp.com/terraform/docs) · [Registry](https://registry.terraform.io) · [HCP Terraform](https://app.terraform.io) · [MCP Server](https://github.com/hashicorp/terraform-mcp-server)

---

**Package:** `hashicorp/terraform-mcp-server` | **License:** MPL-2.0
