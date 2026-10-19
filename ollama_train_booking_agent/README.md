# Ollama Train Booking Agent (safe demo)

This is a self-contained, agentic train-ticket booking demonstration using
Ollama with `qwen3:8b` for optional intent planning. It does **not** connect to
railway, identity, or payment systems. The inventory and bookings live only in
memory for the lifetime of the process.

## Safety model

- Searching trains is read-only.
- A booking is never made from model text alone.
- `confirm_booking` requires the exact booking ID and an explicit `yes` from
  the caller.
- The supplied passenger email is stored only in the in-memory booking record.

## Run

Install Ollama and pull the model first:

```text
ollama pull qwen3:8b
python -m ollama_train_booking_agent.cli
```

The CLI works without Ollama by falling back to deterministic intent routing.

## Test

```text
python -m unittest discover -s ollama_train_booking_agent/tests -v
```
