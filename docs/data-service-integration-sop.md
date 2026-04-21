# Data Service Integration SOP For Heurist Mesh Agents

This SOP defines the standard process for integrating a new third-party data service into Heurist Mesh.

It is based on the actual Yahoo Finance integration pattern:

1. scope the service before writing production agent code
2. validate the real runtime surface, not just the docs
3. promote only the highest-value capabilities into first-class agent tools
4. ship compact, agent-usable outputs with direct failure behavior
5. back the integration with focused tests, example outputs, and regression coverage

Use this SOP for any new external data source, whether the service is a Python library, REST API, SDK, or vendor-specific endpoint family.

## Goals

- integrate new data services without turning agents into thin wrappers over every upstream endpoint
- preserve Mesh agent quality: clear tool boundaries, compact outputs, stable schemas, honest failures
- reduce rework by separating discovery from production integration
- keep the final agent useful for downstream LLMs, not just technically connected to a backend

## Core Principles

- Runtime is the source of truth. Vendor docs are useful, but the installed package version and real API responses decide what we can safely ship.
- Fewer, clearer tools beat many overlapping wrappers. We should expose meaningful task-level tools, not every endpoint.
- Tool outputs must optimize for the next agent decision, not backend completeness.
- Token efficiency is a product requirement. Pagination, truncation, filtering, and sensible defaults are mandatory where result sets can grow.
- Direct tool calls should return structured data with stable top-level keys and direct errors for unsupported or invalid requests.
- Every bug found during integration should turn into a reproducible regression case.

## Step 1: Scoping, Exploration, And Preliminary Service Testing

This step exists to decide what should be integrated before production agent code expands.

### Step 1 Objectives

- understand the upstream documentation and runtime surface
- identify runtime drift between docs and the installed version
- determine which capabilities are worth becoming first-class Mesh tools
- reject low-signal, overlapping, or raw passthrough ideas early
- produce a concrete integration plan with acceptance criteria

### Step 1 Process

1. Gather source material.
   - Identify official docs, SDK references, examples, rate-limit notes, and authentication requirements.
   - If the surface is broad or likely to drift, create a local docs mirror under `docs/<service>/`.
   - Add a machine-readable manifest or index when the mirrored set is large.

2. Establish the runtime reference surface.
   - Install or confirm the exact runtime dependency version.
   - Write a feature sweep script in `mesh/test_scripts/test_<service>_feature_sweep.py`.
   - Exercise the high-value classes, functions, and optional features directly.
   - Record what is available, what fails, what is incomplete, and what differs from the docs.

3. Inventory candidate capabilities.
   - Group upstream features into user tasks, not endpoint names.
   - Ask: what would another agent actually use to make a decision?
   - Separate must-have tools from nice-to-have surfaces and raw debug-only capabilities.

4. Define the first-class tool surface.
   - Pick a small initial tool set with distinct purposes.
   - Draft tool names, descriptions, inputs, asset or entity constraints, and response shapes.
   - Eliminate overlapping tools and thin wrappers that only duplicate upstream terminology.

5. Write a scoping or handoff doc.
   - Capture runtime drift, in-scope features, out-of-scope features, and the review flow.
   - If the integration is multi-phase, write a phase plan before implementation starts.

### Step 1 Deliverables

- optional docs mirror in `docs/<service>/`
- feature sweep script in `mesh/test_scripts/`
- scoping or handoff doc in `docs/`
- candidate tool list with draft response shapes
- explicit list of runtime drift and unsupported features

### Step 1 Acceptance Criteria

Step 1 is complete only when all of the following are true:

- the team can point to the exact upstream docs and exact runtime version being targeted
- the real callable surface has been tested directly with a sweep or equivalent script
- known docs-vs-runtime drift has been documented
- the proposed tools are task-oriented, non-overlapping, and narrower than the full upstream API surface
- each proposed tool has a clear success shape, failure mode, and scope boundary
- at least one scoping document exists that another engineer can use to continue the work without rediscovery

### Step 1 Quality Bar

Reject the scoping phase if:

- the plan assumes the docs are accurate without runtime verification
- the proposed tools are mostly one-endpoint wrappers
- the output shapes are still raw payload dumps
- scope boundaries are vague
- unsupported features are being deferred to implementation instead of being called out now

## Agent Tool Design Guidelines

These rules apply before and during implementation.

### 1. Prefer fewer, clearer tools

- Each tool should represent a meaningful job for the agent.
- Avoid exposing one tool per upstream endpoint unless the endpoint maps cleanly to a unique user task.
- If two tools would often be valid for the same request, the boundary is probably weak.

### 2. Make tool boundaries legible

- Use names that make the action space obvious.
- Group related capabilities naturally and consistently.
- Treat naming as a behavior control surface, not a cosmetic choice.

Good:

- `resolve_symbol`
- `quote_snapshot`
- `equity_overview`
- `equity_screen`

Bad:

- `get_data`
- `fetch_company`
- `ticker_info_full`
- `endpoint_7_wrapper`

### 3. Return high-signal context

- Prefer fields that help the next decision.
- Do not default to raw IDs, null-heavy metadata, or giant vendor payloads.
- Omit empty sections.
- Normalize and rename upstream fields when that makes outputs easier for agents to consume.

### 4. Design for token efficiency

- Add `limit`, filtering, pagination, date windows, or truncation where needed.
- Bound large arrays.
- Use compact summaries at the top level.
- Default to agent-usable summaries, not exhaustive dumps.

### 5. Treat descriptions and schemas as prompts

- Tool descriptions must explain when to use the tool and when not to use it.
- Parameter names should be explicit and unambiguous.
- Schemas should encode constraints like enums, defaults, and required combinations where possible.
- Describe hidden conventions directly in the schema text.

### 6. Enforce schema quality

- Avoid loose free-form inputs where structured parameters are possible.
- Reject invalid parameter combinations directly.
- Fail clearly on unsupported entity types, intervals, markets, or modes.

### 7. Read transcripts, not just pass rates

- Review tool-call transcripts during testing.
- Repeated bad parameters usually mean schema or description problems.
- Repeated redundant calls usually mean poor tool boundaries or low-signal responses.
- If the model hesitates between tools, the tool surface is probably too ambiguous.

## Step 2: Integration

This step begins only after Step 1 is materially complete.

### Step 2 Objectives

- implement the selected service integration inside a Mesh agent
- expose a compact, production-grade tool surface
- add direct tests, example outputs, and regression coverage
- validate behavior with live service calls where practical

### Step 2 Process

1. Create or extend the agent.
   - Inherit from `mesh.mesh_agent.MeshAgent`.
   - Use a descriptive PascalCase class name ending in `Agent`.
   - Update metadata in `__init__` with name, version, author, description, external APIs, tags, image, examples, credits, and x402 config where relevant.

2. Implement the tool schemas.
   - Define tools in `get_tool_schemas()`.
   - Keep the initial tool set small and distinct.
   - Use explicit parameter descriptions, enums, defaults, and required fields.
   - Encode scope constraints in both tool descriptions and implementation.

3. Implement service access.
   - Use environment variables for credentials.
   - Use `@with_retry` and `@with_cache` for network operations where appropriate.
   - Keep the implementation straightforward. Do not add defensive abstraction layers without a concrete need.
   - Normalize upstream responses into compact agent-facing structures.

4. Implement direct failure behavior.
   - Return structured errors for invalid requests, unsupported entity or asset combinations, no-data cases, and upstream failures.
   - Do not pretend unsupported features work because they exist in docs.

5. Add direct agent tests.
   - Create or update `mesh/tests/<agent>.py`.
   - Add representative success and failure cases for every tool.
   - Cover invalid inputs, unsupported combinations, and no-result conditions.

6. Update example outputs.
   - Save example input or output coverage in YAML under `mesh/tests/`.
   - Manually inspect examples for compactness, clarity, and null-heavy junk.

7. Add ad-hoc integration scripts.
   - Put service sweeps and targeted regressions in `mesh/test_scripts/`.
   - Use:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run python mesh/test_scripts/<script_name>.py
```

8. Verify the implementation iteratively.
   - Run focused direct-tool tests first.
   - Run the broader feature sweep if the surface or behavior changed materially.
   - Add a targeted regression case for each bug found.
   - If new dependencies are required, add them with `uv add <package>`.

### Step 2 Acceptance Criteria

Step 2 is complete only when all of the following are true:

- the agent metadata is complete and consistent with Mesh conventions
- the tool set is intentionally limited, distinct, and clearly described
- every tool has at least one direct success case and one direct failure case
- outputs are compact, normalized, and useful to another agent without extra parsing
- unsupported requests fail directly and honestly
- the integration has been exercised against the live runtime, not only mocked locally
- runtime drift discovered during implementation is reflected in docs, tests, or both
- example outputs and regression cases are checked in

### Step 2 Quality Bar

Reject or rework the integration if it does any of the following:

- ships thin wrappers around raw upstream endpoints
- exposes overlapping tools with ambiguous routing
- returns large raw payloads by default
- hides errors behind vague text
- omits critical context like symbol, market, interval, or date window
- leaks empty sections, unstable keys, or backend-specific noise
- lacks a live sweep or equivalent real-runtime verification

## Standard Verification Checklist

Use this checklist on every new service integration.

- `Schema`: Tool names, descriptions, parameters, enums, and defaults are explicit and non-overlapping.
- `Scope`: The agent only claims support for what is actually implemented and runtime-verified.
- `Output`: Top-level keys are stable, compact, and decision-useful.
- `Failure`: Invalid or unsupported requests fail directly with structured errors.
- `Runtime`: Real service calls were tested in this environment.
- `Regression`: Each discovered bug produced a focused regression test or script case.
- `Docs`: Scoping notes, runtime drift, and usage examples are documented.

## Recommended Artifact Set

For non-trivial integrations, the expected artifact set is:

- `mesh/agents/<service>_agent.py`
- `mesh/tests/<service>_agent.py`
- `mesh/tests/<service>_agent_example.yaml`
- `mesh/test_scripts/test_<service>_feature_sweep.py`
- `docs/<service>-handoff.md` or `docs/<service>-phase-plan.md`
- optional mirrored docs under `docs/<service>/`

## Practical Review Loop

Use this loop during development:

1. change one tool or one behavior family
2. run the direct tests
3. run the broader sweep if the change affects surface or output shape
4. inspect outputs manually for clarity, compactness, and scope honesty
5. add or tighten regression coverage before expanding scope further

## Decision Rule

A new data service is ready for Heurist Mesh only when:

- the integration has a narrow, legible tool surface
- the outputs are optimized for agent use rather than backend completeness
- the implementation matches the verified runtime surface
- the direct tests, example outputs, and live sweeps support the claimed behavior

If any of those are missing, do not expand the service further. Tighten scope, fix the surface, and re-run the validation loop.
