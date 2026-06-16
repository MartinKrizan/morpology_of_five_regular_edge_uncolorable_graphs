# Output

This directory contains generated results that are useful enough to keep in the
repository.

## Directories

- [`gadget_categories/`](gadget_categories/) - graph6 files produced by
  `gadget-categorize`.

The category filenames encode the number of port pairs in each relation class:

```text
same_<n>__different_<n>__flexible_<n>__blocked_<n>.g6
```

Regenerate category files with:

```sh
docker compose run --rm python gadget-categorize --ports 5 --n-min 5 --n-max 13
```
