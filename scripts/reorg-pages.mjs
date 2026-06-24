// Post-build: make the portfolio the site root and move ComplyScope under /complyscope/.
// Vite builds ComplyScope to dist/ root and copies public/ (which includes the
// portfolio at public/portfolio). After build we:
//   1. move every root build artifact (ComplyScope) into dist/complyscope/
//   2. lift dist/portfolio/* up to dist/ root (so the portfolio is served at /)
// ComplyScope uses a relative base ('./') and HashRouter, so it works fine at /complyscope/.
import { promises as fs } from 'node:fs';
import path from 'node:path';

const dist = path.resolve('dist');
const csDir = path.join(dist, 'complyscope');
const portfolioDir = path.join(dist, 'portfolio');

const exists = async (p) => { try { await fs.access(p); return true; } catch { return false; } };

if (!(await exists(portfolioDir))) {
  console.error('reorg-pages: dist/portfolio not found; skipping reorg.');
  process.exit(0);
}

// 1) Move ComplyScope (everything at root except the portfolio + target folder) into dist/complyscope/
await fs.mkdir(csDir, { recursive: true });
for (const name of await fs.readdir(dist)) {
  if (name === 'portfolio' || name === 'complyscope') continue;
  await fs.rename(path.join(dist, name), path.join(csDir, name));
}
// The Vite entry is index.vite.html — serve it as complyscope/index.html
if (await exists(path.join(csDir, 'index.vite.html'))) {
  await fs.rename(path.join(csDir, 'index.vite.html'), path.join(csDir, 'index.html'));
}

// 2) Lift the portfolio up to the site root
for (const name of await fs.readdir(portfolioDir)) {
  await fs.rename(path.join(portfolioDir, name), path.join(dist, name));
}
await fs.rmdir(portfolioDir);

console.log('reorg-pages: portfolio -> /, ComplyScope -> /complyscope/');
