# Tweet Claim Flow

Self-service flow for new users to claim `100` free credits by posting a verification tweet.

## Endpoints

### `POST /claim_credits/initiate`
Returns:
- `verification_code` (5 chars)
- `tweet_text` (user posts this on X)
- `instructions`

### `POST /claim_credits/verify`
Body:
```json
{
  "tweet_url": "https://x.com/<user>/status/<id>",
  "verification_code": "<code>"
}
```
Returns on success:
- `api_key` (`<twitter_handle>-<16 chars>`)
- `credits` (`100`)
- `twitter_handle`

## Verification Rules
- Tweet URL must be from `x.com` or `twitter.com` and include `/status/<tweet_id>`.
- Tweet content must include `@heurist_ai`.
- Tweet content must include `verification: <code>` (case-insensitive).
- Verification code must be active (TTL: 10 minutes).
- One claim per Twitter handle.

## Data Stores
- **Users table** (`DYNAMODB_TABLE_NAME`): stores API key item and `USER_DATA` credits item.
- **Claims table** (`tweet-credits-claims`, hardcoded): stores pending verification codes and claimed handles.
  - Partition key: `claim_key` (String)
  - Recommended TTL attribute: `expires_at`

## Required Env Vars
- `DYNAMODB_TABLE_NAME`
- `AWS_REGION` (recommended)
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (if not using IAM role)
- `APIDANCE_API_KEY` (optional fallback provider)

## Error Codes
- `400`: invalid/expired code, invalid URL, missing required tweet text/code
- `404`: tweet not found
- `409`: Twitter handle already claimed
- `502`: tweet verification providers unavailable
- `503`: claim service unavailable (table/config issue)
