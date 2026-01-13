#!/usr/bin/env pwsh
# cosmographia.ps1
# Runs Cosmographia with selectable subcommands and persistent COSMO_PATH.

$ConfigFile = Join-Path $HOME ".cosmo_path"

function Show-Help {
    Write-Host "Usage: $(Split-Path $PSCommandPath -Leaf) [OPTION]"
    Write-Host ""
    Write-Host "Run Cosmographia plugin or one of its related commands."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  juice_ptr     JUICE pointing request plugin"
    Write-Host "  juice_mk      JUICE metakernel loader plugin"
    Write-Host "  cosmo_main    Multi-mission plugin (default)"
    Write-Host "  stardb        Run the stardb database utility"
    Write-Host ""
    Write-Host "If this is your first time running the script, you will be prompted"
    Write-Host "to enter the path where Cosmographia is installed."
}

# -------------------------
# Load or set COSMO_PATH
# -------------------------
if (-not $env:COSMO_PATH -or $env:COSMO_PATH.Trim() -eq "") {

    if (Test-Path $ConfigFile) {
        $env:COSMO_PATH = (Get-Content $ConfigFile -Raw).Trim()
    }
    else {
        Write-Host "COSMO_PATH is not set."
        $env:COSMO_PATH = Read-Host "Please enter the full path to the Cosmographia directory"

        $Executable = Join-Path $env:COSMO_PATH "Cosmographia.exe"

        if (-not (Test-Path $Executable)) {
            Write-Error "Cosmographia executable not found at that location."
            exit 1
        }

        $env:COSMO_PATH.Trim() | Set-Content -NoNewline $ConfigFile
        Write-Host "Saved COSMO_PATH to $ConfigFile"
    }
}

# -------------------------
# Handle arguments
# -------------------------
$Cmd = $args[0]

switch ($Cmd) {
    "juice_ptr"   { $PyScript = "juice_ptr.py" }
    "juice_mk"    { $PyScript = "juice_mk.py" }
    "stardb"      { $PyScript = "stardb_conf.py" }
    "cosmo_main"  { $PyScript = "cosmo_main.py" }
    ""            { $PyScript = "cosmo_main.py" }
    "-h"          { Show-Help; exit 0 }
    "--help"      { Show-Help; exit 0 }
    default {
        Write-Error "Unknown option '$Cmd'"
        Show-Help
        exit 1
    }
}

# -------------------------
# Run Cosmographia
# -------------------------
$Executable = Join-Path ($env:COSMO_PATH).Trim() "Cosmographia.exe"
$Folder = Get-Location

Write-Host "Launching Cosmographia $Executable"
& $Executable -p (Join-Path $Folder $PyScript)