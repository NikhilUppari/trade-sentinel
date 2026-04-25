# Publish to GitHub

Recommended repository name:

```text
trade-sentinel
```

## Option 1: GitHub Website

1. Go to <https://github.com/new>.
2. Repository owner: `NikhilUppari`.
3. Repository name: `trade-sentinel`.
4. Choose Public or Private.
5. Do not add a README, license, or `.gitignore`; this project already has them.
6. Create the repository.

Then run these commands from the project folder:

```bash
git init -b main
git add .
git commit -m "Initial Trade Sentinel project"
git remote add origin https://github.com/NikhilUppari/trade-sentinel.git
git push -u origin main
```

## Option 2: GitHub CLI

If you install GitHub CLI:

```bash
gh repo create NikhilUppari/trade-sentinel --public --source=. --remote=origin --push
```

Use `--private` instead of `--public` if you want the repository hidden.
