# Fix merge conflicts
Get-Content "src\pages\case-artpop.astro" | Where-Object { $_ -notmatch "^<{3,}" -and $_ -notmatch "^={2,}" -and $_ -notmatch "^>{3,}" } | Set-Content "src\pages\case-artpop.astro" -NoNewline
Get-Content "src\pages\case-eho-pobedy-ope-air-2025.astro" | Where-Object { $_ -notmatch "^<{3,}" -and $_ -notmatch "^={2,}" -and $_ -notmatch "^>{3,}" } | Set-Content "src\pages\case-eho-pobedy-ope-air-2025.astro" -NoNewline
