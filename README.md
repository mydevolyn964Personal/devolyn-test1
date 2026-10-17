# devolyn-test1
First Test repository for Devolyn Guard

## Deliberately flawed Python fixture

`fixtures/deliberately_flawed.py` is an isolated sample for testing whether a
review tool detects structural, policy, and impact issues. Its credential is
fake, and its destructive behavior only clears an in-memory list created by
the fixture. It makes no network, filesystem, or other external changes.
