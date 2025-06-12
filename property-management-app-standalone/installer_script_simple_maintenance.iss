; Property Management System Installer with Simple Maintenance Mode
; Basic version with repair, modify, and uninstall detection

[Setup]
AppName=Property Management System
AppVersion=1.0.0
AppPublisher=Property Management Team
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_Maintenance
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayName=Property Management System
UninstallDisplayIcon={app}\app_icon.ico
; Enable maintenance mode options
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=yes
; Show maintenance page for existing installations
WizardSmallImageFile=wizard_small.bmp
WizardImageFile=wizard_image.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
SetupAppTitle=Property Management System Setup
SetupWindowTitle=Property Management System Maintenance
WelcomeLabel1=Welcome to [name/ver] Maintenance
WelcomeLabel2=This installer can install, repair, modify, or remove [name/ver].%n%nClick Next to continue, or Cancel to exit.
ReadyLabel1=Setup is now ready to perform the selected operation.
ReadyLabel2a=Click Install to continue with the operation, or click Back if you want to review or change any settings.
FinishedLabel=Property Management System maintenance has been completed successfully.
FinishedLabelNoIcons=Property Management System maintenance has been completed.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "autostart"; Description: "Start with Windows"; GroupDescription: "Startup Options"; Flags: unchecked
Name: "repair"; Description: "&Repair installation"; GroupDescription: "Maintenance Mode"; Flags: exclusive
Name: "modify"; Description: "&Modify installation"; GroupDescription: "Maintenance Mode"; Flags: exclusive
Name: "reinstall"; Description: "&Reinstall application"; GroupDescription: "Maintenance Mode"; Flags: exclusive

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
Name: "{autostartup}\Property Management System"; Filename: "{app}\PropertyManager.exe"; Tasks: autostart

[Registry]
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.0"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: dword; ValueName: "Installed"; ValueData: 1

[Run]
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent; Check: not IsTaskSelected('autostart')

[UninstallDelete]
Type: files; Name: "{app}\property_management.db"
Type: files; Name: "{app}\*.log"
Type: filesandordirs; Name: "{app}\property_images"
Type: filesandordirs; Name: "{app}\docs"
Type: filesandordirs; Name: "{app}\__pycache__"

[UninstallRun]
Filename: "{cmd}"; Parameters: "/c taskkill /f /im PropertyManager.exe"; Flags: runhidden; RunOnceId: "KillPropertyManager"

[Code]
function IsInstalled(): Boolean;
var
  InstallPath: String;
begin
  Result := RegQueryStringValue(HKEY_CURRENT_USER, 'Software\PropertyManagementSystem', 'InstallPath', InstallPath) and DirExists(InstallPath);
end;

procedure InitializeWizard();
begin
  if IsInstalled() then
  begin
    WizardForm.WelcomeLabel1.Caption := 'Property Management System is already installed.';
    WizardForm.WelcomeLabel2.Caption := 'This installer can repair, modify, or reinstall the application.' + #13#10 + 
                                       'To uninstall, please use "Add or Remove Programs" from Control Panel.' + #13#10 + #13#10 +
                                       'Click Next to continue, or Cancel to exit.';
  end;
end; 