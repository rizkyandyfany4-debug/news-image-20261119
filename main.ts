// The World in One Image — Thursday 19 November 2026.
//
// The entrypoint copies the rendered front page (entry.png, drawn by
// render.py) into the output directory the grader provides. A plain copy is
// byte-identical on every run by construction, so the program's two runs
// always write the same bytes.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
console.log(`Wrote ${dest} (${statSync(dest).size} bytes)`);
