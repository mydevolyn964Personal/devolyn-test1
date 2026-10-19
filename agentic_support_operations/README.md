# Agentic Support Operations Platform (local demo)

This production-style reference project models an AI support-operations agent.
It is intentionally local-only: tickets, knowledge articles, audit events, and
refund actions are in memory. It does not call an LLM, CRM, payment processor,
or customer-notification service.

## Design

- A bounded planner maps a requested support operation to a small action set.
- Read-only status lookups can complete automatically.
- Refunds become proposals and require a separate human approval step.
- Sensitive customer fields are excluded from audit events.
- Approval uses an idempotency key to avoid duplicate tool execution.
- Ticket content is treated as data, never as instructions for tool selection.

## Run tests

```text
python -m unittest discover -s agentic_support_operations/tests -v
```

This is an architectural demo, not a deployable service. A production version
would need authenticated identities, durable storage, encryption, observability,
rate limits, concurrency control, external-service contracts, and threat
modelling.
