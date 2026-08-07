import type { InputHTMLAttributes, ReactNode } from "react";

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  hint?: ReactNode;
  label: string;
}

export function Field({ hint, id, label, ...inputProps }: FieldProps) {
  const hintId = hint === undefined ? undefined : `${id}-hint`;
  return (
    <div className="space-y-2">
      <label className="block text-sm font-semibold" htmlFor={id}>
        {label}
      </label>
      <input
        {...inputProps}
        aria-describedby={hintId}
        className="min-h-11 w-full rounded-[var(--radius-control)] border bg-[var(--color-canvas)] px-3 py-2 text-base"
        id={id}
      />
      {hint === undefined ? null : (
        <p className="text-sm text-[var(--color-text-secondary)]" id={hintId}>
          {hint}
        </p>
      )}
    </div>
  );
}

interface FormErrorProps {
  message: string | null;
  requestId?: string | null;
}

export function FormError({ message, requestId }: FormErrorProps) {
  if (message === null) {
    return null;
  }
  return (
    <div
      aria-live="polite"
      className="rounded-[var(--radius-control)] border border-[var(--color-danger)] bg-[var(--color-danger-subtle)] p-3 text-sm"
      role="alert"
    >
      <p>{message}</p>
      {requestId === null || requestId === undefined ? null : (
        <details className="mt-2 text-[var(--color-text-secondary)]">
          <summary>Support details</summary>
          <p className="mt-1 font-mono text-xs">Request ID: {requestId}</p>
        </details>
      )}
    </div>
  );
}

export function PrimaryButton({
  children,
  disabled,
}: {
  children: ReactNode;
  disabled: boolean;
}) {
  return (
    <button
      className="min-h-11 w-full rounded-[var(--radius-control)] bg-[var(--color-action-primary)] px-4 py-2 font-semibold text-[var(--color-action-primary-text)] disabled:cursor-not-allowed disabled:opacity-60"
      disabled={disabled}
      type="submit"
    >
      {children}
    </button>
  );
}
