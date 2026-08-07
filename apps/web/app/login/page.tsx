"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { AuthShell } from "@/components/auth/auth-shell";
import {
  Field,
  FormError,
  PrimaryButton,
} from "@/components/auth/form-controls";
import { AuthApiError, login } from "@/lib/auth-api";

export default function LoginPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<AuthApiError | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    const form = new FormData(event.currentTarget);
    try {
      await login({
        email: formValue(form, "email"),
        password: formValue(form, "password"),
        rememberMe: form.get("remember_me") === "on",
      });
      router.push("/account");
      router.refresh();
    } catch (caughtError) {
      setError(
        caughtError instanceof AuthApiError
          ? caughtError
          : new AuthApiError(
              "StudyHive could not sign you in. Try again.",
              "unexpected_error",
              500,
              null,
            ),
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthShell
      description="Use the email and password connected to your StudyHive account."
      title="Sign in"
    >
      <form
        className="space-y-5"
        noValidate
        onSubmit={(event) => void handleSubmit(event)}
      >
        <FormError
          message={error?.message ?? null}
          requestId={error?.requestId}
        />
        <Field
          autoComplete="email"
          id="email"
          label="Email"
          name="email"
          required
          type="email"
        />
        <Field
          autoComplete="current-password"
          id="password"
          label="Password"
          name="password"
          required
          type="password"
        />
        <label
          className="flex min-h-11 items-center gap-3 text-sm"
          htmlFor="remember_me"
        >
          <input id="remember_me" name="remember_me" type="checkbox" />
          Keep me signed in on this device
        </label>
        <PrimaryButton disabled={isSubmitting}>
          {isSubmitting ? "Signing in…" : "Sign in"}
        </PrimaryButton>
      </form>
      <p className="mt-6 text-center text-sm text-[var(--color-text-secondary)]">
        New to StudyHive?{" "}
        <Link
          className="font-semibold text-[var(--color-accent)] underline"
          href="/register"
        >
          Create an account
        </Link>
      </p>
    </AuthShell>
  );
}

function formValue(form: FormData, key: string): string {
  const value = form.get(key);
  return typeof value === "string" ? value : "";
}
