# ago_stack_monorepo

Optional **integrator** repository: one clone with **git submodules** (one per stack layer) so submodule pointers move together on release branches, while **day-to-day development** still happens in each layer’s own GitHub repo.

**Canonical pins:** [ago_stack_wheel_pulls](https://github.com/sp103107/ago_stack_wheel_pulls) — keep [`stack_pins.json`](stack_pins.json) aligned (or run [`scripts/sync_pins_from_wheel_pulls.ps1`](scripts/sync_pins_from_wheel_pulls.ps1)).

**License:** root [`LICENSE`](LICENSE) (AoS proprietary short + URN). Canonical pack: [`../aos_license_pack_v1/aos_license_pack_v1/`](../aos_license_pack_v1/aos_license_pack_v1/) — see [`../docs/LICENSE_CANONICAL_PACK.md`](../docs/LICENSE_CANONICAL_PACK.md).

**Governance:** Standalone ownership and Atlas remain in **ago_stack_control** docs; this repo is only an integration surface.

## Why submodules

- **Pull a layer:** `cd <submodule> && git fetch && git checkout <sha>` then commit the parent repo to bump the integrated pointer.
- **Push layer code:** Always in the **layer remote**, not by editing copies in the monorepo without submodule workflow.

## First-time setup (empty monorepo)

After `git init` / clone of **this** repo:

1. Copy or sync pins: see `scripts/sync_pins_from_wheel_pulls.ps1` if you keep both repos as siblings.

2. Add each submodule (once). Commands are generated for you:

   ```bash
   python3 scripts/print_submodule_commands.py
   ```

   Run the printed `git submodule add ...` lines from the monorepo root, then:

   ```bash
   git submodule update --init --recursive
   ```

3. Pin each submodule to the SHA in `stack_pins.json`:

   ```bash
   python3 scripts/apply_pins_to_submodules.py --root .
   ```

4. Commit `.gitmodules` and submodule pointer commits in the parent.

## Update all submodules to pins file

```bash
python3 scripts/apply_pins_to_submodules.py --root .
git status   # review detached HEADs at pinned SHAs
git add -A
git commit -m "Bump stack pins to match stack_pins.json"
```

## Layout

| Path | Role |
|------|------|
| `stack_pins.json` | Mirror of wheel_pulls pin manifest. |
| `scripts/print_submodule_commands.py` | Emit `git submodule add` for missing paths. |
| `scripts/apply_pins_to_submodules.py` | Fetch + `git checkout` pinned SHA in each submodule. |
| `scripts/sync_pins_from_wheel_pulls.ps1` | Copy `stack_pins.json` from a sibling wheel_pulls clone. |
| `docs/INIT_SUBMODULES.md` | Human checklist matching the scripts. |

## Auxiliary module triage

Canonical write-up lives in **ago_stack_wheel_pulls**:  
[docs/AUXILIARY_MODULE_REGISTRY_TRIAGE.md](https://github.com/sp103107/ago_stack_wheel_pulls/blob/main/docs/AUXILIARY_MODULE_REGISTRY_TRIAGE.md)

When this repo sits next to `ago_stack_wheel_pulls` inside a larger workspace, you can open `../ago_stack_wheel_pulls/docs/AUXILIARY_MODULE_REGISTRY_TRIAGE.md` locally.
