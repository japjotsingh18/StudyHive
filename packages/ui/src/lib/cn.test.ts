import { describe, expect, it } from "vitest";

import { cn } from "./cn";

describe("cn", () => {
  it("resolves conflicting Tailwind classes", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
  });
});
