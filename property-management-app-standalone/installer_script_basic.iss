; Basic Property Management System Installer Script
; Simple version without complex Pascal scripting

[Setup]
AppName=Property Management System
AppVersion=1.0.0
AppPublisher=Property Management Team
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_Basic
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayName=Property Management System
UninstallDisplayIcon={app}\app_icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "installer_files\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "AIRTABLE_INTEGRATION_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion skipifsourcedoesntexist
Source: "USER_MANUAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion skipifsourcedoesntexist
Source: "airtable_config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\Configuration Guide"; Filename: "{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md"
Name: "{group}\User Manual"; Filename: "{app}\docs\USER_MANUAL.md"  
Name: "{group}\{cm:UninstallProgram,Property Management System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.0"

[Run]
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\property_management.db"
Type: files; Name: "{app}\*.log"
Type: filesandordirs; Name: "{app}\property_images"
Type: filesandordirs; Name: "{app}\docs"

[Messages]
SetupAppTitle=Property Management System Setup
SetupWindowTitle=Property Management System Setup
WelcomeLabel1=[name/ver] Setup
WelcomeLabel2=This will install [name/ver] on your computer.%n%nIt is recommended that you close all other applications before continuing. 