[CmdletBinding()]
param (
    [Parameter()]
    [switch]$Files,
    [Parameter()]
    [switch]$Git,
    [Parameter()]
    [string] $Source = $null,
    [Parameter()]
    [string] $Destination = $null,
    [Parameter()]
    [string] $ConfigFile = "./config/config.json"
)


function Time { 
    # equivilent to bash time function for performance measuring
    $Command = "$args"
    Measure-Command { Invoke-Expression $Command 2>&1 | out-default} 
}

function Get-Switch{
    param(
        [string]$SwitchName
    )
    return $Config.Switches | Where-Object { $_.Name -eq $SwitchName }
}

function RoboMirror {
    # standardized Robocopy /MIR operation
    param(
        [string]$Source,
        [string]$Destination
    )
    
    # first number is GigaByte representation
    $MaxBytes = 10 * 1000000000

    $ParentPath = [System.IO.Path]::GetDirectoryName($Destination)
    $LogFile = Join-Path $ParentPath "logs/robomirror_$([System.IO.Path]::GetFileName($Destination)).log"

    $LogFileExists = Test-Path $LogFile
    
    if ($LogFileExists -eq $false) {
        New-Item $LogFile -Force
    }

    # must wipe VeraCrypt volumes, so mirror will update their data, can add other overwritables
    $overwrite_files = Get-ChildItem $Destination -Include *.hc -Recurse -Force

    Write-Output "Removing Overwritable Filetypes:"
    foreach ($ft in $overwrite_files) {
        Write-Output "      $ft"
        Remove-Item $ft -Force
    }

    Write-Output "Mirroring Directory:
    Source: $Source
    Destination: $Destination"

    # Options: MultiThreaded, Mirror, NoIOBuffer, MaxFileBytes, FullPathLogging, NoProgressLogging, LogFile
    Robocopy $source $destination /MT /MIR /J /MAX:$MaxBytes /FP /NP /LOG:$LogFile
}


$Config = $(Get-Content $ConfigFile | ConvertFrom-Json)

# executing given Source-Destination
if ($Source -and $Destination){
    Time RoboMirror $Source $Destination
}

# executing standard switches
if ($Files -eq $true) {
    $SwitchFiles = Get-Switch "Files"
    Time RoboMirror $SwitchFiles.Source $SwitchFiles.Destination
}

if ($Git -eq $true) {
    $SwitchGit = Get-Switch "Git"
    Time RoboMirror $SwitchGit.Source $SwitchGit.Destination
}
