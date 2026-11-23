// Hash van bron.md: de single source of truth van een deck. Zelfde berekening als scripts/parse_bron.py hash.
// sha256 over de UTF-8-tekst met \r\n → \n, zodat Windows/Unix-checkouts dezelfde hash geven.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

export function bronHash(file) {
  const text = readFileSync(file, 'utf8').replace(/^﻿/, '').replace(/\r\n/g, '\n');
  return 'sha256:' + createHash('sha256').update(text, 'utf8').digest('hex').slice(0, 16);
}

/** bron.md naast een HTML-deck of deck-spec; null als die er niet is. */
export function bronNaast(file) {
  const p = join(dirname(file), 'bron.md');
  return existsSync(p) ? p : null;
}
