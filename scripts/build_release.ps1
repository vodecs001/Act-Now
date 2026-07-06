param(
    [string]$PythonExe = "E:\inkscape\bin\python.exe",
    [string]$PythonPath = "C:\Users\admin\AppData\Local\Programs\Python\Python313\Lib\site-packages",
    [string]$TclLibrary = "E:\inkscape\lib\tcl8.6",
    [string]$TkLibrary = "E:\inkscape\lib\tk8.6"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ReleaseDir = Join-Path $ProjectRoot "release"
$BuildAppDir = Join-Path $ProjectRoot "build_actnow"
$BuildInstallerDir = Join-Path $ProjectRoot "build_installer"

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

$env:PYTHONPATH = $PythonPath
$env:TCL_LIBRARY = $TclLibrary
$env:TK_LIBRARY = $TkLibrary

$commonTkData = @(
    "--add-data", "$TclLibrary;_tcl_data",
    "--add-data", "$TkLibrary;_tk_data",
    "--add-data", "$TclLibrary;lib/tcl8.6",
    "--add-data", "$TkLibrary;lib/tk8.6"
)

& $PythonExe -m PyInstaller --noconfirm --onefile --windowed `
    --name "ActNow" `
    --icon "$ProjectRoot\assets\app_icon.ico" `
    --add-data "$ProjectRoot\assets\lxfs.png;assets" `
    --add-data "$ProjectRoot\assets\app_icon.ico;assets" `
    --add-data "$ProjectRoot\assets\app_icon_256.png;assets" `
    @commonTkData `
    --distpath $ReleaseDir `
    --workpath $BuildAppDir `
    --specpath $ProjectRoot `
    "$ProjectRoot\sticky_todo.py"

Copy-Item "$ReleaseDir\ActNow.exe" "$ReleaseDir\快办.exe" -Force

& $PythonExe -m PyInstaller --noconfirm --onefile --windowed `
    --name "ActNowSetup" `
    --icon "$ProjectRoot\assets\app_icon.ico" `
    --add-data "$ReleaseDir\快办.exe;payload" `
    --add-data "$ProjectRoot\assets\app_icon.ico;assets" `
    --add-data "$ProjectRoot\assets\app_icon_256.png;assets" `
    @commonTkData `
    --distpath $ReleaseDir `
    --workpath $BuildInstallerDir `
    --specpath "$ProjectRoot\installer" `
    "$ProjectRoot\installer\actnow_installer.py"

Copy-Item "$ReleaseDir\ActNowSetup.exe" "$ReleaseDir\快办安装程序.exe" -Force

Write-Host "Built:"
Write-Host "  $ReleaseDir\快办.exe"
Write-Host "  $ReleaseDir\快办安装程序.exe"
