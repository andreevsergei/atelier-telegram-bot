import type { MetadataRoute } from "next";

export const dynamic = 'force-static';

export default function manifest(): MetadataRoute.Manifest {
	return {
		name: "Next App",
		short_name: "NextApp",
		description: "Installed Next.js application",
		start_url: "/",
		display: "standalone",
		background_color: "#ffffff",
		theme_color: "#111827",
		icons: [
			{ src: "/icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
			{ src: "/icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
			{ src: "/icons/icon-192-maskable.png", sizes: "192x192", type: "image/png", purpose: "maskable" },
			{ src: "/icons/icon-512-maskable.png", sizes: "512x512", type: "image/png", purpose: "maskable" }
		]
	};
}

