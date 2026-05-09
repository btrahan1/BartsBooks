$scratchDir = "C:\Users\bartt\.gemini\antigravity\scratch"
$destDir = "books"

# Function to copy and rename
function Import-Book($srcPath, $destName, $pattern, $numberExtractor) {
    $targetDir = Join-Path $destDir $destName
    if (!(Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir | Out-Null
    }
    
    Get-ChildItem -Path $srcPath -Filter $pattern | Where-Object { $_.Name -ne "00_frontmatter.md" } | ForEach-Object {
        $file = $_
        $num = &$numberExtractor $file.Name
        if ($num -gt 0) {
            $paddedNum = $num.ToString().PadLeft(2, '0')
            $newName = "chapter_$paddedNum.md"
            Copy-Item -Path $file.FullName -Destination (Join-Path $targetDir $newName) -Force
        }
    }
    Write-Host "Imported $destName" -ForegroundColor Green
}

# The Thrill
Import-Book `
    -srcPath (Join-Path $scratchDir "TheThrill\Chapters") `
    -destName "TheThrill" `
    -pattern "*.md" `
    -numberExtractor { param($name) [int]($name.Substring(0, 2)) }

# Never Going Back
Import-Book `
    -srcPath (Join-Path $scratchDir "NeverGoingBAck\manuscript") `
    -destName "NeverGoingBAck" `
    -pattern "*.md" `
    -numberExtractor { param($name) if ($name -match '^\d+') { [int]$Matches[0] } else { 0 } }

# Bus To Anywhere
Import-Book `
    -srcPath (Join-Path $scratchDir "BusToAnywhere\Chapters") `
    -destName "BusToAnywhere" `
    -pattern "*.md" `
    -numberExtractor { param($name) [int]($name.Substring(0, 2)) }

# No Ordinary Mage
Import-Book `
    -srcPath (Join-Path $scratchDir "NoOrdinaryMage\Book1") `
    -destName "NoOrdinaryMage_Book1" `
    -pattern "*.md" `
    -numberExtractor { param($name) if ($name -match '\d+') { [int]$Matches[0] } else { 0 } }
