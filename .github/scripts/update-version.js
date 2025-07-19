#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get the new version from semantic-release
const newVersion = process.env.NEXT_RELEASE_VERSION;

if (!newVersion) {
  console.error('NEXT_RELEASE_VERSION environment variable not set');
  process.exit(1);
}

// Update pyproject.toml
const pyprojectPath = path.join(process.cwd(), 'pyproject.toml');
let pyprojectContent = fs.readFileSync(pyprojectPath, 'utf8');

// Update version in pyproject.toml
pyprojectContent = pyprojectContent.replace(
  /version = ".*"/,
  `version = "${newVersion}"`
);

fs.writeFileSync(pyprojectPath, pyprojectContent);
console.log(`Updated pyproject.toml to version ${newVersion}`);