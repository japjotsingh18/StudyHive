export interface SessionEnvelope {
  data: {
    type: "session";
    id: string;
    attributes: {
      expires_at: string;
      account_status: "pending" | "active";
      email_verification: "pending" | "verified";
      university_verification: "unverified" | "verified";
      profile_completion: "incomplete" | "complete";
      recent_authentication_until: string;
    };
    relationships: {
      user: { data: { type: "user"; id: string } };
    };
    capabilities: string[];
  };
  meta: { request_id: string; generated_at: string; warnings: unknown[] };
  links: Record<string, string>;
}

export interface AccountEnvelope {
  data: {
    type: "user";
    id: string;
    attributes: {
      account_status: "pending" | "active";
      email_verification: "pending" | "verified";
      university_verification: "unverified" | "verified";
      profile_completion: "incomplete" | "complete";
      roles: string[];
      scopes: string[];
    };
    capabilities: string[];
  };
  meta: { request_id: string; generated_at: string; warnings: unknown[] };
  links: Record<string, string>;
}

interface ProblemEnvelope {
  error: {
    code: string;
    message: string;
    status: number;
    request_id: string;
    retryable: boolean;
  };
}

interface LoginInput {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface RegistrationInput {
  email: string;
  password: string;
}

const API_ORIGIN =
  process.env.NEXT_PUBLIC_STUDYHIVE_API_URL ?? "http://localhost:8000";

export class AuthApiError extends Error {
  readonly code: string;
  readonly requestId: string | null;
  readonly status: number;

  constructor(
    message: string,
    code: string,
    status: number,
    requestId: string | null,
  ) {
    super(message);
    this.name = "AuthApiError";
    this.code = code;
    this.status = status;
    this.requestId = requestId;
  }
}

export async function login(input: LoginInput): Promise<SessionEnvelope> {
  return requestSession("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({
      email: input.email,
      password: input.password,
      remember_me: input.rememberMe,
    }),
  });
}

export async function register(
  input: RegistrationInput,
): Promise<SessionEnvelope> {
  return requestSession("/api/v1/auth/registrations", {
    method: "POST",
    headers: { "Idempotency-Key": globalThis.crypto.randomUUID() },
    body: JSON.stringify({
      email: input.email,
      password: input.password,
      policy_acknowledgements: [
        { key: "terms_of_service", version: "1" },
        { key: "privacy_policy", version: "1" },
      ],
    }),
  });
}

export async function getSession(): Promise<SessionEnvelope> {
  const response = await apiFetch("/api/v1/auth/session", { method: "GET" });
  return parseSessionEnvelope(await response.json());
}

export async function getAccount(): Promise<AccountEnvelope> {
  const response = await apiFetch("/api/v1/me", { method: "GET" });
  return parseAccountEnvelope(await response.json());
}

export async function logout(): Promise<void> {
  await apiFetch("/api/v1/auth/logout", {
    method: "POST",
    headers: csrfHeaders(),
  });
}

async function requestSession(
  path: string,
  init: RequestInit,
): Promise<SessionEnvelope> {
  const response = await apiFetch(path, init);
  return parseSessionEnvelope(await response.json());
}

async function apiFetch(path: string, init: RequestInit): Promise<Response> {
  const headers = new Headers(init.headers);
  if (init.body !== undefined) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${API_ORIGIN}${path}`, {
    ...init,
    headers,
    credentials: "include",
  });
  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null);
    if (isProblemEnvelope(payload)) {
      throw new AuthApiError(
        payload.error.message,
        payload.error.code,
        payload.error.status,
        payload.error.request_id,
      );
    }
    throw new AuthApiError(
      "StudyHive could not complete the request. Try again.",
      "unexpected_response",
      response.status,
      response.headers.get("X-Request-ID"),
    );
  }
  return response;
}

function csrfHeaders(): HeadersInit {
  const token = readCookie("studyhive_csrf");
  return token === null ? {} : { "X-CSRF-Token": token };
}

function readCookie(name: string): string | null {
  if (typeof document === "undefined") {
    return null;
  }
  const prefix = `${encodeURIComponent(name)}=`;
  for (const segment of document.cookie.split(";")) {
    const candidate = segment.trim();
    if (candidate.startsWith(prefix)) {
      return decodeURIComponent(candidate.slice(prefix.length));
    }
  }
  return null;
}

function parseSessionEnvelope(value: unknown): SessionEnvelope {
  if (
    !isRecord(value) ||
    !isRecord(value.data) ||
    value.data.type !== "session" ||
    typeof value.data.id !== "string" ||
    !isRecord(value.data.attributes) ||
    typeof value.data.attributes.expires_at !== "string" ||
    !isRecord(value.meta) ||
    typeof value.meta.request_id !== "string"
  ) {
    throw new AuthApiError(
      "StudyHive returned an unexpected authentication response.",
      "invalid_response",
      502,
      null,
    );
  }
  return value as unknown as SessionEnvelope;
}

function parseAccountEnvelope(value: unknown): AccountEnvelope {
  if (
    !isRecord(value) ||
    !isRecord(value.data) ||
    value.data.type !== "user" ||
    typeof value.data.id !== "string" ||
    !isRecord(value.data.attributes) ||
    typeof value.data.attributes.account_status !== "string" ||
    !isRecord(value.meta) ||
    typeof value.meta.request_id !== "string"
  ) {
    throw new AuthApiError(
      "StudyHive returned an unexpected account response.",
      "invalid_response",
      502,
      null,
    );
  }
  return value as unknown as AccountEnvelope;
}

function isProblemEnvelope(value: unknown): value is ProblemEnvelope {
  return (
    isRecord(value) &&
    isRecord(value.error) &&
    typeof value.error.code === "string" &&
    typeof value.error.message === "string" &&
    typeof value.error.status === "number" &&
    typeof value.error.request_id === "string" &&
    typeof value.error.retryable === "boolean"
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
