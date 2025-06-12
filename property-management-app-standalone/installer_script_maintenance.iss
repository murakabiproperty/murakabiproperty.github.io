; Property Management System Installer with Maintenance Mode
; Enhanced version with Repair, Modify, Uninstall options

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
; Enable maintenance mode
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
MaintenanceMode=Property Management System is already installed on this computer.
SelectOperation=Please select the operation you would like to perform:
RepairInstallation=&Repair the installation
ModifyInstallation=&Modify the installation
RemoveInstallation=&Remove Property Management System from this computer
ContinueInstallation=&Reinstall Property Management System
MaintenanceTitle=Maintenance Mode
RepairDescription=Repair installation by reinstalling all program files
ModifyDescription=Add or remove program components
RemoveDescription=Remove the program and all of its components

[Code]
var
  MaintenancePage: TWizardPage;
  OperationRadioButton1, OperationRadioButton2, OperationRadioButton3, OperationRadioButton4: TRadioButton;
  SelectedOperation: Integer;

function IsInstalled(): Boolean;
var
  InstallPath: String;
begin
  Result := RegQueryStringValue(HKEY_CURRENT_USER, 'Software\PropertyManagementSystem', 'InstallPath', InstallPath) and DirExists(InstallPath);
end;

function GetSelectedOperation(): Integer;
begin
  Result := SelectedOperation;
end;

procedure CreateMaintenancePage();
var
  DescLabel: TLabel;
  OperationLabel: TLabel;
begin
  MaintenancePage := CreateCustomPage(wpWelcome, ExpandConstant('{cm:MaintenanceTitle}'), ExpandConstant('{cm:MaintenanceMode}'));

  DescLabel := TLabel.Create(MaintenancePage);
  DescLabel.Parent := MaintenancePage.Surface;
  DescLabel.Left := 0;
  DescLabel.Top := 0;
  DescLabel.Width := MaintenancePage.SurfaceWidth;
  DescLabel.Height := 40;
  DescLabel.AutoSize := False;
  DescLabel.WordWrap := True;
  DescLabel.Caption := ExpandConstant('{cm:SelectOperation}');

  OperationRadioButton1 := TRadioButton.Create(MaintenancePage);
  OperationRadioButton1.Parent := MaintenancePage.Surface;
  OperationRadioButton1.Left := 20;
  OperationRadioButton1.Top := 60;
  OperationRadioButton1.Width := MaintenancePage.SurfaceWidth - 40;
  OperationRadioButton1.Height := 17;
  OperationRadioButton1.Caption := ExpandConstant('{cm:RepairInstallation}');
  OperationRadioButton1.Checked := True;

  DescLabel := TLabel.Create(MaintenancePage);
  DescLabel.Parent := MaintenancePage.Surface;
  DescLabel.Left := 40;
  DescLabel.Top := 80;
  DescLabel.Width := MaintenancePage.SurfaceWidth - 60;
  DescLabel.Height := 20;
  DescLabel.Font.Style := [];
  DescLabel.Font.Color := clGray;
  DescLabel.Caption := ExpandConstant('{cm:RepairDescription}');

  OperationRadioButton2 := TRadioButton.Create(MaintenancePage);
  OperationRadioButton2.Parent := MaintenancePage.Surface;
  OperationRadioButton2.Left := 20;
  OperationRadioButton2.Top := 110;
  OperationRadioButton2.Width := MaintenancePage.SurfaceWidth - 40;
  OperationRadioButton2.Height := 17;
  OperationRadioButton2.Caption := ExpandConstant('{cm:ModifyInstallation}');

  DescLabel := TLabel.Create(MaintenancePage);
  DescLabel.Parent := MaintenancePage.Surface;
  DescLabel.Left := 40;
  DescLabel.Top := 130;
  DescLabel.Width := MaintenancePage.SurfaceWidth - 60;
  DescLabel.Height := 20;
  DescLabel.Font.Style := [];
  DescLabel.Font.Color := clGray;
  DescLabel.Caption := ExpandConstant('{cm:ModifyDescription}');

  OperationRadioButton3 := TRadioButton.Create(MaintenancePage);
  OperationRadioButton3.Parent := MaintenancePage.Surface;
  OperationRadioButton3.Left := 20;
  OperationRadioButton3.Top := 160;
  OperationRadioButton3.Width := MaintenancePage.SurfaceWidth - 40;
  OperationRadioButton3.Height := 17;
  OperationRadioButton3.Caption := ExpandConstant('{cm:RemoveInstallation}');

  DescLabel := TLabel.Create(MaintenancePage);
  DescLabel.Parent := MaintenancePage.Surface;
  DescLabel.Left := 40;
  DescLabel.Top := 180;
  DescLabel.Width := MaintenancePage.SurfaceWidth - 60;
  DescLabel.Height := 20;
  DescLabel.Font.Style := [];
  DescLabel.Font.Color := clGray;
  DescLabel.Caption := ExpandConstant('{cm:RemoveDescription}');

  OperationRadioButton4 := TRadioButton.Create(MaintenancePage);
  OperationRadioButton4.Parent := MaintenancePage.Surface;
  OperationRadioButton4.Left := 20;
  OperationRadioButton4.Top := 210;
  OperationRadioButton4.Width := MaintenancePage.SurfaceWidth - 40;
  OperationRadioButton4.Height := 17;
  OperationRadioButton4.Caption := ExpandConstant('{cm:ContinueInstallation}');
end;

procedure InitializeWizard();
begin
  if IsInstalled() then
  begin
    CreateMaintenancePage();
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  if IsInstalled() then
  begin
    case PageID of
      wpWelcome, wpLicense, wpInfoBefore, wpUserInfo, wpSelectDir, wpSelectProgramGroup, wpSelectTasks, wpReady, wpInfoAfter:
      begin
        // For repair and reinstall, skip to file copying
        if (SelectedOperation = 1) or (SelectedOperation = 4) then
          Result := True;
        // For modify, show component selection
        if (SelectedOperation = 2) then
          Result := (PageID <> wpSelectTasks);
        // For uninstall, skip all pages except maintenance
        if (SelectedOperation = 3) then
          Result := True;
      end;
      wpInstalling:
      begin
        // For uninstall, skip installation page
        if (SelectedOperation = 3) then
          Result := True;
      end;
    end;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if (CurPageID = MaintenancePage.ID) then
  begin
    if OperationRadioButton1.Checked then
      SelectedOperation := 1  // Repair
    else if OperationRadioButton2.Checked then
      SelectedOperation := 2  // Modify
    else if OperationRadioButton3.Checked then
      SelectedOperation := 3  // Uninstall
    else if OperationRadioButton4.Checked then
      SelectedOperation := 4; // Reinstall
      
    // If uninstall is selected, run uninstaller
    if (SelectedOperation = 3) then
    begin
      var
        ResultCode: Integer;
      begin
        if Exec(ExpandConstant('{uninstallexe}'), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode) then
        begin
          WizardForm.Close;
          Result := False;
        end;
      end;
    end;
  end;
end;

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "autostart"; Description: "Start with Windows"; GroupDescription: "Startup Options"; Flags: unchecked

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

[Messages]
SetupAppTitle=Property Management System Setup
SetupWindowTitle=Property Management System Setup - Maintenance Mode
WelcomeLabel1=[name/ver] Setup
WelcomeLabel2=This installer can repair, modify, or remove [name/ver].%n%nIt is recommended that you close all other applications before continuing. 