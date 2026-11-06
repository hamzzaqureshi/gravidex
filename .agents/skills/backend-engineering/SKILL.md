---
name: backend-engineering
description: "Architect and build production backend services, APIs, and agent connectors. Covers REST API design, Express/Next.js API routes, robust error handling across TypeScript/Python/Go, and Model Context Protocol (MCP) server development. Use when building backend endpoints, designing data schemas, implementing typed error boundaries, or authoring MCP servers."
license: MIT
metadata:
  version: "1.0.0"
  type: curated-capability
  domains: [backend, api-design, error-handling, mcp-servers, rest]
  sources_count: 4
---

# Backend Engineering

Consolidated capability for architecting, implementing, and securing production backend services, RESTful APIs, typed error boundaries, and Model Context Protocol (MCP) tools.

## When to Activate
- Designing REST endpoints, resource URLs, status codes, pagination, and rate limits.
- Implementing Node.js, Express, Next.js API routes, or serverless functions.
- Designing error architectures (typed errors, error boundaries, retries, circuit breakers).
- Authoring or debugging Model Context Protocol (MCP) servers (tools, resources, prompts, stdio/SSE).

## When NOT to Activate
- Performing vulnerability reviews or penetration testing (use `security-audit`).
- Writing client-side React UI components (use `frontend-engineering`).

## Core Execution Workflow

1. **REST API Design & Standards:**
   - Use plural nouns for resources (`/api/v1/users`). Use standard status codes (200, 201, 400, 401, 403, 404, 409, 429, 500).
   - Enforce cursor-based or limit/offset pagination and standard response envelopes `{ data, error, meta }`.
   - Consult [references/rest-api-design.md](references/rest-api-design.md).

2. **Backend Architecture & Data Access:**
   - Encapsulate data access behind repositories. Validate all incoming request payloads at system boundaries with schema validators (Zod/Pydantic).
   - Consult [references/backend-patterns.md](references/backend-patterns.md).

3. **Robust Error Handling & Resilience:**
   - Distinguish operational errors from programmer errors.
   - Implement exponential backoff retries and circuit breakers for external API dependencies.
   - Consult [references/robust-error-handling.md](references/robust-error-handling.md).

4. **MCP Server Development:**
   - Build MCP servers with Node/TypeScript SDK. Define schema-validated tools, dynamic resources, and prompt templates.
   - Consult [references/mcp-server-development.md](references/mcp-server-development.md).

## Modular Reference Directory

| Reference Module | Primary Focus | Source Provenance |
|---|---|---|
| [rest-api-design.md](references/rest-api-design.md) | REST API patterns, status codes, pagination, filtering, versioning | `affaan-m/ECC` (`api-design`) |
| [backend-patterns.md](references/backend-patterns.md) | Node.js, Express, Next.js API routes, repository patterns, data access | `affaan-m/ECC` (`backend-patterns`) |
| [robust-error-handling.md](references/robust-error-handling.md) | Typed errors, error boundaries, retries, circuit breakers in TS/Python/Go | `affaan-m/ECC` (`error-handling`) |
| [mcp-server-development.md](references/mcp-server-development.md) | MCP SDK server development, tools, resources, prompts, Zod validation | `affaan-m/ECC` (`mcp-server-patterns`) |
