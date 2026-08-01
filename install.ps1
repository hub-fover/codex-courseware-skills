$ErrorActionPreference = 'Stop'

$source = Join-Path $PSScriptRoot 'skills'
$target = Join-Path $HOME '.codex\skills'
New-Item -ItemType Directory -Force -Path $target | Out-Null

Get-ChildItem -Directory $source | ForEach-Object {
    $destination = Join-Path $target $_.Name
    if (Test-Path $destination) {
        $answer = Read-Host "Replace existing $($_.Name)? [y/N]"
        if ($answer -notmatch '^(y|yes)$') { return }
        Remove-Item -LiteralPath $destination -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse
    Write-Host "Installed $($_.Name)"
}
