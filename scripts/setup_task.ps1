$pythonPath = "C:\Users\julio\AppData\Local\Programs\Python\Python312\python.exe"
$scriptPath = "C:\Users\julio\dev\sitio-web-csd\scripts\auto_sync.py"
$workDir = "C:\Users\julio\dev\sitio-web-csd"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00"
$trigger.RepetitionInterval = (New-TimeSpan -Minutes 15)
$trigger.RepetitionDuration = (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "CSD_Sync_EduColombia" -Action $action -Trigger $trigger -Settings $settings -Description "Sincronizacion continua de cupos con EduColombia para Colegio CSD" -Force
Start-ScheduledTask -TaskName "CSD_Sync_EduColombia"
Write-Host "Tarea programada registrada y ejecutada exitosamente."
