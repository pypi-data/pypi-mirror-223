# Publish a new release

A gitlab CI/CD handle the build of the release archives, and push them to Gitlab Package Registry, PyPI and Github Releases.
To trigger it, we just need to:

1. update the version in pyproject.toml
2. update the changelog
3. git commit
4. git tag
5. git push
6. git push --tags


For this, an helper script is provided:

```bash
./docs/release.sh x.y.z
```
