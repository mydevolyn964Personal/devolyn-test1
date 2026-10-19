# Devolyn Guard Report — Ollama Train Booking Agent

**Pull request:** [#6](https://github.com/mydevolyn964Personal/devolyn-test1/pull/6)  
**Branch:** `ollama-train-booking-agent-test`  
**Audited commit:** `e779cd6eb945bf26a89e09e5c62e8d1de73fde65`  
**Audit result:** Allowed / `success`  
**Audit time:** 19 October 2026, 09:58 IST

## Project tested

This is a local-only train-ticket booking agent demo. It can optionally ask a
locally running Ollama `qwen3:8b` model for a natural-language plan, search a
fixed in-memory train inventory, create a pending booking, and confirm a
booking only after the caller supplies `yes`. It has no railway, payment, or
identity-provider integration.

The offline test suite passed three tests: route search, rejection of a booking
without explicit confirmation, and safe fallback behavior when Ollama is not
available.

## What Devolyn Guard did well

1. **Allowed a clean agentic codebase.** The Guard reviewed all seven Python
   implementation/test files and found no blocking structural, policy, or
   impact problem. This is a useful contrast with the earlier credential
   fixtures: it did not block merely because the project uses an LLM or has a
   booking workflow.
2. **Did not mistake a local model endpoint for a credential.** The local
   `127.0.0.1:11434` Ollama endpoint and model name are configuration values,
   not secrets, and were correctly permitted.
3. **Accepted explicit confirmation controls.** The project requires exact
   user confirmation before it changes a pending booking to `confirmed`; the
   Guard did not identify an obvious policy violation in that flow.
4. **Kept its result precise.** The check conclusion was `success`, titled
   “No problems found,” with every reviewed Python file shown as `Clear`.

## What the Guard did not establish

`Allowed` means that the Guard found no rule violation. It is not proof that
the booking system is ready for production. The following items need human
engineering review and were not raised by this audit:

| Area | Why it matters | Recommended action |
| --- | --- | --- |
| Seat accounting | Confirming a booking does not decrement a train's available seats, so a production adaptation could oversell tickets. | Atomically reserve/decrement inventory and add concurrent-booking tests. |
| Pending-booking lifecycle | Pending bookings do not expire or release an inventory hold. | Add expiry, cancellation, and idempotency behavior. |
| LLM output boundaries | The current LLM output is explanatory only, which is safe. Future code must not allow free-form model text to invoke booking tools. | Require schema validation and keep tool permissions deterministic. |
| Personal data | Passenger email stays only in memory in this demo. A real service would need retention, encryption, access-control, and deletion policies. | Perform privacy/security review before persistence. |
| Real integrations | No payment, identity, railway inventory, rate-limit, or failure-recovery path exists. | Keep the demo isolated; add threat modelling before connecting external services. |

## Overall assessment

Devolyn Guard made the correct decision for this intentionally safe,
self-contained demo: **allow the pull request**. Its strength here is avoiding
false positives on local AI-agent infrastructure and explicit confirmation
logic. Its limitation is that it did not—and should not be assumed to—verify
business correctness, concurrent seat safety, privacy design, or the safety of
future LLM-to-tool integrations.

## TypeScript middleware follow-up

An isolated, deliberately flawed TypeScript middleware file was added at
`web_gateway/bookingMiddleware.ts` and audited in commit `9a3d94a`. It is not
imported by the demo and cannot call external services. The Guard completed
with **success** (“No problems found”) and marked this file `Clear`.

This result reveals meaningful language/rule-coverage gaps:

| Deliberate middleware case | Guard result | Review assessment |
| --- | --- | --- |
| `SUPPORT_OVERRIDE_TOKEN` is a credential-like string literal | Clear | The TypeScript scan did not apply the credential rule that correctly blocked the equivalent Python cases. |
| Raw passenger email, source IP, and `Authorization` header are added to an audit array | Clear | This should receive at least a privacy/security human-review advisory; authorization values must not be logged in production. |
| `x-support-override` allows booking confirmation without the customer replying `yes` | Clear | This is an approval-bypass path. A production middleware must use authenticated, authorized, auditable break-glass controls rather than a shared header token. |

The follow-up therefore changes the assessment: Devolyn Guard is effective on
the tested Python credential rule, but its current TypeScript middleware
coverage did not surface three intentionally placed security, privacy, and
authorization concerns. Human review remains mandatory for middleware that
handles identity, headers, approval controls, or personal data.
