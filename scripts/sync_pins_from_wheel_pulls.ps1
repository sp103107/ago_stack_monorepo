# Copies stack_pins.json from a sibling ago_stack_wheel_pulls clone into this monorepo root.
# Usage: .\scripts\sync_pins_from_wheel_pulls.ps1 -WheelPullsRoot ..\ago_stack_wheel_pulls

param(
    [Parameter(Mandatory = $true)]
    [string] $WheelPullsRoot
)

$monoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$src = Join-Path $WheelPullsRoot "stack_pins.json"
$dst = Join-Path $monoRoot "stack_pins.json"
if (-not (Test-Path $src)) { Write-Error "Missing $src"; exit 2 }
Copy-Item -Path $src -Destination $dst -Force
Write-Host "Copied stack_pins.json -> $dst"
# Restore monorepo canonical_note (optional manual): wheel_pulls file wins for content;
# edit canonical_note in dst if you want the monorepo disclaimer string.
exit 0
