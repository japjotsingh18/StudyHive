import { describe, expect, it } from "vitest";

import { protectedRouteDecision } from "@/lib/route-guard";

describe("protected frontend route policy", () => {
  it("redirects an anonymous account request to login", () => {
    expect(protectedRouteDecision("/account", false)).toEqual({
      kind: "redirect",
      destination: "/login",
    });
  });

  it("allows a browser with a session cookie to reach server validation", () => {
    expect(protectedRouteDecision("/account", true)).toEqual({ kind: "allow" });
  });

  it("does not protect unrelated public routes", () => {
    expect(protectedRouteDecision("/login", false)).toEqual({ kind: "allow" });
  });
});
