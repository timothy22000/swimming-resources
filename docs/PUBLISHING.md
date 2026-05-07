# Publishing Guide

This guide publishes the Swimming Resources Database to GitHub and Hugging
Face. The canonical owners are `timothy22000` on GitHub and `t22000t` on
Hugging Face; substitute your own accounts if you are publishing a fork.

## 1. Final Local Checks

Run the build and confirm the generated files are present:

```bash
python -m pip install --upgrade pandas pyarrow
python scripts/build_dataset.py
ls data/swimming_resources.json data/swimming_resources.jsonl data/swimming_resources.csv data/swimming_resources.parquet data/schema.json
```

Review the release files:

```bash
ls LICENSE LICENSE-CODE CODE_OF_CONDUCT.md CHANGELOG.md README.md CONTRIBUTING.md
ls .github/workflows/validate.yml .github/workflows/link-check.yml
ls .github/PULL_REQUEST_TEMPLATE.md .github/ISSUE_TEMPLATE/
ls huggingface/README.md docs/PUBLISHING.md
```

## 2. Create and Push the GitHub Repository

If this directory is not already a git repository, initialize it:

```bash
git init
git branch -M main
git add .
git commit -m "Release swimming resources database v1.0.0"
```

Create the repository and push:

```bash
gh auth login
gh repo create timothy22000/swimming-resources --public --source=. --remote=origin --push
```

Add the initial release tag:

```bash
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 \
  --title "Swimming Resources Database v1.0.0" \
  --notes "Initial release: 410 verified swimming resources across 20 categories."
```

After the push, open the Actions tab and confirm that `Validate dataset` passes.
You can run `Link check` manually once before announcing the dataset.

## 3. Create the Hugging Face Dataset Repo

Install the Hugging Face CLI and log in:

```bash
python -m pip install --upgrade huggingface_hub
huggingface-cli login
```

Create the dataset repository:

```bash
huggingface-cli repo create swimming-resources --type dataset
```

Clone it locally:

```bash
git clone https://huggingface.co/datasets/t22000t/swimming-resources hf-swimming-resources
cd hf-swimming-resources
```

Copy the dataset card and Parquet file from this repository:

```bash
cp ../huggingface/README.md README.md
cp ../data/swimming_resources.parquet swimming_resources.parquet
```

If the Parquet file is large enough to require Git LFS, enable it before
committing:

```bash
git lfs install
git lfs track "*.parquet"
git add .gitattributes
```

Commit and push:

```bash
git add README.md swimming_resources.parquet
git commit -m "Add swimming resources dataset v1.0.0"
git push
```

## 4. Owner References (for forks)

This repository hard-codes the canonical owners:

- `timothy22000` for GitHub references in `README.md`, `CHANGELOG.md`,
  `data/swimming_resources.json`, `data/schema.json`, and the link-check
  workflow user-agent string.
- `t22000t` for Hugging Face references in `README.md` and
  `huggingface/README.md`.

If you fork the repository under different accounts, update those values and
re-run `python scripts/build_dataset.py` so the canonical JSON metadata is
regenerated with your homepage URL.

## 5. Release Checklist

- [ ] GitHub repository is public.
- [ ] `v1.0.0` tag and GitHub release exist.
- [ ] `Validate dataset` passes on `main`.
- [ ] `Link check` has been run at least once.
- [ ] Hugging Face dataset page loads and `load_dataset("t22000t/swimming-resources")` works.
- [ ] README links point to the final GitHub and Hugging Face URLs.
- [ ] No generated commit metadata includes AI co-author trailers.
