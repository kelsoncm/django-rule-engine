# Publishing to PyPI

This guide explains how to publish `django-rule-engine` to PyPI using GitHub Actions.

## Prerequisites

### 1. Configure PyPI Trusted Publishing

Instead of using API tokens, we use PyPI's Trusted Publishers feature for secure, token-free publishing.

#### Steps:

1. Go to https://pypi.org/ and log in
2. Navigate to your account settings
3. Go to "Publishing" section
4. Click "Add a new pending publisher"
5. Fill in the form:
   - **PyPI Project Name:** `django-rule-engine`
   - **Owner:** `kelsoncm`
   - **Repository name:** `django-rule-engine` (or your repository name)
   - **Workflow name:** `publish-to-pypi.yml`
   - **Environment name:** `pypi`
6. Click "Add"

#### For TestPyPI (optional, for testing):

Repeat the same steps on https://test.pypi.org/

## Publishing Methods

### Method 1: Automatic Publishing on Release (Recommended)

This is the easiest way to publish. Creating a GitHub Release will automatically trigger the publish workflow.

1. Go to your GitHub repository
2. Click on "Releases" → "Create a new release"
3. Create a new tag (e.g., `v1.0.0`)
4. Fill in the release title and description
5. Click "Publish release"

The GitHub Action will automatically:
- Build the package
- Publish to PyPI
- The package will be available at https://pypi.org/project/django-rule-engine/

### Method 2: Manual Workflow Trigger

You can manually trigger the workflow from GitHub Actions tab.

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Publish to PyPI" workflow
4. Click "Run workflow"
5. Choose:
   - **test_pypi**: `false` for production PyPI, `true` for TestPyPI
6. Click "Run workflow"

## Version Management

Update the version number in `pyproject.toml`:

```toml
[project]
version = "1.0.0"  # Change this
```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for bug fixes (backwards compatible)

## Testing Before Publishing

### Test Locally

Build and check the package locally:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Test installation locally
pip install dist/django_rule_engine-1.0.0-py3-none-any.whl
```

### Test on TestPyPI

1. Run workflow manually with `test_pypi: true`
2. Install from TestPyPI to verify:

```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    django-rule-engine
```

Note: `--extra-index-url` is needed because dependencies are on main PyPI.

## Workflow Details

### Files Created

- `.github/workflows/publish-to-pypi.yml` - Main publishing workflow
- `.github/workflows/test.yml` - Testing workflow
- `pyproject.toml` - Modern Python project configuration
- `PUBLISHING.md` - This guide

### What the Workflow Does

1. **Build Job:**
   - Checks out the code
   - Sets up Python
   - Installs build tools
   - Builds wheel and source distribution
   - Uploads artifacts

2. **Publish Job:**
   - Downloads built packages
   - Publishes to PyPI using Trusted Publishing
   - No tokens or passwords needed!

### Workflow Triggers

- **On Release:** Automatically publishes to PyPI
- **Manual Trigger:** Can publish to PyPI or TestPyPI on demand

## Troubleshooting

### Package Already Exists

If you see "File already exists" error:
- You cannot re-upload the same version
- Bump the version in `pyproject.toml`
- Create a new release

### Trusted Publishing Not Working

If you get authentication errors:
1. Verify the publisher configuration on PyPI
2. Check the workflow name matches exactly: `publish-to-pypi.yml`
3. Ensure the environment name is `pypi`
4. Check repository and owner names are correct

### Build Fails

If the build fails:
1. Check `pyproject.toml` syntax
2. Verify all required files exist (README.md, LICENSE, etc.)
3. Check the build logs in GitHub Actions

## Security Notes

- ✅ **No API tokens needed** - Uses OpenID Connect (OIDC) trusted publishing
- ✅ **Automatic token generation** - GitHub generates short-lived tokens
- ✅ **Environment protection** - Can require approvals before publishing
- ✅ **Audit trail** - All publishes are logged

## GitHub Environment Configuration (Optional)

For additional security, configure environment protection rules:

1. Go to Settings → Environments → Create "pypi" environment
2. Add protection rules:
   - Required reviewers
   - Wait timer
   - Deployment branches

## Useful Links

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Python Packaging Guide](https://packaging.python.org/)
- [GitHub Actions for Publishing](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Semantic Versioning](https://semver.org/)

## Quick Checklist

Before publishing:

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG (if you have one)
- [ ] Test package builds locally
- [ ] Configure Trusted Publisher on PyPI
- [ ] Create GitHub Release or trigger workflow manually
- [ ] Verify package on PyPI
- [ ] Test installation: `pip install django-rule-engine`
