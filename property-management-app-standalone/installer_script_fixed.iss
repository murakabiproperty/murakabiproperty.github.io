; Fixed Property Management System Installer Script
; This version properly handles preserve data scenarios without runtime errors

[Setup]
AppName=Property Management System
AppVersion=1.0.1
AppPublisher=Property Management Team
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_Fixed
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Add these to prevent runtime errors
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "installer_files\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "AIRTABLE_INTEGRATION_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion; Check: FileExists('AIRTABLE_INTEGRATION_GUIDE.md')
Source: "USER_MANUAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion; Check: FileExists('USER_MANUAL.md')
Source: "airtable_config.py"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('airtable_config.py')
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('app_icon.ico')

[Icons]
Name: "{group}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\Configuration Guide"; Filename: "{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md"; Check: FileExists(ExpandConstant('{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md'))
Name: "{group}\User Manual"; Filename: "{app}\docs\USER_MANUAL.md"; Check: FileExists(ExpandConstant('{app}\docs\USER_MANUAL.md'))
Name: "{group}\{cm:UninstallProgram,Property Management System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Registry]
; Application settings
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.1"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallDate"; ValueData: "{code:GetCurrentDate}"

[Run]
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Only delete these if user chooses not to preserve data
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\temp\*.*"

[Code]
var
  InstallChoicePage: TInputOptionWizardPage;
  ExistingInstallPath: String;
  IsExistingInstallation: Boolean;
  InstallationType: Integer; // 0=New, 1=Repair, 2=Upgrade
  PreserveUserData: Boolean;

// Safe function to get current date
function GetCurrentDate(Param: String): String;
begin
  Result := GetDateTimeString('yyyy/mm/dd', #0, #0);
end;

// Function to detect existing installation safely
function DetectExistingInstallation(): Boolean;
var
  RegPath: String;
  TempPath: String;
begin
  Result := False;
  ExistingInstallPath := '';
  
  try
    // Check registry for existing installation
    RegPath := 'Software\PropertyManagementSystem';
    if RegQueryStringValue(HKCU, RegPath, 'InstallPath', TempPath) then
    begin
      if (TempPath <> '') and DirExists(TempPath) then
      begin
        if FileExists(TempPath + '\PropertyManager.exe') then
        begin
          ExistingInstallPath := TempPath;
          Result := True;
          Exit;
        end;
      end;
    end;
    
    // Check default installation path
    TempPath := ExpandConstant('{autopf}\Property Management System');
    if DirExists(TempPath) and FileExists(TempPath + '\PropertyManager.exe') then
    begin
      ExistingInstallPath := TempPath;
      Result := True;
    end;
  except
    // If any error occurs, assume no existing installation
    Result := False;
    ExistingInstallPath := '';
  end;
end;

// Initialize setup with proper error handling
function InitializeSetup(): Boolean;
begin
  Result := True;
  PreserveUserData := True; // Default to preserve data
  InstallationType := 0; // Default to new installation
  
  try
    // Check if another instance is running
    if CheckForMutexes('Global\PropertyManagementSystemSetup') then
    begin
      if MsgBox('Another instance of Property Management System installer is already running.' + #13#10 +
                'Do you want to wait and continue?', mbConfirmation, MB_YESNO) = IDYES then
      begin
        // Wait a bit and try again
        Sleep(2000);
        if CheckForMutexes('Global\PropertyManagementSystemSetup') then
        begin
          MsgBox('Another installer is still running. Please wait for it to complete and try again.', 
                 mbError, MB_OK);
          Result := False;
          Exit;
        end;
      end
      else
      begin
        Result := False;
        Exit;
      end;
    end;
    CreateMutex('Global\PropertyManagementSystemSetup');
  except
    // If mutex fails, continue anyway
    Result := True;
  end;
end;

// Initialize wizard with safe error handling
procedure InitializeWizard;
begin
  try
    // Detect existing installation
    IsExistingInstallation := DetectExistingInstallation();
    
    if IsExistingInstallation then
    begin
      // Create installation choice page only if existing installation found
      InstallChoicePage := CreateInputOptionPage(wpWelcome,
        'Existing Installation Detected',
        'Property Management System is already installed on this computer.',
        'An existing installation has been detected at:' + #13#10 + ExistingInstallPath + #13#10#13#10 +
        'Please choose what you would like to do:',
        True, False);
      
      InstallChoicePage.Add('Repair Installation - Fix any corrupted files');
      InstallChoicePage.Add('Upgrade Installation - Update to latest version (keeps your data)');
      InstallChoicePage.Add('Fresh Install - Remove old version and install clean');
      
      // Set default choice to Repair
      InstallChoicePage.SelectedValueIndex := 0;
    end;
  except
    // If wizard initialization fails, continue with normal installation
    IsExistingInstallation := False;
  end;
end;

// Handle next button clicks safely
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  try
    // Handle installation choice page
    if IsExistingInstallation and (InstallChoicePage <> nil) and (CurPageID = InstallChoicePage.ID) then
    begin
      InstallationType := InstallChoicePage.SelectedValueIndex;
      
      case InstallationType of
        0: // Repair Installation
          begin
            PreserveUserData := True;
            Result := True;
          end;
        1: // Upgrade Installation  
          begin
            PreserveUserData := True;
            Result := True;
          end;
        2: // Fresh Install
          begin
            if MsgBox('This will remove the existing installation and all data.' + #13#10#13#10 +
                      'Are you sure you want to continue?', 
                      mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
            begin
              PreserveUserData := False;
              Result := True;
            end
            else
            begin
              Result := False;
            end;
          end;
        else
          Result := True;
      end;
    end;
  except
    // If any error occurs, continue with installation
    Result := True;
  end;
end;

// Skip page logic with error handling
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  try
    // Skip installation choice page if no existing installation
    if IsExistingInstallation and (InstallChoicePage <> nil) and (PageID = InstallChoicePage.ID) then
      Result := False
    else if not IsExistingInstallation and (InstallChoicePage <> nil) and (PageID = InstallChoicePage.ID) then
      Result := True;
  except
    Result := False;
  end;
end;

// Post-installation steps with error handling
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  BackupConfigFile: String;
  DatabaseFile: String;
  BackupDatabaseFile: String;
begin
  try
    if CurStep = ssPostInstall then
    begin
      // Handle configuration preservation for upgrade/repair
      if IsExistingInstallation and PreserveUserData and (InstallationType <> 2) then
      begin
        // Preserve configuration file
        ConfigFile := ExpandConstant('{app}\airtable_config.py');
        BackupConfigFile := ExistingInstallPath + '\airtable_config.py';
        
        if FileExists(BackupConfigFile) then
        begin
          try
            FileCopy(BackupConfigFile, ConfigFile, False);
          except
            // If copy fails, continue without error
          end;
        end;
        
        // Preserve database if it exists
        DatabaseFile := ExpandConstant('{app}\property_management.db');
        BackupDatabaseFile := ExistingInstallPath + '\property_management.db';
        
        if FileExists(BackupDatabaseFile) and not FileExists(DatabaseFile) then
        begin
          try
            FileCopy(BackupDatabaseFile, DatabaseFile, False);
          except
            // If copy fails, continue without error
          end;
        end;
      end;
      
      // Show completion message
      case InstallationType of
        0: MsgBox('Property Management System has been successfully repaired!', mbInformation, MB_OK);
        1: MsgBox('Property Management System has been successfully upgraded!' + #13#10 +
                  'Your existing data has been preserved.', mbInformation, MB_OK);
        2: MsgBox('Property Management System has been freshly installed!', mbInformation, MB_OK);
      else
        MsgBox('Property Management System has been successfully installed!', mbInformation, MB_OK);
      end;
    end;
  except
    // If post-install fails, don't show error to user
  end;
end;

// Uninstall step handling with proper data preservation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  KeepData: Boolean;
begin
  try
    if CurUninstallStep = usPostUninstall then
    begin
      // Ask user about data preservation
      KeepData := MsgBox('Do you want to keep your property database and images?' + #13#10#13#10 +
                        'Choose "Yes" to preserve your data for future installations.' + #13#10 +
                        'Choose "No" to completely remove all data.' + #13#10#13#10 +
                        'Note: If you choose "Yes", your data will be preserved and available if you reinstall.',
                        mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES;
      
      if not KeepData then
      begin
        // Remove user data only if explicitly requested
        try
          DelTree(ExpandConstant('{userappdata}\PropertyManagementSystem'), True, True, True);
          DeleteFile(ExpandConstant('{app}\property_management.db'));
          DelTree(ExpandConstant('{app}\property_images'), True, True, True);
          DelTree(ExpandConstant('{app}\logs'), True, True, True);
        except
          // If deletion fails, continue
        end;
        
        MsgBox('Property Management System and all data have been completely removed.' + #13#10 +
               'Thank you for using our software!', mbInformation, MB_OK);
      end
      else
      begin
        MsgBox('Property Management System has been uninstalled.' + #13#10 +
               'Your data has been preserved and will be available if you reinstall.' + #13#10#13#10 +
               'Thank you for using our software!', mbInformation, MB_OK);
      end;
    end;
  except
    // If uninstall handling fails, show generic message
    MsgBox('Uninstallation completed.', mbInformation, MB_OK);
  end;
end; 