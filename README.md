# Stripe Shop (Django + MySQL)

## What this app does
Single-page shop showing 3 fixed products. Users can enter quantities, pay using Stripe (test mode), and see paid orders on the same page.

## Assumptions
- Prices are stored in cents (integer) to avoid currency rounding issues.
- Stripe Checkout is used for simplicity.
- Orders are created before redirecting to Checkout and marked paid via Stripe webhook.

## Flow chosen
**Stripe Checkout** (hosted checkout page) because:
- Simpler integration.
- Handles payment authentication (3DS) and validation.
- Reduces PCI surface area.

## How double-charge / inconsistent state is avoided
- Orders created before checkout with `stripe_session_id` unique field.
- Final `paid` status set only when `checkout.session.completed` webhook is received and validated.
- Use idempotency keys for critical Stripe API calls.

## Setup / run steps
1. Create virtualenv & install:
   ```bash

   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

**Aslo add** 
STRIPE_PUBLISHABLE_KEY = "####"
STRIPE_SECRET_KEY = "####"