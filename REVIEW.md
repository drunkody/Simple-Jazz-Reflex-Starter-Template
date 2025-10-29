# Code Review Checklist

This document outlines critical areas to review in the Jazz + Reflex Starter Template.

## Critical Areas to Review

### 1. **GitHub Actions Workflows** ⚠️ HIGH PRIORITY

We just fixed major YAML syntax errors. Verify:
- `.github/workflows/deploy.yml` - Check indentation is correct (2 spaces)
- `.github/workflows/tests.yml` - Same indentation check
- **Secret handling**: `REFLEX_API_KEY` and `CODECOV_TOKEN` need to be configured in GitHub
- Test the workflows on a non-main branch first to avoid breaking CI

### 2. **Security Issues** 🔒

- **`app/state.py:79`** - ID generation using `len(self.notes) + 1` creates collision risk after deletions
- **No input validation** - Users can submit unlimited content length
- **Generic exception catching** - Could hide critical errors silently

### 3. **Jazz Integration is Fake** 🎭

- **`app/state.py:56-67`** - Just calls `asyncio.sleep(0.5)`, doesn't actually use Jazz
- **`app/jazz/schema.ts`** - 122 lines of TypeScript schemas that are never used
- Decision needed: Implement Jazz properly or remove the mock?

### 4. **Type Safety Issues**

- **`app/state.py:116`** - `on_load()` typed as `-> None` but returns a callable
- Missing return type hints on several methods (lines 46-51, 95-107, 109-115)

### 5. **Dead/Commented Code**

- **`rxconfig.py:10-13`** - Commented Jazz packages
- **`rxconfig.py:16`** - Commented database URL
- Should these be removed or implemented?

### 6. **Dependencies & Versions**

- `reflex>=0.4.0` - Is this the right version constraint?
- **`package.json`** uses `"latest"` for jazz-tools/jazz-react/cojson - risky for reproducibility

### 7. **Nix Flake Configuration**

- **`flake.nix`** - Review the Python and Node.js versions
- Check if all necessary packages are included for your use case

## Quick Review Checklist

- [ ] Run workflows on test branch first
- [ ] Decide: Implement Jazz or remove mock?
- [ ] Fix ID generation security issue
- [ ] Add input validation (max lengths)
- [ ] Fix type hints
- [ ] Clean up commented code
- [ ] Pin dependency versions in package.json

## Testing Before Merge

**Most important**: Test the GitHub Actions workflows before merging to main.

1. Create a test branch
2. Push changes and verify CI passes
3. Check all jobs complete successfully
4. Review any warnings or errors

## Architecture Decisions Needed

### Jazz Integration
**Current State**: Mocked with `asyncio.sleep()`  
**Options**:
1. Implement actual Jazz integration with WebSocket bridge
2. Remove Jazz mock and use local-only storage
3. Keep as template and document clearly

### Type System
**Current State**: Missing return types, wrong annotations  
**Action**: Add complete type hints for better IDE support and catching errors

### ID Generation
**Current State**: Fragile length-based IDs  
**Action**: Switch to UUID or proper auto-increment counter

## Security Review

### Input Validation
- [ ] Add maximum title length (e.g., 200 chars)
- [ ] Add maximum content length (e.g., 10000 chars)
- [ ] Add rate limiting for note creation
- [ ] Sanitize user input to prevent XSS

### Exception Handling
- [ ] Replace generic `except Exception` with specific exceptions
- [ ] Add user-facing error messages
- [ ] Don't catch system errors (KeyboardInterrupt, SystemExit)

### Secrets Management
- [ ] Verify `REFLEX_API_KEY` is set in GitHub Secrets
- [ ] Verify `CODECOV_TOKEN` is set in GitHub Secrets (optional)
- [ ] Ensure no secrets are logged or committed

## Performance Considerations

### State Management
- Note list grows indefinitely without pagination
- No cleanup of old completed notes
- Consider adding note limits or archiving

### Frontend
- No lazy loading for large note lists
- All notes rendered at once
- Consider virtualization for 100+ notes

## Documentation Review

- [ ] README.md accurately describes features
- [ ] All setup steps are correct and tested
- [ ] IMPROVE.md lists all known issues
- [ ] Examples work as documented

## CI/CD Pipeline

### GitHub Actions
- [ ] Test workflow runs on pull requests
- [ ] Lint workflow catches style issues
- [ ] TypeScript check validates schemas
- [ ] Coverage reports upload correctly
- [ ] Deploy workflow has proper environment variables

### Local Development
- [ ] `make install` works correctly
- [ ] `make run` starts the app
- [ ] `make test` passes all tests
- [ ] `make lint` catches issues
- [ ] Nix flake provides complete dev environment
