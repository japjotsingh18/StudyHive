import Link from "next/link";
import type { ReactNode } from "react";

interface AuthShellProps {
  children: ReactNode;
  description: string;
  title: string;
}

export function AuthShell({ children, description, title }: AuthShellProps) {
  return (
    <main
      className="mx-auto flex min-h-screen w-full max-w-lg items-center px-6 py-12"
      id="main-content"
    >
      <div className="w-full space-y-8">
        <Link
          className="inline-flex text-lg font-bold tracking-tight text-[var(--color-text-primary)]"
          href="/"
        >
          StudyHive
        </Link>
        <section
          aria-labelledby="auth-title"
          className="rounded-[var(--radius-surface)] border bg-[var(--color-surface)] p-6 shadow-sm sm:p-8"
        >
          <div className="mb-6 space-y-2">
            <h1 className="text-2xl font-bold tracking-tight" id="auth-title">
              {title}
            </h1>
            <p className="text-sm leading-6 text-[var(--color-text-secondary)]">
              {description}
            </p>
          </div>
          {children}
        </section>
      </div>
    </main>
  );
}
