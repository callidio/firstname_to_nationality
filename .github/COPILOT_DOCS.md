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

## Automated Version Management

This repository uses automated version management through GitHub Actions. See `.github/workflows/auto-version-bump.yml` for details.

### How It Works

1. Commits are analyzed for conventional commit format
2. Version bump type is determined (patch/minor/major)
3. `setup.py` is automatically updated
4. A new release is created on GitHub
5. Commit includes `[skip ci]` to prevent infinite loops

### Commit Message Format

Use conventional commits for automatic version bumping:

- `fix: description` → Patch version bump (1.0.0 → 1.0.1)
- `feat: description` → Minor version bump (1.0.0 → 1.1.0)
- `feat!: description` or `BREAKING CHANGE:` → Major version bump (1.0.0 → 2.0.0)
