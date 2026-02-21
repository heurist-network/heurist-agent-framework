# Inflow Guide For AI Agents

Use this runbook to execute paid sync tool calls on Heurist Mesh with Inflow.

## 1) Required Inputs

Set these before running:

- `MESH_URL` (use production: `https://mesh.heurist.xyz`)
- `INFLOW_BASE_URL` (for direct Inflow checks, for example `https://sandbox.inflowpay.ai`)
- `BUYER_USER_ID` (Inflow buyer userId)
- `BUYER_PRIVATE_KEY` (Inflow buyer private key)

## 2) Optional Buyer Setup (One-Time Per Buyer)

If you already have a buyer user and private key, skip to section 3.

### 2.1 Create agentic user

`locale` and `timezone` are optional fields.

```bash
curl -sS -X POST "$MESH_URL/mesh_signup_inflow" \
  -H "Content-Type: application/json" \
  -d '{"locale":"EN_US","timezone":"US/Pacific"}'
```

Save:
- `data.userId` -> buyer user id
- `data.privateKey` -> buyer private key

### 2.2 Attach identity/email

Use a real email address that the user can access. After this step, the user should check inbox and complete Inflow email confirmation.

Password requirements:
- at least 10 characters
- at least 1 uppercase letter
- at least 1 lowercase letter
- at least 1 number
- at least 1 symbol

```bash
curl -sS -X POST "$MESH_URL/mesh_signup_inflow_attach" \
  -H "Content-Type: application/json" \
  -d '{
    "privateKey":"<BUYER_PRIVATE_KEY>",
    "email":"user@example.com",
    "firstName":"John",
    "lastName":"Doe",
    "password":"SecurePass1!"
  }'
```

Notes:
- attach is one-time for that buyer
- Inflow sends verification/approval links via email for HEADLESS flows

## 3) Build A Stable Mesh Request Payload

The second `/mesh_request` call must keep the same:
- `agent_id`
- `input.tool`
- `input.tool_arguments`
- `payment.user_id`

If these change, Mesh rejects `payment.request_id` with payload mismatch.

Example base payload:

```json
{
  "agent_id": "TokenResolverAgent",
  "input": {
    "tool": "token_profile",
    "tool_arguments": {"coingecko_id": "bitcoin"},
    "raw_data_only": true
  },
  "payment": {
    "provider": "INFLOW",
    "user_id": "<BUYER_USER_ID>",
    "currency": "USDC",
    "request_id": null
  }
}
```

## 4) First Call: Create Payment Request

```bash
curl -sS -X POST "$MESH_URL/mesh_request" \
  -H "Content-Type: application/json" \
  -d '<BASE_PAYLOAD_WITH_request_id_null>'
```

Expected response:
- `status: "payment_pending"`
- `payment.request_id: "<uuid>"`

Persist `payment.request_id` immediately. It is required for the next call.

## 5) Ask Human To Approve In Inflow

Present `payment.request_id` and ask the user to approve in Inflow dashboard/email/mobile flow.

Optional buyer-side status check:

```bash
curl -sS -H "X-API-Key: $BUYER_PRIVATE_KEY" \
  "$INFLOW_BASE_URL/v1/requests/<REQUEST_ID>"
```

If approved, buyer-side response shows `status: "APPROVED"`.

## 6) Second Call: Execute Tool With Same request_id

Send the same payload again, only changing:
- `payment.request_id` = saved request id

```bash
curl -sS -X POST "$MESH_URL/mesh_request" \
  -H "Content-Type: application/json" \
  -d '<SAME_PAYLOAD_WITH_request_id_set>'
```

Interpret response:
- tool result payload -> success, finish
- `status: "payment_pending"` -> approval not finalized yet; wait and retry same call
- `status: "payment_not_approved"` -> declined/expired/cancelled; stop and start a new payment flow
- `400` with invalid/expired request id -> restart from section 4 (new payment request)

## 7) Agent State Machine (Recommended)

1. Prepare stable payload.
2. Call `/mesh_request` with `request_id = null`.
3. If `payment_pending`, store `request_id` and notify user to approve.
4. Retry `/mesh_request` with same payload + `request_id`.
5. Loop on `payment_pending` with backoff (for example 3-10 seconds).
6. Exit on success or terminal failure (`payment_not_approved`).

## 8) Special Reuse Rule (No Additional Payment)

A previously approved `request_id` can be reused for these status tools:
- `AskHeuristAgent.check_job_status`
- `CaesarResearchAgent.get_research_result`

Requirements:
- same Inflow `user_id`
- same agent family
- matching linked status id from the original paid request:
  - `ask_heurist` -> same `job_id`
  - `caesar_research` -> same `research_id`

This means agents can continue polling job/research status without creating a new payment each time, if they reuse the correct approved `request_id`.

## 9) Self-Debug Playbook

### A) `Invalid or expired payment.request_id`

Check:
- second call used the same Mesh environment/session
- no long delay exceeded request TTL
- payload fields listed in section 3 did not change

### B) Inflow approved but Mesh still not succeeding

Check buyer-side request status directly:

```bash
curl -sS -H "X-API-Key: $BUYER_PRIVATE_KEY" \
  "$INFLOW_BASE_URL/v1/requests/<REQUEST_ID>"
```

If status is `APPROVED` and Mesh still errors, collect:
- `request_id`
- `transactionId` (if present)
- Mesh response body

Then retry once; if still failing, surface this diagnostic bundle to the platform operator.

### C) `INSUFFICIENT_FUNDS`

Buyer wallet balance is insufficient. Fund buyer wallet and restart from section 4.

## 10) Scripted End-To-End Test

For scripted flow (first call -> manual approve -> second call), use:

- `mesh/test_scripts/test_inflow_payment_flow_existing_buyer.py`

Example:

```bash
uv run python mesh/test_scripts/test_inflow_payment_flow_existing_buyer.py \
  --buyer-user-id <BUYER_USER_ID> \
  --mesh-url "$MESH_URL"
```
