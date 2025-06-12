; Simple and Safe Property Management System Installer Script
; This version avoids complex logic to prevent runtime errors

[Setup]
AppName=Property Management System
AppVersion=1.0.1
AppPublisher=Property Management Team
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_Safe
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Prevent common sources of runtime errors
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no
UninstallDisplayIcon={app}\app_icon.ico
AllowNoIcons=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Core application files (required)
Source: "installer_files\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Optional documentation files (only if they exist)
Source: "AIRTABLE_INTEGRATION_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion external skipifsourcedoesntexist
Source: "USER_MANUAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion external skipifsourcedoesntexist
Source: "airtable_config.py"; DestDir: "{app}"; Flags: ignoreversion external skipifsourcedoesntexist
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion external skipifsourcedoesntexist

[Icons]
Name: "{group}\Property Management System"; Filename: "{app}\PropertyManager.exe"
Name: "{group}\{cm:UninstallProgram,Property Management System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Property Management System"; Filename: "{app}\PropertyManager.exe"; Tasks: desktopicon

[Registry]
; Simple registry entries for application tracking
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.1"

[Run]
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up log files and temporary data
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: filesandordirs; Name: "{app}\temp"

[Code]
// Simple initialization without complex logic
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// Simple uninstall handling
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  KeepData: Boolean;
  DataPath: String;
  ImagesPath: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Simple data preservation choice
    KeepData := MsgBox(
      'Do you want to keep your property database and images?' + #13#10#13#10 +
      'Yes - Keep data for future installations' + #13#10 +
      'No - Remove all data completely',
      mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES;
    
    if not KeepData then
    begin
      // Simple cleanup - only remove what we know exists
      DataPath := ExpandConstant('{app}\property_management.db');
      ImagesPath := ExpandConstant('{app}\property_images');
      
      // Delete database file if exists
      if FileExists(DataPath) then
        DeleteFile(DataPath);
      
      // Delete images directory if exists
      if DirExists(ImagesPath) then
        DelTree(ImagesPath, True, True, True);
      
      // Delete logs directory
      DelTree(ExpandConstant('{app}\logs'), True, True, True);
      
      MsgBox('Property Management System and all data have been removed.' + #13#10 +
             'Thank you for using our software!', mbInformation, MB_OK);
    end
    else
    begin
      MsgBox('Property Management System has been uninstalled.' + #13#10 +
             'Your data has been preserved for future use.' + #13#10#13#10 +
             'Thank you for using our software!', mbInformation, MB_OK);
    end;
  end;
end;

// Simple post-install message
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Property Management System has been successfully installed!' + #13#10#13#10 +
           'You can now start the application from:' + #13#10 +
           '• Desktop shortcut (if created)' + #13#10 +
           '• Start Menu' + #13#10 +
           '• Or directly from: ' + ExpandConstant('{app}'),
           mbInformation, MB_OK);
  end;
end; 