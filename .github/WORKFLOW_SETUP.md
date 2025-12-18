# GitHub Actions Workflow Setup Guide

This guide explains how to set up the auto-version-bump workflow to work properly with GitHub Actions.

## Problem

The error "GitHub Actions is not permitted to create or approve pull requests" occurs because GitHub's default `GITHUB_TOKEN` has security restrictions that prevent it from creating pull requests that would trigger other workflow runs. This is a deliberate security measure to prevent recursive workflow execution.

## Solutions

You have two options to fix this issue:

### Option 1: Personal Access Token (PAT) - Recommended for Most Users

This is the simpler approach and works well for most repositories.

#### Steps:

1. **Create a Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or use this direct link: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a descriptive name like "Auto Version Bump Workflow"
   - Set an appropriate expiration date
   - Select the following scopes:
     - ✅ `repo` (Full control of private repositories)
       - This includes `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, and `security_events`
     - ✅ `workflow` (Update GitHub Action workflows)
   - Click "Generate token" and **copy the token immediately** (you won't be able to see it again)

2. **Add the PAT as a Repository Secret**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PAT_TOKEN`
   - Value: Paste the token you just created
   - Click "Add secret"

3. **Done!** The workflow is already configured to use `PAT_TOKEN` if available.

#### Token Expiration

PATs expire, so you'll need to:
- Set a reminder to renew the token before expiration
- Generate a new token and update the secret when needed
- Consider using fine-grained tokens (see below) for better security and control

### Option 2: Fine-Grained Personal Access Token - More Secure

Fine-grained tokens are newer and provide better security with repository-specific access.

#### Steps:

1. **Create a Fine-Grained PAT**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Or use this direct link: https://github.com/settings/tokens?type=beta
   - Click "Generate new token"
   - Fill in the details:
     - **Token name**: "Auto Version Bump Workflow"
     - **Expiration**: Set your preferred expiration
     - **Repository access**: Select "Only select repositories" and choose this repository
     - **Permissions** → Repository permissions:
       - ✅ Contents: Read and write
       - ✅ Pull requests: Read and write
       - ✅ Metadata: Read (automatically selected)
       - ✅ Workflows: Read and write
   - Click "Generate token" and copy it

2. **Add as Repository Secret** (same as Option 1, step 2)

3. **Done!**

### Option 3: GitHub App - Most Secure for Organizations

This is the most secure option and recommended for organizations, but requires more setup.

#### Steps:

1. **Create a GitHub App**:
   - Go to Organization Settings → Developer settings → GitHub Apps
   - Or go to: https://github.com/organizations/YOUR_ORG/settings/apps/new
   - Fill in the basic information:
     - **GitHub App name**: "Auto Version Bump Bot"
     - **Homepage URL**: Your repository URL
     - **Webhook**: Uncheck "Active" (not needed)
   - Set **Repository permissions**:
     - Contents: Read & write
     - Pull requests: Read & write
     - Workflows: Read & write
   - Click "Create GitHub App"

2. **Install the GitHub App**:
   - After creation, click "Install App"
   - Select the repository to install it on
   - Click "Install"

3. **Generate a Private Key**:
   - In your GitHub App settings, scroll to "Private keys"
   - Click "Generate a private key"
   - Save the downloaded `.pem` file securely

4. **Add Secrets to Repository**:
   - `APP_ID`: Your GitHub App ID (found in the About section)
   - `APP_PRIVATE_KEY`: Content of the `.pem` file

5. **Update the Workflow**:
   - You'll need to use a GitHub Action that generates a token from the App credentials
   - See: https://github.com/marketplace/actions/create-github-app-token

## Testing the Workflow

After setting up the PAT:

1. Make a commit to the `main` branch (or trigger the workflow manually via workflow_dispatch)
2. The workflow should run and successfully create a PR
3. Check the Actions tab to see if the workflow completed without errors

## Troubleshooting

### Error: "Resource not accessible by integration"

This means the token doesn't have the required permissions. Double-check:
- The `repo` scope is enabled for classic PATs
- For fine-grained PATs, check that Contents, Pull Requests, and Workflows permissions are set to "Read and write"

### Error: "Bad credentials"

- The token might have expired
- The token might not be properly saved in the repository secrets
- Make sure you named the secret `PAT_TOKEN` (case-sensitive)

### Workflow still fails after adding PAT_TOKEN

1. Verify the secret exists: Repository Settings → Secrets and variables → Actions
2. Check that you copied the entire token without any extra spaces
3. Try regenerating the token and updating the secret
4. Make sure the workflow file is using `${{ secrets.PAT_TOKEN || secrets.GITHUB_TOKEN }}`

## Why This Is Necessary

GitHub's default `GITHUB_TOKEN` is scoped to prevent workflows from creating PRs that trigger other workflows. This security measure prevents:
- Infinite workflow loops
- Unauthorized workflow modifications
- Excessive Actions minutes usage

By using a PAT or GitHub App token, you explicitly grant permission for the workflow to create PRs that can trigger other workflows, while maintaining security through token management and expiration.

## Security Best Practices

1. **Use Fine-Grained Tokens** when possible for better security
2. **Set Short Expiration Times** (e.g., 90 days) and rotate tokens regularly
3. **Use GitHub Apps** for organization repositories
4. **Never Commit Tokens** to the repository
5. **Limit Token Scope** to only what's needed
6. **Use Repository Secrets** (never organization or environment secrets unless necessary)
7. **Audit Token Usage** regularly in GitHub's token settings

## Additional Resources

- [peter-evans/create-pull-request - Triggering Further Workflow Runs](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#triggering-further-workflow-runs)
- [GitHub Docs - Creating a Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub Docs - Automatic Token Authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [GitHub Apps Documentation](https://docs.github.com/en/apps)
