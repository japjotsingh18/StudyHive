import Link from "next/link";

export default function Home() {
  return (
    <main
      className="mx-auto flex min-h-screen w-full max-w-3xl items-center px-6 py-16"
      id="main-content"
    >
      <section aria-labelledby="page-title" className="space-y-5">
        <p className="text-sm font-medium text-[var(--color-accent)]">
          Secure authentication foundation
        </p>
        <h1
          className="text-4xl font-bold tracking-tight text-[var(--color-text-primary)]"
          id="page-title"
        >
          StudyHive
        </h1>
        <p className="max-w-2xl text-lg text-[var(--color-text-secondary)]">
          Create an account or sign in with the email/password provider.
          StudyHive keeps session secrets out of browser JavaScript and protects
          account routes by default.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link
            className="min-h-11 rounded-[var(--radius-control)] bg-[var(--color-action-primary)] px-5 py-2.5 font-semibold text-[var(--color-action-primary-text)]"
            href="/register"
          >
            Create account
          </Link>
          <Link
            className="min-h-11 rounded-[var(--radius-control)] border px-5 py-2.5 font-semibold"
            href="/login"
          >
            Sign in
          </Link>
        </div>
      </section>
    </main>
  );
}
