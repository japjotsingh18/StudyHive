import { type NextRequest, NextResponse } from "next/server";

import { protectedRouteDecision } from "@/lib/route-guard";

export function proxy(request: NextRequest) {
  const decision = protectedRouteDecision(
    request.nextUrl.pathname,
    request.cookies.has("studyhive_session"),
  );
  if (decision.kind === "redirect") {
    return NextResponse.redirect(new URL(decision.destination, request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/account/:path*"],
};
