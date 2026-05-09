# Script to scan the scratch folder for folders containing .md files (potential books)
$scratchDir = "C:\Users\bartt\.gemini\antigravity\scratch"
$books = @()

Write-Host "Scanning $scratchDir for books..." -ForegroundColor Cyan

Get-ChildItem -Path $scratchDir -Directory | ForEach-Object {
    $dir = $_
    # Check if directory contains .md files (searching recursively)
    $mdFiles = Get-ChildItem -Path $dir.FullName -Filter *.md -Recurse -ErrorAction SilentlyContinue
    
    if ($mdFiles.Count -gt 0) {
        $books += [PSCustomObject]@{
            FolderName = $dir.Name
            MdFileCount = $mdFiles.Count
        }
    }
}

# Display results
if ($books.Count -gt 0) {
    Write-Host "`nFound the following potential book folders:" -ForegroundColor Green
    $books | Sort-Object MdFileCount -Descending | Format-Table -AutoSize
} else {
    Write-Host "No folders with .md files found." -ForegroundColor Yellow
}
