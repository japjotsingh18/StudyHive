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
import { AuthApiError, register } from "@/lib/auth-api";

export default function RegisterPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<AuthApiError | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    const form = new FormData(event.currentTarget);
    if (form.get("terms") !== "on" || form.get("privacy") !== "on") {
      setError(
        new AuthApiError(
          "Accept the Terms of Service and Privacy Policy to create an account.",
          "policy_acknowledgement_required",
          422,
          null,
        ),
      );
      return;
    }
    setIsSubmitting(true);
    try {
      await register({
        email: formValue(form, "email"),
        password: formValue(form, "password"),
      });
      router.push("/account");
      router.refresh();
    } catch (caughtError) {
      setError(
        caughtError instanceof AuthApiError
          ? caughtError
          : new AuthApiError(
              "StudyHive could not create the account. Try again.",
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
      description="Create your identity now. University verification and profile onboarding follow in the next approved phase."
      title="Create your account"
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
          autoComplete="new-password"
          hint="Use at least 12 characters. Avoid common passwords and words from your email."
          id="password"
          label="Password"
          minLength={12}
          name="password"
          required
          type="password"
        />
        <fieldset className="space-y-3">
          <legend className="text-sm font-semibold">Required policies</legend>
          <label className="flex gap-3 text-sm" htmlFor="terms">
            <input id="terms" name="terms" required type="checkbox" />
            <span>I accept the current Terms of Service.</span>
          </label>
          <label className="flex gap-3 text-sm" htmlFor="privacy">
            <input id="privacy" name="privacy" required type="checkbox" />
            <span>I accept the current Privacy Policy.</span>
          </label>
        </fieldset>
        <PrimaryButton disabled={isSubmitting}>
          {isSubmitting ? "Creating account…" : "Create account"}
        </PrimaryButton>
      </form>
      <p className="mt-6 text-center text-sm text-[var(--color-text-secondary)]">
        Already have an account?{" "}
        <Link
          className="font-semibold text-[var(--color-accent)] underline"
          href="/login"
        >
          Sign in
        </Link>
      </p>
    </AuthShell>
  );
}

function formValue(form: FormData, key: string): string {
  const value = form.get(key);
  return typeof value === "string" ? value : "";
}
