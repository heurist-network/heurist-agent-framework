sequenceDiagram
    participant User
    participant Heurist as Heurist Tool API
    participant Inflow as Inflow API

    User->>Inflow: 1. Sign up for Inflow API (POST /v1/users/agentic)
    Inflow-->>User: 2. Signup successful (userId + credentials)

    User->>Heurist: 3. Query service and price
    Heurist-->>User: 4. Return service info + price
    User->>Heurist: 5. Confirm payment authorization

    Heurist->>Inflow: 6. Create payment request (POST /v1/requests/payment)
    Inflow-->>Heurist: requestId + status=PENDING
    Inflow-->>User: Approval prompt (dashboard/email/mobile app)
    User->>Inflow: Approve or decline payment

    loop Poll every 5s (timeout at 300s)
        Heurist->>Inflow: GET /v1/requests/{requestId}
        Inflow-->>Heurist: status = PENDING|APPROVED|DECLINED|EXPIRED|CANCELLED
    end

    alt status == APPROVED
        Heurist->>Heurist: Execute sync tool call
        Heurist-->>User: 7. Deliver service result
    else status in DECLINED/EXPIRED/CANCELLED
        Heurist-->>User: Payment failed (no service delivery)
    else timeout (300s)
        Heurist-->>User: Payment timeout (no service delivery)
    end
