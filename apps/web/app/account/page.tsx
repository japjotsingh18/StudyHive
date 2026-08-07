"use client";

import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { AuthApiError, getAccount, logout } from "@/lib/auth-api";

export default function AccountPage() {
  const router = useRouter();
  const [logoutError, setLogoutError] = useState<string | null>(null);
  const account = useQuery({
    queryKey: ["account-bootstrap"],
    queryFn: getAccount,
    retry: false,
  });

  async function handleLogout() {
    setLogoutError(null);
    try {
      await logout();
      router.replace("/login");
      router.refresh();
    } catch (error) {
      setLogoutError(
        error instanceof AuthApiError
          ? error.message
          : "StudyHive could not sign you out. Try again.",
      );
    }
  }

  return (
    <main
      className="mx-auto min-h-screen w-full max-w-3xl px-6 py-12"
      id="main-content"
    >
      <header className="flex flex-wrap items-center justify-between gap-4 border-b pb-6">
        <div>
          <p className="text-sm font-semibold text-[var(--color-accent)]">
            StudyHive
          </p>
          <h1 className="mt-1 text-3xl font-bold tracking-tight">Account</h1>
        </div>
        <button
          className="min-h-11 rounded-[var(--radius-control)] border px-4 py-2 font-semibold"
          onClick={() => void handleLogout()}
          type="button"
        >
          Sign out
        </button>
      </header>
      <section aria-labelledby="account-status" className="py-8">
        <h2 className="text-xl font-bold" id="account-status">
          Authentication status
        </h2>
        {account.isPending ? (
          <p
            aria-live="polite"
            className="mt-4 text-[var(--color-text-secondary)]"
          >
            Loading your secure account…
          </p>
        ) : null}
        {account.isError ? (
          <div
            className="mt-4 rounded-[var(--radius-control)] border p-4"
            role="alert"
          >
            <p>Your session could not be validated. Sign in again.</p>
            <button
              className="mt-3 font-semibold text-[var(--color-accent)] underline"
              onClick={() => router.replace("/login")}
              type="button"
            >
              Go to sign in
            </button>
          </div>
        ) : null}
        {account.data === undefined ? null : (
          <dl className="mt-5 grid gap-4 rounded-[var(--radius-surface)] border p-5 sm:grid-cols-2">
            <div>
              <dt className="text-sm text-[var(--color-text-secondary)]">
                Account
              </dt>
              <dd className="mt-1 font-semibold capitalize">
                {account.data.data.attributes.account_status}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-[var(--color-text-secondary)]">
                Email verification
              </dt>
              <dd className="mt-1 font-semibold capitalize">
                {account.data.data.attributes.email_verification}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-[var(--color-text-secondary)]">
                University verification
              </dt>
              <dd className="mt-1 font-semibold capitalize">
                {account.data.data.attributes.university_verification}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-[var(--color-text-secondary)]">
                Profile
              </dt>
              <dd className="mt-1 font-semibold capitalize">
                {account.data.data.attributes.profile_completion}
              </dd>
            </div>
          </dl>
        )}
        <p className="mt-5 text-sm leading-6 text-[var(--color-text-secondary)]">
          Sprint 1 establishes your secure identity and session. University
          verification and profile onboarding are intentionally unavailable
          until their approved sprint.
        </p>
        {logoutError === null ? null : (
          <p
            aria-live="polite"
            className="mt-4 text-sm text-[var(--color-danger)]"
            role="alert"
          >
            {logoutError}
          </p>
        )}
      </section>
    </main>
  );
}
