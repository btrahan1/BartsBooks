# Script to scan the local books folder and generate a books.json manifest
$books = @()
$booksDir = "books"

if (Test-Path $booksDir) {
    Get-ChildItem -Path $booksDir -Directory | ForEach-Object {
        $bookDir = $_
        $mdFiles = Get-ChildItem -Path $bookDir.FullName -Filter *.md
        if ($mdFiles.Count -gt 0) {
            $books += [PSCustomObject]@{
                id = $bookDir.Name
                title = $bookDir.Name -replace '_Book', ' - Book ' -replace '_', ' '
                chapters = $mdFiles.Count
            }
        }
    }

    $books | ConvertTo-Json | Out-File -FilePath "books.json" -Encoding utf8
    Write-Host "Generated books.json with $($books.Count) books." -ForegroundColor Green
} else {
    Write-Host "Books directory not found." -ForegroundColor Yellow
}
