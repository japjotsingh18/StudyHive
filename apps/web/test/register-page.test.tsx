import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import RegisterPage from "@/app/register/page";

const router = vi.hoisted(() => ({ push: vi.fn(), refresh: vi.fn() }));

vi.mock("next/navigation", () => ({ useRouter: () => router }));

describe("registration page", () => {
  it("shows password guidance before submission", () => {
    render(<RegisterPage />);

    expect(screen.getByText(/Use at least 12 characters/)).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toHaveAttribute(
      "minlength",
      "12",
    );
  });

  it("requires both versioned policy acknowledgements", () => {
    render(<RegisterPage />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "student@example.edu" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "a sufficiently long password" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Create account" }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "Accept the Terms of Service and Privacy Policy",
    );
  });
});
