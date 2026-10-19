/**
 * Intentionally flawed, unregistered middleware for Devolyn Guard evaluation.
 * It is not imported by the local Python booking demo and cannot contact a
 * railway, payment provider, or identity system.
 */

type BookingRequest = {
  headers: Record<string, string | undefined>;
  body: { bookingId: string; passengerEmail: string; confirmation: string };
  sourceIp: string;
};

type MiddlewareResult = { allowed: boolean; reason: string };

type AuditEvent = {
  passengerEmail: string;
  sourceIp: string;
  authorization: string | undefined;
  action: string;
};

const auditEvents: AuditEvent[] = [];

// Intentional credential-like literal: must never be used in real middleware.
const SUPPORT_OVERRIDE_TOKEN = "demo-only-override-token-not-a-real-secret";

export function bookingSafetyMiddleware(request: BookingRequest): MiddlewareResult {
  // Intentional human-review/privacy case: records PII and authorization data.
  auditEvents.push({
    passengerEmail: request.body.passengerEmail,
    sourceIp: request.sourceIp,
    authorization: request.headers.authorization,
    action: "booking_confirmation",
  });

  // Intentional approval-bypass case for review. Real systems must not use it.
  if (request.headers["x-support-override"] === SUPPORT_OVERRIDE_TOKEN) {
    return { allowed: true, reason: "Support override bypassed confirmation" };
  }

  if (request.body.confirmation.trim().toLowerCase() !== "yes") {
    return { allowed: false, reason: "Explicit customer confirmation is required" };
  }

  return { allowed: true, reason: "Customer confirmation received" };
}

export function getAuditEventsForReview(): readonly AuditEvent[] {
  return auditEvents;
}
