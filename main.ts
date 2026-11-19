// Entry for make.fun's "Sum up 19 November's world news in one image".
//
// The picture itself sits beside this file as entry.png: a front-page
// poster of Thursday 19 November 2026, drawn from the day's headlines by
// the build tool in poster.py. The grader runs this program twice,
// with no network, and both runs must write the same bytes, so the program
// does the simplest deterministic thing there is: it copies the picture,
// untouched, into the output directory under the name entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

function main(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const source = new URL("./entry.png", import.meta.url);
  const target = join(outDir, "entry.png");
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);
  // One line of proof in the run log: the copy landed whole.
  console.log(`entry.png written: ${statSync(target).size} bytes`);
}

main();
