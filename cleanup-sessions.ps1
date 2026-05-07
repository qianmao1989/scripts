# cleanup-sessions.ps1
# 会话文件夹容量清理脚本
# 规则：总大小超过 50MB 时，删除最旧的会话文件直到回到 50MB 以下

param(
    [string]$SessionsPath = "$env:USERPROFILE\.openclaw\agents\main\sessions",
    [int]$MaxSizeMB = 50
)

$ErrorActionPreference = "Stop"

$currentSize = (Get-ChildItem $SessionsPath -Recurse | Measure-Object -Property Length -Sum).Sum
$currentSizeMB = [math]::Round($currentSize / 1MB, 2)

if ($currentSizeMB -le $MaxSizeMB) {
    Write-Host "✅ 当前大小 ${currentSizeMB}MB，未超过 ${MaxSizeMB}MB，无需清理。"
    exit 0
}

Write-Host "⚠️ 当前大小 ${currentSizeMB}MB，超过 ${MaxSizeMB}MB，开始清理..."

# 按最后写入时间排序，找到可清理的会话文件（排除 sessions.json 和当前活跃会话）
$sessionsJson = Get-Content "$SessionsPath\sessions.json" -Raw | ConvertFrom-Json
$activeKeys = @()
foreach ($key in $sessionsJson.PSObject.Properties.Name) {
    $activeKeys += $key
}

# 获取所有 .jsonl 会话文件（按最后修改时间升序，最旧的在前）
$files = Get-ChildItem $SessionsPath -Filter "*.jsonl" |
    Where-Object { $_.Name -ne "sessions.json" } |
    Sort-Object LastWriteTime

$deleted = 0
foreach ($file in $files) {
    # 跳过当前活跃会话对应的文件
    $isActive = $false
    foreach ($key in $activeKeys) {
        if ($file.Name -like "$key*") {
            $isActive = $true
            break
        }
    }
    if ($isActive) { continue }

    $sessionId = $file.BaseName -replace '\.jsonl$',''
    Write-Host "🗑️ 删除旧会话: $($file.Name) ($([math]::Round($file.Length/1KB,1))KB, $($file.LastWriteTime))"

    # 删除该会话的所有相关文件
    Get-ChildItem $SessionsPath | Where-Object { $_.Name -like "$sessionId*" } | Remove-Item -Force
    $deleted++

    # 检查是否已经降到目标以下
    $remainingSize = (Get-ChildItem $SessionsPath -Recurse | Measure-Object -Property Length -Sum).Sum
    if ($remainingSize / 1MB -lt $MaxSizeMB) {
        Write-Host "✅ 清理完成，当前大小 $([math]::Round($remainingSize/1MB,2))MB"
        break
    }
}

if ($deleted -eq 0) {
    Write-Host "ℹ️ 没有可清理的旧会话文件（仅活跃会话）。"
} else {
    Write-Host "🧹 共清理了 $deleted 个旧会话。"
}
