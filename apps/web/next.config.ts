import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  transpilePackages: ["@studyhive/ui"],
  typedRoutes: true,
};

export default nextConfig;
