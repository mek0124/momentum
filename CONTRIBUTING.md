# Contributing to Momentum

Thanks for taking the time to contribute.

Momentum values **clarity, simplicity, and restraint**.

---

## Getting Started

1. Fork the repo
2. Create a feature branch
3. Install dev dependencies:

```bash
pip install -e ".[dev]"
```

---

## Code Style

- Python: PEP8 + Black
- Avoid clever abstractions
- Prefer explicit code
- Comment intent, not mechanics

Run before committing:

```bash
black .
flake8 .
pytest
```

---

## What to Contribute

Good:
- Bug fixes
- UI polish
- Performance improvements
- Docs improvements
- Tests

Be cautious with:
- New dependencies
- Large frameworks
- Feature creep

---

## Commit Messages

Use clear, imperative messages:

```
Add task due date validation
Fix priority badge color contrast
```

---

## Issues

- One issue per PR
- Describe *why*, not just *what*
- Screenshots welcome for UI changes

---

## License

By contributing, you agree your work is MIT licensed.
