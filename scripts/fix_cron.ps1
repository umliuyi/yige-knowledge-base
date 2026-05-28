$jobs = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object { $_.TaskName -like "*调研*" -or $_.TaskName -like "*research*" }
if ($jobs) {
    foreach ($j in $jobs) {
        Write-Output "Found: $($j.TaskName)"
        Unregister-ScheduledTask -TaskName $j.TaskName -Confirm:$false -ErrorAction SilentlyContinue
        Write-Output "Unregistered: $($j.TaskName)"
    }
} else {
    Write-Output "No matching tasks found"
}
