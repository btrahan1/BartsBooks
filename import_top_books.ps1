# Script to import and normalize top books from scratch
$ErrorActionPreference = "Stop"

# Function to copy and normalize simple cases (Chapter_01.md -> chapter_01.md)
function Import-SimpleBook ($srcDir, $destDir) {
    if (Test-Path $srcDir) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Get-ChildItem -Path $srcDir -Filter "Chapter_*.md" | ForEach-Object {
            $newName = $_.Name -replace '^Chapter_', 'chapter_'
            Copy-Item $_.FullName -Destination "$destDir\$newName"
        }
        Write-Host "Imported $destDir" -ForegroundColor Green
    } else {
        Write-Host "Source not found: $srcDir" -ForegroundColor Yellow
    }
}

# 1. CultivatorInNYC
Import-SimpleBook "C:\Users\bartt\.gemini\antigravity\scratch\CultivatorInNYC" "books\CultivatorInNYC_Book1"
Import-SimpleBook "C:\Users\bartt\.gemini\antigravity\scratch\CultivatorInNYC\book2" "books\CultivatorInNYC_Book2"
Import-SimpleBook "C:\Users\bartt\.gemini\antigravity\scratch\CultivatorInNYC\book3" "books\CultivatorInNYC_Book3"

# 2. GongTheTank
Import-SimpleBook "C:\Users\bartt\.gemini\antigravity\scratch\GongTheTank" "books\GongTheTank"

# 3. SmallTownSmith (Requires special extraction for names like chapter_1_escape.md)
$srcDir = "C:\Users\bartt\.gemini\antigravity\scratch\SmallTownSmith"
$destDir = "books\SmallTownSmith"

if (Test-Path $srcDir) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    Get-ChildItem -Path $srcDir -Filter "chapter_*.md" | ForEach-Object {
        if ($_.Name -match 'chapter_(\d+)_') {
            $num = $Matches[1].PadLeft(2, '0')
            $newName = "chapter_$num.md"
            Copy-Item $_.FullName -Destination "$destDir\$newName"
        }
    }
    Write-Host "Imported $destDir (Normalized names)" -ForegroundColor Green
} else {
    Write-Host "Source not found: $srcDir" -ForegroundColor Yellow
}
