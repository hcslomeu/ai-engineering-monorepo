Perform a quick code quality review of: $ARGUMENTS

## Checklist

Review the specified file(s) or module against these criteria:

### Type Safety
- [ ] All function parameters and return values have type hints
- [ ] No `Any` types unless justified
- [ ] Pydantic models used for structured data

### Code Quality
- [ ] Google-style docstrings on public functions/classes
- [ ] No teaching comments or AI-generated feel
- [ ] Clear variable and function names
- [ ] Single responsibility per module

### Error Handling
- [ ] External API calls have error handling
- [ ] User-facing errors are clear and actionable
- [ ] No bare `except:` clauses

### Testing
- [ ] Public functions have corresponding tests
- [ ] Edge cases are covered (empty input, None, error paths)
- [ ] Mocks used for external dependencies (API calls, databases)

### Security
- [ ] No hardcoded secrets or API keys
- [ ] `SecretStr` used for sensitive config values
- [ ] No command injection vectors

## Output

Present findings as:
- **Issues found** (with file:line references)
- **Suggested fixes** (concrete code changes)
- **Overall assessment** (1-2 sentences)

Do NOT apply fixes — present them for the user to decide.
