# Contributing

Thanks for considering a contribution. The Swimming Resources Database is
intended to be the most accurate, comprehensive, and well-maintained
open-source index of swimming resources. Every correction or addition makes
the dataset more useful for athletes, coaches, researchers, and ML systems.

This is an open community project. Please be respectful - see the
[Code of Conduct](CODE_OF_CONDUCT.md).

## What we accept

- **New resources** that fit one of the 20 categories.
- **Corrections** to existing entries (URLs, names, statuses, descriptions).
- **Rebrand and defunct flags** when an organization or product changes.
- **Translations** of `description` and `notes` (open an issue first to
  discuss schema changes for multi-language fields).
- **New categories** - open an issue first to discuss.

## What we do *not* accept

- Pure marketing content. Resources must serve athletes, coaches, or
  researchers; pay-to-list is not acceptable.
- Unverifiable resources. URLs must resolve and the resource must demonstrably
  exist as described.
- Duplicate or near-duplicate entries.

## The contribution workflow

Edit the source-of-truth Python files. **Do not edit `data/*.json`,
`data/*.jsonl`, `data/*.csv`, or `data/*.parquet` directly** - those files are
generated.

```bash
# 1. Fork & clone
git clone https://github.com/<your-fork>/swimming-resources.git
cd swimming-resources

# 2. Branch
git checkout -b add-resource-<short-name>

# 3. Edit the appropriate scripts/data_partN.py file
#    (each part owns one or more categories - check the file header)

# 4. Install build deps (only once)
pip install pandas pyarrow

# 5. Run the build - must exit 0 with no validation errors
python scripts/build_dataset.py

# 6. Commit the source change AND the regenerated data files together
git add scripts/data_partN.py data/
git commit -m "Add <Resource Name> to <category>"
git push origin add-resource-<short-name>
```

Then open a pull request against `main`.

## Schema requirements

Every entry must have:

| Field         | Required? | Notes                                                  |
| ------------- | --------- | ------------------------------------------------------ |
| `id`          | yes       | Unique slug, format `<prefix>-NNN`. Increment.         |
| `category`    | yes       | One of the 20 category IDs.                            |
| `name`        | yes       | Display name.                                          |
| `type`        | yes       | What it is.                                            |
| `audience`    | yes       | Who it serves.                                         |
| `description` | yes       | One sentence; ≤ 200 characters preferred.              |
| `url`         | yes       | Canonical URL; must start with `http(s)://`.           |
| `pricing`     | yes       | One of `free`, `paid`, `freemium`, `mixed`, `varies`.  |
| `region`      | yes       | `global`, a continent, or a country.                   |
| `language`    | yes       | ISO 639-1 (`en`, `fr`, `de`, …).                       |
| `status`      | yes       | One of `active`, `rebranded`, `defunct`.               |
| `tags`        | yes       | Array of short, lowercase, hyphenated tags.            |
| `verified`    | yes       | `YYYY-MM` of the month you confirmed the URL loads.    |

Optional fields: `subcategory`, `year_founded`, `notes`.

The full JSON Schema is at [`data/schema.json`](data/schema.json).

## URL verification policy

Before submitting a PR, **load every URL you add or change in a browser.**
Set `verified` to the current month (e.g. `"2026-05"`).

The weekly CI workflow at
[`.github/workflows/link-check.yml`](.github/workflows/link-check.yml) checks
all URLs and opens issues for batches of broken links.

## Choosing an `id`

Each category has a stable prefix:

| Category               | Prefix    | Example      |
| ---------------------- | --------- | ------------ |
| `governing_bodies`     | `gov-`    | `gov-129`    |
| `learn_to_swim`        | `lts-`    | `lts-026`    |
| `technique`            | `tech-`   | `tech-015`   |
| `youtube`              | `yt-`     | `yt-027`     |
| `training_plans`       | `train-`  | `train-020`  |
| `apps`                 | `app-`    | `app-020`    |
| `books`                | `book-`   | `book-035`   |
| `certifications`       | `cert-`   | `cert-024`   |
| `science`              | `sci-`    | `sci-020`    |
| `news`                 | `news-`   | `news-017`   |
| `podcasts`             | `pod-`    | `pod-015`    |
| `gear`                 | `gear-`   | `gear-026`   |
| `open_water`           | `ow-`     | `ow-021`     |
| `triathlon`            | `tri-`    | `tri-016`    |
| `masters`              | `mas-`    | `mas-017`    |
| `para`                 | `para-`   | `para-011`   |
| `drowning_prevention`  | `dp-`     | `dp-012`     |
| `records`              | `rec-`    | `rec-033`    |
| `college`              | `col-`    | `col-016`    |
| `recruiting`           | `rec2-`   | `rec2-017`   |

Pick the next available integer in that prefix's series.

## Commit messages

Use clear, conventional messages:

- `Add <Name> to <category>` - new entry
- `Update <id>: <what changed>` - correction
- `Flag <id> as rebranded/defunct: <details>` - status change
- `Fix dead link in <id>` - URL repair

## Pull request checklist

Your PR should pass these checks before review:

- [ ] `python scripts/build_dataset.py` exits 0 with no validation errors.
- [ ] You verified the URL loads in a browser.
- [ ] You set `verified` to the current month.
- [ ] You committed both the `scripts/data_partN.py` change *and* the
      regenerated files in `data/`.
- [ ] You did not edit `data/*.json`, `*.jsonl`, `*.csv`, or `*.parquet`
      directly.

## Reporting issues

Use the GitHub issue templates in
[`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/):

- **Resource: Add** - propose a new resource (we will add via PR).
- **Resource: Update / Correct** - fix a name, URL, or description.
- **Broken link** - flag a URL that no longer resolves.
- **Other** - anything else.

## Questions

Open a Discussion or an Issue. We typically respond within a week.

Thanks for contributing.
