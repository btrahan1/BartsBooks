# Script to split polished Amazing Grace source into chapters
$sourcePath = "books\AmazingGrace_Polished_Source.md"
$destDir = "books\AmazingGrace_Polished"

if (Test-Path $sourcePath) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    
    $content = Get-Content $sourcePath
    $currentChapter = 0
    $currentContent = @()
    
    foreach ($line in $content) {
        if ($line -match '^## Chapter (\d+)') {
            $num = [int]$Matches[1]
            if ($num -ne $currentChapter) {
                # New chapter! Save previous if exists
                if ($currentChapter -gt 0) {
                    $paddedNum = $currentChapter.ToString().PadLeft(2, '0')
                    $currentContent | Out-File -FilePath "$destDir\chapter_$paddedNum.md" -Encoding utf8
                    Write-Host "Saved chapter_$paddedNum.md" -ForegroundColor Green
                }
                $currentChapter = $num
                $currentContent = @($line)
            } else {
                # Continuation of same chapter
                $currentContent += $line
            }
        } else {
            if ($currentChapter -gt 0) {
                $currentContent += $line
            }
        }
    }
    
    # Save the last chapter
    if ($currentChapter -gt 0) {
        $paddedNum = $currentChapter.ToString().PadLeft(2, '0')
        $currentContent | Out-File -FilePath "$destDir\chapter_$paddedNum.md" -Encoding utf8
        Write-Host "Saved chapter_$paddedNum.md" -ForegroundColor Green
    }
    
    Write-Host "Finished splitting polished Amazing Grace." -ForegroundColor Green
} else {
    Write-Host "Source file not found: $sourcePath" -ForegroundColor Yellow
}
