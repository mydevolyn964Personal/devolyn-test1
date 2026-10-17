# devolyn-test1
First Test repository for Devolyn Guard

## Deliberately flawed Python fixture

`fixtures/deliberately_flawed.py` is an isolated sample for testing whether a
review tool detects structural, policy, and impact issues. Its credential is
fake, and its destructive behavior only clears an in-memory list created by
the fixture. It makes no network, filesystem, or other external changes.

## Context-dependent review example

`fixtures/human_review.py` stores an email domain in an in-memory diagnostic
list. This is intentional and uses a reserved example address; whether it
deserves a privacy warning depends on the product context, the data subjects,
and the diagnostic list's eventual use and retention. It does not transmit or
persist data. Use it to check that a review tool explains uncertainty and
requests human judgment instead of treating every potential concern as a
confirmed violation.
