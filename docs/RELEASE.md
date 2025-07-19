# Automated Release Process

This project uses [semantic-release](https://semantic-release.gitbook.io/) to automate the release process based on conventional commits.

## How It Works

1. **Commit Analysis**: When you push to the `main` branch, the GitHub Actions workflow analyzes your commit messages
2. **Version Determination**: Based on the commit types, it determines the next version:
   - `feat:` commits trigger a minor version bump (1.0.0 → 1.1.0)
   - `fix:` commits trigger a patch version bump (1.0.0 → 1.0.1)
   - `BREAKING CHANGE:` in commit body triggers a major version bump (1.0.0 → 2.0.0)
3. **Release Creation**: Automatically creates a GitHub release with generated release notes
4. **Changelog Update**: Updates CHANGELOG.md with all changes
5. **Version Update**: Updates the version in pyproject.toml

## Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature (minor version bump)
- **fix**: A bug fix (patch version bump)
- **docs**: Documentation only changes (no release)
- **style**: Changes that don't affect code meaning (no release)
- **refactor**: Code change that neither fixes a bug nor adds a feature (patch version bump)
- **perf**: Performance improvement (patch version bump)
- **test**: Adding missing tests (no release)
- **chore**: Changes to build process or auxiliary tools (no release)

### Breaking Changes

To indicate a breaking change, add `BREAKING CHANGE:` in the commit body:

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

## Examples

### Feature Release (Minor Version)
```bash
git commit -m "feat: add support for Python 3.12"
```

### Bug Fix Release (Patch Version)
```bash
git commit -m "fix: correct indentation calculation for nested strings"
```

### Breaking Change Release (Major Version)
```bash
git commit -m "feat!: rename fix-file command to fix

BREAKING CHANGE: The CLI command 'fix-file' has been renamed to 'fix' for consistency"
```

### No Release
```bash
git commit -m "chore: update dependencies"
git commit -m "docs: improve README examples"
git commit -m "style: format code with black"
```

## Manual Release

If you need to trigger a release manually:

1. Ensure all changes are committed
2. Push to the main branch
3. The GitHub Actions workflow will handle the rest

## Configuration

- `.releaserc.json`: Configures semantic-release behavior
- `.github/workflows/release.yml`: GitHub Actions workflow
- `.github/scripts/update-version.js`: Updates version in pyproject.toml

## Troubleshooting

If a release fails:

1. Check the GitHub Actions logs
2. Ensure your commit messages follow the conventional format
3. Verify that the GITHUB_TOKEN has proper permissions
4. Check that the branch protection rules allow the workflow to push