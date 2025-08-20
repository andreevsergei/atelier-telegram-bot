import sharp from "sharp";
import path from "node:path";
import fs from "node:fs";

async function ensureDir(dirPath: string): Promise<void> {
	await fs.promises.mkdir(dirPath, { recursive: true });
}

async function main(): Promise<void> {
	const projectRoot = path.resolve(__dirname, "..");
	const publicIconsDir = path.join(projectRoot, "public", "icons");
	await ensureDir(publicIconsDir);

	const sourceSvg = path.join(projectRoot, "public", "next.svg");
	const icon192Path = path.join(publicIconsDir, "icon-192.png");
	const icon512Path = path.join(publicIconsDir, "icon-512.png");

	const buffer = await fs.promises.readFile(sourceSvg);

	await sharp(buffer).resize(192, 192).png().toFile(icon192Path);
	await sharp(buffer).resize(512, 512).png().toFile(icon512Path);

	// Also emit maskable variants for better Android experience
	const icon192Maskable = path.join(publicIconsDir, "icon-192-maskable.png");
	const icon512Maskable = path.join(publicIconsDir, "icon-512-maskable.png");
	await sharp(buffer)
		.resize(192, 192)
		.png({ progressive: true })
		.extend({ top: 24, bottom: 24, left: 24, right: 24, background: { r: 17, g: 24, b: 39, alpha: 1 } })
		.resize(192, 192)
		.toFile(icon192Maskable);
	await sharp(buffer)
		.resize(512, 512)
		.png({ progressive: true })
		.extend({ top: 64, bottom: 64, left: 64, right: 64, background: { r: 17, g: 24, b: 39, alpha: 1 } })
		.resize(512, 512)
		.toFile(icon512Maskable);

	console.log("Generated:");
	console.log(" -", path.relative(projectRoot, icon192Path));
	console.log(" -", path.relative(projectRoot, icon512Path));
	console.log(" -", path.relative(projectRoot, icon192Maskable));
	console.log(" -", path.relative(projectRoot, icon512Maskable));
}

main().catch((error: unknown) => {
	console.error(error);
	process.exit(1);
});