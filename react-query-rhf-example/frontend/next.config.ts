import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // La API de ejemplo corre en el puerto 8000. Ajustá la URL según tu entorno.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },
};

export default nextConfig;