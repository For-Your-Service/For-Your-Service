# Versioning Strategy

## Semantic Versioning

For Your Service follows [SemVer 2.0.0](https://semver.org/)

**Format:** MAJOR.MINOR.PATCH

- **MAJOR:** Breaking changes to API
- **MINOR:** Backwards-compatible new features
- **PATCH:** Backwards-compatible bug fixes

---

## Version History

### v0.1.0 (2026-08-10)
- Initial release
- Bronze layer ingestion
- Core documentation

### v0.2.0 (Planned: Sep 2026)
- Silver layer enrichment
- O*NET integration
- MOS crosswalk

### v1.0.0 (Planned: Q4 2026)
- Production-ready API
- Neural matching engine
- Hugging Face deployment

---

## Git Tags

We use Git tags for releases:

```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

---

## Branch Strategy

- **main:** Production-ready code
- **develop:** Integration branch
- **feature/*:** New features
- **bugfix/*:** Bug fixes
- **release/*:** Release preparation

---

## Release Process

1. **Feature freeze** on develop
2. Create **release branch**
3. **Testing** and bug fixes
4. **Update** CHANGELOG.md
5. **Merge** to main
6. **Tag** version
7. **Deploy** to production
8. **Merge back** to develop

---

## Deprecation Policy

- Features marked deprecated: 2 minor versions before removal
- API changes: 1 major version advance notice
- Security patches: Immediate, no deprecation

---

## Compatibility

### Backwards Compatibility
- Maintained for MINOR and PATCH versions
- Breaking changes only in MAJOR versions

### Forward Compatibility
- Not guaranteed
- Use latest stable version

---

## Version Support

| Version | Status | Support Until |
|---------|--------|---------------|
| 0.1.x | Current | Dec 2026 |
| 0.2.x | Planned | Mar 2027 |
| 1.0.x | Future | TBD |

---

Questions? See [SUPPORT.md](SUPPORT.md)
