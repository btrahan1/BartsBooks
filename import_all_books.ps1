# Script to import all remaining books from scratch
$scratchDir = "C:\Users\bartt\.gemini\antigravity\scratch"
$destBase = "books"

$booksToImport = @(
    "KungFuKevin", "AIMeltdown", "BeautifulBard", "KungFuMedic", "TannerSmith",
    "WayOfTheSpear", "OrbitHaul", "ThePreserve", "TheThrill", "ShakespeareInArcadia",
    "NeverGoingBAck", "BusToAnywhere", "Score3D", "WuxiaKungFu", "NoOrdinaryMage",
    "SpaceTrucker", "SpaceTrucker_Book3", "SpaceTrucker_Book2"
)

foreach ($book in $booksToImport) {
    $srcDir = Join-Path $scratchDir $book
    $destDir = Join-Path $destBase $book
    
    if (Test-Path $srcDir) {
        Write-Host "Processing $book..." -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        
        # Look for chapter files in root or manuscript/chapters
        $searchPaths = @($srcDir, (Join-Path $srcDir "manuscript"), (Join-Path $srcDir "chapters"))
        $copied = $false
        
        foreach ($p in $searchPaths) {
            if (Test-Path $p) {
                $files = Get-ChildItem -Path $p -Filter "Chapter_*.md"
                if ($files.Count -eq 0) {
                    $files = Get-ChildItem -Path $p -Filter "chapter_*.md"
                }
                
                if ($files.Count -gt 0) {
                    Write-Host "  Found $($files.Count) files in $p" -ForegroundColor Green
                    $files | ForEach-Object {
                        $name = $_.Name
                        # Extract number
                        if ($name -match '(\d+)') {
                            $num = $Matches[1].PadLeft(2, '0')
                            $newName = "chapter_$num.md"
                            Copy-Item $_.FullName -Destination "$destDir\$newName" -Force
                        }
                    }
                    $copied = $true
                    break # Stop after finding first valid directory
                }
            }
        }
        
        if (-not $copied) {
            Write-Host "  No standard chapter files found for $book" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Source not found: $srcDir" -ForegroundColor Red
    }
}

Write-Host "`nUpdating manifest..." -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File .\generate_books_manifest.ps1
