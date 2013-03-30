@echo off
%~d0
cd %~dp0

set serverRoot=.\Server

:: Common
del /f /s /q "*.log" > nul 2>&1
del /f /s /q "*.err" > nul 2>&1

:: Collect Server
rmdir /s /q "%serverRoot%\Collect Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Collect Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Collect Server\WorkflowServer\Cache" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\Jobs\Auto\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\WorkflowServer\Log\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\WorkflowServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\WorkflowServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\WorkflowServer\Triggers\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\WorkflowServer\Archive\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\Recovery\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\Preprocess\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Collect Server\Logs\*.*" > nul 2>&1

:: Flow Server
rmdir /s /q "%serverRoot%\Flow Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Flow Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Flow Server\WorkflowServer\Cache" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\Jobs\Auto\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\WorkflowServer\Log\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\WorkflowServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\WorkflowServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\WorkflowServer\Triggers\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\WorkflowServer\Archive\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\Recovery\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Flow Server\Logs\*.*" > nul 2>&1

:: Publish Server
rmdir /s /q "%serverRoot%\Publish Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Publish Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Publish Server\WorkflowServer\Cache" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\Jobs\Auto\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\WorkflowServer\Log\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\WorkflowServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\WorkflowServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\WorkflowServer\Triggers\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\WorkflowServer\Archive\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\Recovery\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Publish Server\Logs\*.*" > nul 2>&1

:: Config Server
rmdir /s /q "%serverRoot%\Config Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Config Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Config Server\ConfigServer\Cache" > nul 2>&1
rmdir /s /q "%serverRoot%\Config Server\ConfigServer\Files\Tmp" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\ConfigServer\Data\PrinterServer\*.pdf" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\ConfigServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\ConfigServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\BackupUpdate\*.log" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\BackupUpdate\*.html" > nul 2>&1
del /f /s /q "%serverRoot%\Config Server\Logs\*.*" > nul 2>&1

:: Document Server
rmdir /s /q "%serverRoot%\Document Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Document Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Document Server\DocumentServer\Cache" > nul 2>&1
del /f /s /q "%serverRoot%\Document Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Document Server\DocumentServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Document Server\DocumentServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Document Server\DocumentServer\ZDocIn\*.*" > nul 2>&1
rmdir /s /q "%serverRoot%\Document Server\DocumentServer\ZDocIn\Error" > nul 2>&1
rmdir /s /q "%serverRoot%\Document Server\DocumentServer\ZDocIn\Fast\TempZDoc" > nul 2>&1
del /f /s /q "%serverRoot%\Document Server\Logs\*.*" > nul 2>&1

:: Recognize Server
rmdir /s /q "%serverRoot%\Recognize Server\Temp" > nul 2>&1
mkdir "%serverRoot%\Recognize Server\Temp" > nul 2>&1
rmdir /s /q "%serverRoot%\Recognize Server\RecognizeServer\Cache" > nul 2>&1
del /f /s /q "%serverRoot%\Recognize Server\transfer\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Recognize Server\RecognizeServer\Queue\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Recognize Server\RecognizeServer\Temp\*.*" > nul 2>&1
del /f /s /q "%serverRoot%\Recognize Server\Logs\*.*" > nul 2>&1