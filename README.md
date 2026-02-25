# POS Payment App 

A clickable Point-of-Sale (POS) payment prototype built with Django.

This project simulates the main payment flow for a small merchant, including:
- Card payments
- QR payments
- Error handling (declined, offline, expired)
- Transaction history
- Refund flow (simulated)

# Objective

Build a simple, merchant-friendly POS app that demonstrates:

- Clear checkout flow
- Transaction lifecycle modeling
- Error handling and recovery
- Refund simulation
- Clean UI/UX for cashiers

Designed for:
- Small merchants
- Fast checkout environments
- Minimal training requirement

# Core Workflow

1. New Sale
- Enter amount
- Choose payment method (Card / QR)

2. Payment Processing
- Processing state
- Success or failure (simulated)

3. Transaction History
- View all transactions
- Status indicators
- Reference IDs

4. Refund (Optional Flow)
- Refund available for successful transactions
- Refund reference generated
- Refund timestamp stored

# Transaction States

- `pending`
- `success`
- `declined`
- `offline`
- `expired`
- `failed`
- `refunded`

This models a simplified real-world payment lifecycle.

# Refund Design

Refund is implemented as a state transition:

- Only successful transactions can be refunded
- Refund generates:
  - `refund_reference`
  - `refunded_at` timestamp
- Status changes to `refunded`

In production:
- Refunds would require provider API calls
- Eligibility validation
- Idempotency protection
- Audit logging