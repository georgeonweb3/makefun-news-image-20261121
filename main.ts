// news-image-20261121 entry, written for Node 22 with only the
// standard library.
//
// The front page is already drawn: entry.png sits next to this file,
// produced by draw.py (Python + Pillow, every pixel code-drawn, no
// photos). All this program has to do is deliver that exact file to
// the grader, untouched.
//
// The grader runs the program in a fresh container where the output
// directory is /output. When I run it by hand outside that container
// I point MAKEFUN_OUTPUT_DIR at a scratch folder instead:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const pngBesideScript = join(scriptDir, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destination = join(outDir, 'entry.png');

// I read the whole PNG into memory, create the output directory if it
// is not there yet, write the bytes back out, and then confirm the
// file on disk is exactly as long as the one I read. If the sizes
// ever disagree the program fails loudly instead of handing the judge
// a truncated image.

const pngBytes = readFileSync(pngBesideScript);
mkdirSync(outDir, { recursive: true });
writeFileSync(destination, pngBytes);

const bytesOnDisk = statSync(destination).size;
if (bytesOnDisk !== pngBytes.length) {
  throw new Error(
    `entry.png did not copy whole: ${bytesOnDisk} of ${pngBytes.length} bytes on disk`,
  );
}
console.log(`wrote entry.png (${pngBytes.length} bytes) to ${destination}`);
