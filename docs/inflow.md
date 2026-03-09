# Inflow Integration Plan (Use Existing `/mesh_request`)

## Goal
Use Inflow with the existing `POST /mesh_request` endpoint for sync tool calls by adding a `payment` object in the body.

## Scope
- In scope: sync direct tool calls (`input.tool`).
- Out of scope: natural language mode (`input.query`), async task APIs.
- Existing Heurist API key + credits flow remains unchanged when `payment` is not provided.

## API Contract

### Inflow request body (same `/mesh_request`)
```json
{
  "agent_id": "AskHeuristAgent",
  "input": {
    "tool": "ask_heurist",
    "tool_arguments": {"prompt": "What is BTC price?"},
    "raw_data_only": true
  },
  "payment": {
    "provider": "INFLOW",
    "user_id": "inflow-user-id-uuid",
    "currency": "USDC",
    "request_id": null
  }
}
```

Rules:
- Inflow path: no `api_key` / bearer required.
- First call: `request_id` must be empty.
- Second call: `request_id` must be present and must be the Inflow `requestId` returned from first call.

## Two-Call Flow (No Server Polling)
1. First call to `/mesh_request` with `payment.provider=INFLOW` and no `request_id`.
2. Server computes tool amount from metadata credits, then calls `POST /v1/requests/payment`.
3. If Inflow returns `requestId`, server returns `payment_pending` response with `request_id`.
4. User approves payment in Inflow.
5. User calls `/mesh_request` again with same payload + `payment.request_id`.
6. Server checks once with `GET /v1/requests/{requestId}`:
   - `APPROVED` -> execute tool and return result.
   - `PENDING/DECLINED/EXPIRED/CANCELLED` -> return non-success payment status; do not execute tool.

## Server Validation Rules
Use a single-process in-memory dict keyed by Inflow `requestId`:
- `INFLOW_REQUEST_CONTEXT: dict[str, dict]`

Store at minimum:
- `request_id`, `inflow_user_id`, `agent_id`, `tool_name`, `tool_args_hash`
- `created_at`, `expires_at`
- optional linked status IDs (`job_id`, `research_id`)

Enforce on second call:
- `request_id` exists in context store.
- `user_id`, `agent_id`, `tool`, `tool_arguments` hash match the stored context.
- context not expired.
- `request_id` is single-use by default after one approved execution, except allowlisted status tools below.

Rationale: prevents replay/tampering and binds an approved Inflow request to the exact tool call.

## Special Reuse Rule (Slow Status Tools)
Allow reuse of a previously approved `request_id` for:
- `AskHeuristAgent.check_job_status`
- `CaesarResearchAgent.get_research_result`

Allowed only when:
- same `inflow_user_id`
- same agent family
- provided status ID matches linked ID from the paid initial call:
  - `ask_heurist` -> `job_id`
  - `caesar_research` -> `research_id`

## Pricing
- Source of truth: existing tool credits metadata (`resolve_agent_credits`).
- Inflow amount: `max(credits / 100, 0.01)`.
- Initial currency: `USDC`.

## Error/Response Contract
- First call success: return `payment_pending` + Inflow `request_id`.
- First call failure (e.g. `INSUFFICIENT_FUNDS`): return Inflow error; no second call possible.
- Second call approved: return normal tool response.
- Second call with non-approved payment status: return payment status response; no tool execution.
- Invalid/missing/expired `request_id` or payload mismatch: `400`.
- Inflow API failure: `502`.

## Implementation Checklist
1. Update `mesh/mesh_api.py` request model:
   - add `payment` with `provider`, `user_id`, `currency`, `request_id`.
2. Update `/mesh_request` auth logic:
   - Inflow path bypasses `get_api_key` dependency and Heurist credit checks.
   - legacy path unchanged.
3. Add `mesh/inflow_service.py`:
   - create payment request
   - fetch request status (single check, no polling loop)
4. Add in-memory request context helpers in `mesh/mesh_api.py`:
   - create, validate, expire, cleanup.
5. Add allowlisted reuse logic for Ask/Caesar status tools.
6. Add env vars:
   - `INFLOW_BASE_URL` (default `https://sandbox.inflowpay.ai`)
   - `INFLOW_API_KEY`
   - `INFLOW_REQUEST_CONTEXT_TTL_SECONDS`

## Known Limitation
- Request context is in-memory only (single process).
- After process restart, prior `request_id` context is lost; second call should fail with clear error.

## Appendix: Inflow API Response Shapes (Sandbox-Verified)

Tested against `https://sandbox.inflowpay.ai` on 2026-02-13. All responses include an undocumented `"object"` discriminator field not in the OpenAPI spec.

Auth: all requests use `X-API-Key: <privateKey>` header.

### GET /v1/users/self

```json
{
  "object": "User",
  "created": "2026-01-16T19:39:04.293Z",
  "email": "team@heurist.xyz",
  "firstName": "JW",
  "lastName": "Wang",
  "locale": "ZH_CN",
  "timezone": "Europe/Amsterdam",
  "updated": "2026-02-12T21:10:11.292Z",
  "userId": "6bf5316e-32d3-4b80-8aa5-f89d0ef523cb"
}
```

### GET /v1/balances

```json
{
  "object": "Balances",
  "balances": [
    {"object": "Balance", "currency": "EURC"},
    {"object": "Balance", "currency": "PYUSD"},
    {"object": "Balance", "currency": "USDC"},
    {"object": "Balance", "currency": "USDT"}
  ]
}
```

Note: `total` field is omitted when balance is zero (despite being `required` in the OpenAPI spec).

### GET /v1/balances/{currency}

```json
{"object": "Balance", "currency": "USDC"}
```

### POST /v1/users/agentic

Request:
```json
{"locale": "EN_US", "timezone": "US/Pacific"}
```

Response (200):
```json
{
  "object": "AgenticUser",
  "created": "2026-02-13T11:15:46.532414319Z",
  "locale": "EN_US",
  "privateKey": "4469831a40a842e3a40b3962a1d4d40a",
  "timezone": "US/Pacific",
  "updated": "2026-02-13T11:15:46.648375933Z",
  "userId": "9e187225-afc6-4407-84d5-0b8fa2b9c74e"
}
```

### POST /v1/requests/payment

Request:
```json
{
  "userId": "<buyer-uuid>",
  "amount": 0.01,
  "currency": "USDC",
  "display": "HEADLESS",
  "userDetails": []
}
```

Success response (200) — returns `Request` object:
```json
{
  "requestId": "<uuid>",
  "status": "PENDING",
  "type": "PAYMENT"
}
```

Error response (400) — buyer has insufficient funds:
```json
{
  "errors": [
    {
      "code": "INSUFFICIENT_FUNDS",
      "message": "The wallet has insufficient funds.",
      "parameter": "amount"
    }
  ],
  "id": "<error-uuid>"
}
```

Note: on sandbox, newly created agentic users have zero balance so payment requests return `INSUFFICIENT_FUNDS`. In production, buyers must fund their Inflow wallets first.

### GET /v1/requests/{requestId}

Success response (200) — returns `Request` object:
```json
{
  "requestId": "<uuid>",
  "status": "PENDING|APPROVED|DECLINED|EXPIRED|CANCELLED",
  "type": "PAYMENT",
  "transactionId": "<uuid>",
  "approvedDetails": { ... },
  "userDetails": ["EMAIL", "NAME", ...]
}
```

Fields `transactionId` and `approvedDetails` are only present when `status` is `APPROVED`.

Error response (404):
```json
{
  "errors": [
    {
      "code": "APPROVAL_NOT_FOUND",
      "message": "The specified approval is not found.",
      "parameter": "approvalId"
    }
  ],
  "id": "<error-uuid>"
}
```

### GET /v1/transactions

```json
{
  "count": 0,
  "data": [],
  "total": 0
}
```

Each item in `data` follows the `Transaction` schema with fields: `transactionId`, `amount`, `currency`, `status`, `type`, `created`, `updated`, and optional `blockchain`, `transactionHash`, `errorCode`.

### GET /v1/events

```json
{
  "count": 0,
  "data": [],
  "total": 0
}
```

Each item in `data` follows the `Event` schema with fields: `eventId`, `type`, `status`, `created`, `delivered`, `webhookId`, `data`.

### POST /v1/users/search

Request:
```json
{"username": "some_user"}
```

Error response (404):
```json
{
  "errors": [
    {
      "code": "USER_NOT_FOUND",
      "message": "The specified user is not found.",
      "parameter": "userId"
    }
  ],
  "id": "<error-uuid>"
}
```

Success response (200):
```json
{
  "userId": "<uuid>"
}
```

### GET /v1/deposit-addresses

```json
{
  "object": "DepositAddresses",
  "configured": [
    {
      "address": "0xf9720cdbfa5648f624d4c0acc4c93c964600dbb3",
      "blockchain": "BASE",
      "currencies": ["EURC", "USDC"]
    },
    {
      "address": "5FDSMRdDWPYuxX16Fz4p2WqyxU8WSEkA7dJKQWeNFRaL",
      "blockchain": "SOLANA",
      "currencies": ["EURC", "PYUSD", "USDC", "USDT"]
    }
  ]
}
```

Note: `unconfigured` array is omitted when empty (not `[]`). New agentic users get wallets auto-configured on both BASE and SOLANA.

### POST /v1/deposit-addresses/{blockchain}

Response (200):
```json
{
  "object": "DepositAddress",
  "configured": {
    "address": "5bHPCjwbLwf8ZBgsNb7uwPDQfQ7wNRZRKg3mPJgHSmLC",
    "blockchain": "SOLANA",
    "currencies": ["EURC", "PYUSD", "USDC", "USDT"]
  }
}
```

### GET /v1/withdrawal-addresses

```json
{
  "object": "WithdrawalAddresses",
  "withdrawalAddresses": []
}
```

### Error Response Format (General)

All error responses follow:
```json
{
  "errors": [
    {
      "code": "INSUFFICIENT_FUNDS|APPROVAL_NOT_FOUND|USER_NOT_FOUND|PARAMETER_REQUIRED|...",
      "message": "Human-readable description.",
      "parameter": "optional-field-name"
    }
  ],
  "id": "<error-uuid>"
}
```

### Key Observations

1. **Undocumented `object` field**: Every successful response includes an `"object"` discriminator field (e.g., `"User"`, `"Balance"`, `"AgenticUser"`) not in the OpenAPI spec. Code should tolerate this extra field.
2. **Zero balance omits `total`**: The `Balance` schema marks `total` as required, but the API omits it when balance is zero.
3. **Auto-provisioned wallets**: New agentic users get BASE and SOLANA wallets auto-configured with all supported currencies.
4. **`INSUFFICIENT_FUNDS` pre-check**: Payment requests are rejected upfront if the buyer lacks funds — the API does not create a pending request for unfunded users.
5. **Sandbox limitation**: Cannot complete a full payment flow without real/testnet token deposits. The `POST /v1/requests/payment` → `GET /v1/requests/{requestId}` happy path needs a funded buyer.
6. **Timestamp formats**: `created`/`updated` use RFC 3339 format. Some include nanosecond precision (e.g., `2026-02-13T11:15:46.532414319Z`).
