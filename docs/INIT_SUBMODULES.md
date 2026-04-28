# Initialize submodules (checklist)

Use this after creating the [ago_stack_monorepo](https://github.com/sp103107/ago_stack_monorepo) Git repository on GitHub and cloning it locally.

1. Ensure [`stack_pins.json`](../stack_pins.json) matches [ago_stack_wheel_pulls](https://github.com/sp103107/ago_stack_wheel_pulls) (run `scripts/sync_pins_from_wheel_pulls.ps1` or copy the file).

2. Print one-time `git submodule add` commands:

   ```bash
   python3 scripts/print_submodule_commands.py --root .
   ```

3. Execute each printed line from the monorepo root (Git 2.13+). If a path already exists as a plain folder, remove or rename it before `submodule add`.

4. Initialize:

   ```bash
   git submodule update --init --recursive
   ```

5. Detach each submodule at the pinned SHA:

   ```bash
   python3 scripts/apply_pins_to_submodules.py --root .
   ```

6. Commit `.gitmodules` and the submodule gitlink blobs in the parent repository.

## Updating a single layer

```bash
cd RAGMT_RUNTIME
git fetch origin
git checkout <new-sha>
cd ..
git add RAGMT_RUNTIME
git commit -m "Bump RAGMT_RUNTIME"
```

Then update `stack_pins.json` in **ago_stack_wheel_pulls** (canonical) and mirror the SHA into this repo’s `stack_pins.json`.
