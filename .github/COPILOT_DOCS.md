# GitHub Copilot Coding Agent Documentation

This file provides information about configuring automated tools for the firstname_to_nationality repository.

## Dependabot Configuration

To get started with Dependabot version updates, you'll need to specify which package ecosystems to update and where the package manifests are located.

Please see the documentation for all configuration options:
https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file

### Current Configuration

The repository uses the following Dependabot configuration in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Monitor pip dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "python"
    commit-message:
      prefix: "chore"
      include: "scope"
  
  # Monitor GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "chore"
      include: "scope"
```

## Package Ecosystems

### Supported Ecosystems

Dependabot supports the following package ecosystems:

- **pip** - Python dependencies (requirements.txt, setup.py)
- **npm** - JavaScript/Node.js dependencies (package.json)
- **github-actions** - GitHub Actions in workflow files
- **docker** - Docker images in Dockerfiles
- **composer** - PHP dependencies (composer.json)
- **bundler** - Ruby dependencies (Gemfile)
- **maven** - Java dependencies (pom.xml)
- **gradle** - Java/Kotlin dependencies (build.gradle)
- **cargo** - Rust dependencies (Cargo.toml)
- **go** - Go modules (go.mod)
- **nuget** - .NET dependencies (*.csproj)
- **terraform** - Terraform modules

### Current Repository Configuration

This repository uses:
- **pip** for Python dependencies
- **github-actions** for workflow dependencies

### Adding New Ecosystems

To add monitoring for a new package ecosystem, add a new entry to the `updates` array:

```yaml
- package-ecosystem: "" # See documentation for possible values
  directory: "/" # Location of package manifests
  schedule:
    interval: "weekly"
```

## Additional Resources

- [Dependabot Documentation](https://docs.github.com/code-security/dependabot)
- [GitHub Copilot Documentation](https://gh.io/copilot-coding-agent-docs)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## Automated Version Management & Releases

This repository uses fully automated version management and release creation through GitHub Actions.

### Automated Workflows

1. **Version Bumping** (`.github/workflows/auto-version-bump.yml`)
   - Commits are analyzed for conventional commit format
   - Version bump type is determined (patch/minor/major)
   - `setup.py` is automatically updated
   - Changes are committed directly to main branch
   - A git tag is created and pushed (e.g., `1.2.3`)

2. **Release Creation** (`.github/workflows/release.yml`)
   - Automatically triggered when a tag is pushed
   - Creates a GitHub release with the tag
   - Generates release notes using GitHub's AI-powered feature
   - Release notes include all commits since the previous release

3. **PyPI Publishing** (`.github/workflows/publish.yml`)
   - Automatically triggered when a release is created
   - Builds and publishes the package to PyPI

### Complete Flow

```
Push to main → Auto version bump → Create tag → Auto release → Publish to PyPI
```

### Commit Message Format

Use conventional commits for automatic version bumping:

- `fix: description` → Patch version bump (1.0.0 → 1.0.1)
- `feat: description` → Minor version bump (1.0.0 → 1.1.0)
- `feat!: description` or `BREAKING CHANGE:` → Major version bump (1.0.0 → 2.0.0)
