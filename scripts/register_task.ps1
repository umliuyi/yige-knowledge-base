$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\run_pipeline_v3.py"
Register-ScheduledTask -TaskName "小虾早报视频流水线" -Action $action -Trigger (New-ScheduledTaskTrigger -Daily -At "08:30") -Description "每天8:30自动生成早报视频" -RunLevel Highest
Write-Output "done"
