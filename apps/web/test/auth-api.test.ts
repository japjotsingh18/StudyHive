import { afterEach, describe, expect, it, vi } from "vitest";

import { login, logout } from "@/lib/auth-api";
import type { AuthApiError } from "@/lib/auth-api";

const SESSION_RESPONSE = {
  data: {
    type: "session",
    id: "ses_test",
    attributes: {
      expires_at: "2026-08-06T10:00:00Z",
      account_status: "pending",
      email_verification: "pending",
      university_verification: "unverified",
      profile_completion: "incomplete",
      recent_authentication_until: "2026-08-06T03:15:00Z",
    },
    relationships: { user: { data: { type: "user", id: "usr_test" } } },
    capabilities: ["validate", "refresh", "logout"],
  },
  meta: {
    request_id: "req_test",
    generated_at: "2026-08-06T03:00:00Z",
    warnings: [],
  },
  links: {},
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("authentication API client", () => {
  it("sends credentials through cookie-authenticated requests without exposing them in URLs", async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify(SESSION_RESPONSE), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const session = await login({
      email: "student@example.edu",
      password: "a sufficiently long password",
      rememberMe: true,
    });

    expect(session.data.id).toBe("ses_test");
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/auth/login",
      expect.objectContaining({ credentials: "include", method: "POST" }),
    );
    const request = fetchMock.mock.calls.at(0)?.[1];
    expect(typeof request?.body === "string" ? request.body : "").toContain(
      "a sufficiently long password",
    );
  });

  it("maps the safe problem envelope to a typed error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            error: {
              code: "invalid_credentials",
              message: "The email or password is incorrect.",
              status: 401,
              request_id: "req_failure",
              retryable: false,
            },
          }),
          { status: 401, headers: { "Content-Type": "application/json" } },
        ),
      ),
    );

    await expect(
      login({
        email: "student@example.edu",
        password: "wrong password",
        rememberMe: false,
      }),
    ).rejects.toMatchObject({
      code: "invalid_credentials",
      requestId: "req_failure",
    } satisfies Partial<AuthApiError>);
  });

  it("binds logout to the readable CSRF cookie", async () => {
    Object.defineProperty(document, "cookie", {
      configurable: true,
      value: "studyhive_csrf=csrf-token",
    });
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValue(new Response(null, { status: 204 }));
    vi.stubGlobal("fetch", fetchMock);

    await logout();

    const request = fetchMock.mock.calls.at(0)?.[1];
    expect(new Headers(request?.headers).get("X-CSRF-Token")).toBe(
      "csrf-token",
    );
  });
});
