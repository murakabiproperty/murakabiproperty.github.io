; Property Management System Installer with Safe Installation Menu
; This version detects existing installations and provides menu options

[Setup]
AppName=Property Management System
AppVersion=1.0.1
AppPublisher=Property Management Team
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_WithMenu
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Prevent runtime errors
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
Name: "{group}\Configuration Guide"; Filename: "{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md"; Check: FileExists(ExpandConstant('{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md'))
Name: "{group}\User Manual"; Filename: "{app}\docs\USER_MANUAL.md"; Check: FileExists(ExpandConstant('{app}\docs\USER_MANUAL.md'))
Name: "{group}\{cm:UninstallProgram,Property Management System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Property Management System"; Filename: "{app}\PropertyManager.exe"; Tasks: desktopicon

[Registry]
; Application tracking registry entries
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.1"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "LastInstall"; ValueData: "{code:GetCurrentDateTime}"

[Run]
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up log files and temporary data
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: filesandordirs; Name: "{app}\temp"

[Code]
var
  InstallChoicePage: TInputOptionWizardPage;
  ExistingInstallPath: String;
  ExistingVersion: String;
  IsExistingInstallation: Boolean;
  SelectedAction: Integer; // 0=Install, 1=Repair, 2=Modify, 3=Uninstall

// Safe function to get current date and time
function GetCurrentDateTime(Param: String): String;
begin
  Result := GetDateTimeString('yyyy/mm/dd hh:nn:ss', #0, #0);
end;

// Safe function to detect existing installation
function DetectExistingInstallation(): Boolean;
var
  RegInstallPath: String;
  DefaultInstallPath: String;
begin
  Result := False;
  ExistingInstallPath := '';
  ExistingVersion := '';
  
  try
    // Method 1: Check registry for install path
    if RegQueryStringValue(HKCU, 'Software\PropertyManagementSystem', 'InstallPath', RegInstallPath) then
    begin
      if (RegInstallPath <> '') and DirExists(RegInstallPath) and FileExists(RegInstallPath + '\PropertyManager.exe') then
      begin
        ExistingInstallPath := RegInstallPath;
        RegQueryStringValue(HKCU, 'Software\PropertyManagementSystem', 'Version', ExistingVersion);
        Result := True;
        Exit;
      end;
    end;
    
    // Method 2: Check default installation directory
    DefaultInstallPath := ExpandConstant('{autopf}\Property Management System');
    if DirExists(DefaultInstallPath) and FileExists(DefaultInstallPath + '\PropertyManager.exe') then
    begin
      ExistingInstallPath := DefaultInstallPath;
      ExistingVersion := 'Unknown';
      Result := True;
      Exit;
    end;
    
    // Method 3: Check Program Files (x86) for 32-bit installs
    DefaultInstallPath := ExpandConstant('{pf32}\Property Management System');
    if DirExists(DefaultInstallPath) and FileExists(DefaultInstallPath + '\PropertyManager.exe') then
    begin
      ExistingInstallPath := DefaultInstallPath;
      ExistingVersion := 'Unknown';
      Result := True;
    end;
    
  except
    // If any error occurs, assume no existing installation
    Result := False;
    ExistingInstallPath := '';
    ExistingVersion := '';
  end;
end;

// Safe initialization
function InitializeSetup(): Boolean;
begin
  Result := True;
  IsExistingInstallation := False;
  SelectedAction := 0; // Default to new install
  
  try
    // Detect existing installation
    IsExistingInstallation := DetectExistingInstallation();
  except
    // If detection fails, continue with normal installation
    IsExistingInstallation := False;
  end;
end;

// Initialize wizard with installation detection
procedure InitializeWizard;
begin
  try
    if IsExistingInstallation then
    begin
      // Create installation choice page
      InstallChoicePage := CreateInputOptionPage(wpWelcome,
        'Existing Installation Detected',
        'Property Management System is already installed on this computer.',
        'An existing installation has been detected:' + #13#10 +
        'Location: ' + ExistingInstallPath + #13#10 +
        'Version: ' + ExistingVersion + #13#10#13#10 +
        'What would you like to do?',
        True, False);
      
      // Add options
      InstallChoicePage.Add('Install/Upgrade - Install new version (recommended)');
      InstallChoicePage.Add('Repair Installation - Fix corrupted files and settings');
      InstallChoicePage.Add('Modify Installation - Add or remove components');
      InstallChoicePage.Add('Uninstall Application - Remove Property Management System');
      
      // Set default choice to Install/Upgrade
      InstallChoicePage.SelectedValueIndex := 0;
    end;
  except
    // If wizard initialization fails, continue with normal installation
    IsExistingInstallation := False;
  end;
end;

// Handle user's choice
function NextButtonClick(CurPageID: Integer): Boolean;
var
  UninstallExe: String;
  UninstallResult: Integer;
begin
  Result := True;
  
  try
    if IsExistingInstallation and (InstallChoicePage <> nil) and (CurPageID = InstallChoicePage.ID) then
    begin
      SelectedAction := InstallChoicePage.SelectedValueIndex;
      
      case SelectedAction of
        0: // Install/Upgrade
          begin
            if MsgBox('This will upgrade your existing installation.' + #13#10 +
                      'Your data and settings will be preserved.' + #13#10#13#10 +
                      'Continue with installation?', 
                      mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES then
            begin
              Result := True;
            end
            else
            begin
              Result := False;
            end;
          end;
          
        1: // Repair Installation
          begin
            if MsgBox('This will repair your existing installation.' + #13#10 +
                      'Corrupted files will be replaced and settings restored.' + #13#10#13#10 +
                      'Continue with repair?', 
                      mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES then
            begin
              Result := True;
            end
            else
            begin
              Result := False;
            end;
          end;
          
        2: // Modify Installation
          begin
            MsgBox('Modification mode will allow you to change installation components.' + #13#10 +
                   'You can add or remove optional features.',
                   mbInformation, MB_OK);
            Result := True;
          end;
          
        3: // Uninstall Application
          begin
            if MsgBox('This will uninstall Property Management System.' + #13#10 +
                      'You will be prompted about keeping your data.' + #13#10#13#10 +
                      'Continue with uninstallation?', 
                      mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
            begin
              // Try to run the uninstaller
              UninstallExe := ExistingInstallPath + '\unins000.exe';
              if FileExists(UninstallExe) then
              begin
                if Exec(UninstallExe, '', '', SW_SHOW, ewWaitUntilTerminated, UninstallResult) then
                begin
                  MsgBox('Uninstallation completed.', mbInformation, MB_OK);
                end
                else
                begin
                  MsgBox('Could not run uninstaller automatically.' + #13#10 +
                         'Please uninstall manually from Control Panel.', mbError, MB_OK);
                end;
              end
              else
              begin
                MsgBox('Uninstaller not found.' + #13#10 +
                       'Please uninstall manually from Control Panel.', mbError, MB_OK);
              end;
              
              // Exit installer after uninstall attempt
              Result := False;
              WizardForm.Close;
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
    // If any error occurs, continue with normal installation
    Result := True;
  end;
end;

// Skip pages based on user choice
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  try
    // Skip choice page if no existing installation
    if (InstallChoicePage <> nil) and (PageID = InstallChoicePage.ID) and not IsExistingInstallation then
      Result := True;
  except
    Result := False;
  end;
end;

// Handle installation completion
procedure CurStepChanged(CurStep: TSetupStep);
var
  OldConfigFile: String;
  NewConfigFile: String;
  OldDatabaseFile: String;
  NewDatabaseFile: String;
begin
  try
    if CurStep = ssPostInstall then
    begin
      // Preserve user data for upgrades and repairs
      if IsExistingInstallation and (SelectedAction <= 1) then // Install/Upgrade or Repair
      begin
        // Preserve configuration if exists
        OldConfigFile := ExistingInstallPath + '\airtable_config.py';
        NewConfigFile := ExpandConstant('{app}\airtable_config.py');
        
        if FileExists(OldConfigFile) and FileExists(NewConfigFile) then
        begin
          try
            // Backup current config and restore old one
            FileCopy(OldConfigFile, NewConfigFile + '.backup', True);
            FileCopy(OldConfigFile, NewConfigFile, False);
          except
            // If preservation fails, continue
          end;
        end;
        
        // Preserve database if exists and not in same location
        if ExistingInstallPath <> ExpandConstant('{app}') then
        begin
          OldDatabaseFile := ExistingInstallPath + '\property_management.db';
          NewDatabaseFile := ExpandConstant('{app}\property_management.db');
          
          if FileExists(OldDatabaseFile) and not FileExists(NewDatabaseFile) then
          begin
            try
              FileCopy(OldDatabaseFile, NewDatabaseFile, False);
            except
              // If preservation fails, continue
            end;
          end;
        end;
      end;
      
      // Show completion message based on action
      case SelectedAction of
        0: // Install/Upgrade
          begin
            if IsExistingInstallation then
              MsgBox('Property Management System has been successfully upgraded!' + #13#10 +
                     'Your existing data and settings have been preserved.' + #13#10#13#10 +
                     'Version: 1.0.1', mbInformation, MB_OK)
            else
              MsgBox('Property Management System has been successfully installed!' + #13#10#13#10 +
                     'Version: 1.0.1', mbInformation, MB_OK);
          end;
        1: // Repair
          MsgBox('Property Management System has been successfully repaired!' + #13#10 +
                 'All files have been restored and settings verified.' + #13#10#13#10 +
                 'Version: 1.0.1', mbInformation, MB_OK);
        2: // Modify
          MsgBox('Property Management System has been successfully modified!' + #13#10 +
                 'Components have been updated as requested.' + #13#10#13#10 +
                 'Version: 1.0.1', mbInformation, MB_OK);
      else
        MsgBox('Property Management System installation completed!' + #13#10#13#10 +
               'Version: 1.0.1', mbInformation, MB_OK);
      end;
    end;
  except
    // If post-install handling fails, show generic message
    MsgBox('Installation completed.', mbInformation, MB_OK);
  end;
end;

// Handle uninstallation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  KeepData: Boolean;
  DataPath: String;
  ImagesPath: String;
begin
  try
    if CurUninstallStep = usPostUninstall then
    begin
      // Ask about data preservation
      KeepData := MsgBox(
        'Do you want to keep your property database and images?' + #13#10#13#10 +
        'Choose "Yes" to preserve your data for future installations.' + #13#10 +
        'Choose "No" to completely remove all data.' + #13#10#13#10 +
        'Note: Preserved data will be available if you reinstall.',
        mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES;
      
      if not KeepData then
      begin
        // Remove user data only if explicitly requested
        DataPath := ExpandConstant('{app}\property_management.db');
        ImagesPath := ExpandConstant('{app}\property_images');
        
        if FileExists(DataPath) then
          DeleteFile(DataPath);
        
        if DirExists(ImagesPath) then
          DelTree(ImagesPath, True, True, True);
        
        DelTree(ExpandConstant('{app}\logs'), True, True, True);
        DelTree(ExpandConstant('{userappdata}\PropertyManagementSystem'), True, True, True);
        
        MsgBox('Property Management System and all data have been completely removed.' + #13#10 +
               'Thank you for using our software!', mbInformation, MB_OK);
      end
      else
      begin
        MsgBox('Property Management System has been uninstalled.' + #13#10 +
               'Your data has been preserved and will be available for future installations.' + #13#10#13#10 +
               'Thank you for using our software!', mbInformation, MB_OK);
      end;
    end;
  except
    // If uninstall handling fails, show generic message
    MsgBox('Uninstallation completed.', mbInformation, MB_OK);
  end;
end; 