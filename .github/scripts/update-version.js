#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get the new version from semantic-release
const newVersion = process.env.NEXT_RELEASE_VERSION;

if (!newVersion) {
  console.error('NEXT_RELEASE_VERSION environment variable not set');
  process.exit(1);
}

// Update setup.py
const setupPath = path.join(process.cwd(), 'setup.py');
let setupContent = fs.readFileSync(setupPath, 'utf8');

// Update version in setup.py
setupContent = setupContent.replace(
  /version="[^"]*"/,
  `version="${newVersion}"`
);

fs.writeFileSync(setupPath, setupContent);
console.log(`Updated setup.py to version ${newVersion}`);