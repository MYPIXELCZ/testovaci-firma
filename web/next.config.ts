import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Plánovač se servíruje jen přes /stahnout/[id] po zaplacení, proto leží v private/ a ne v public/.
  outputFileTracingIncludes: {
    "/stahnout/*": ["./private/**/*"],
  },
};

export default nextConfig;
