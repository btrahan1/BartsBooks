# Script to scan the local books folder and generate a books.json manifest
$books = @()
$booksDir = "books"

if (Test-Path $booksDir) {
    Get-ChildItem -Path $booksDir -Directory | ForEach-Object {
        $bookDir = $_
        # Exclude synopsis.md from chapter count
        $mdFiles = Get-ChildItem -Path $bookDir.FullName -Filter *.md | Where-Object { $_.Name -ne "synopsis.md" -and $_.Name -ne "notes.md" }
        
        if ($mdFiles.Count -gt 0) {
            # Read synopsis if it exists
            $synopsisPath = Join-Path $bookDir.FullName "synopsis.md"
            $synopsis = "No synopsis available."
            if (Test-Path $synopsisPath) {
                $synopsis = Get-Content $synopsisPath -Raw
            }
            
            $books += [PSCustomObject]@{
                id = $bookDir.Name
                title = $bookDir.Name -replace '_Book', ' - Book ' -replace '_', ' '
                chapters = $mdFiles.Count
                synopsis = $synopsis.Trim()
            }
        }
    }

    $books | ConvertTo-Json | Out-File -FilePath "books.json" -Encoding utf8
    Write-Host "Generated books.json with $($books.Count) books." -ForegroundColor Green
} else {
    Write-Host "Books directory not found." -ForegroundColor Yellow
}
