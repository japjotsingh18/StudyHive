export type ProtectedRouteDecision =
  { kind: "allow" } | { kind: "redirect"; destination: string };

export function protectedRouteDecision(
  pathname: string,
  hasSessionCookie: boolean,
): ProtectedRouteDecision {
  if (pathname.startsWith("/account") && !hasSessionCookie) {
    return { kind: "redirect", destination: "/login" };
  }
  return { kind: "allow" };
}
