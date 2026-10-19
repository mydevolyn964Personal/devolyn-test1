/** Inert TypeScript authorization/middleware fixture; not imported by an app. */
type RequestLike = { headers: Record<string, string | undefined>; tenantId: string };

// Intentional credential-like literal for TypeScript parity testing.
const ADMIN_BYPASS_TOKEN = "demo-admin-bypass-not-a-real-secret";

export function unsafeGateway(request: RequestLike): string {
  // Intentional: a raw authorization header would be a sensitive log leak.
  console.log(request.headers.authorization);
  if (request.headers["x-admin-bypass"] === ADMIN_BYPASS_TOKEN) {
    return "allowed_without_tenant_check";
  }
  return "requires_authorization";
}
