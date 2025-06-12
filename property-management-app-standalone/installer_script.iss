; Property Management System Installer Script
; Created for Inno Setup 6.x
; This creates a professional Windows installer with wizard interface

[Setup]
; Basic Information
AppName=Property Management System
AppVersion=1.0.0
AppPublisher=Property Management Team
AppPublisherURL=https://github.com/yourusername/property-management
AppSupportURL=https://github.com/yourusername/property-management
AppUpdatesURL=https://github.com/yourusername/property-management
DefaultDirName={autopf}\Property Management System
DefaultGroupName=Property Management System
AllowNoIcons=yes
; LicenseFile=LICENSE.txt
InfoBeforeFile=INSTALL_INFO.txt
InfoAfterFile=AIRTABLE_INTEGRATION_GUIDE.md
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
PrivilegesRequired=admin

; Visual customization - Using your website logo
WizardImageFile=wizard_image.bmp
WizardSmallImageFile=wizard_small.bmp

; Version Information
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Property Management Team
VersionInfoDescription=Property Management System Installer
VersionInfoCopyright=Copyright (C) 2024

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associatefiles"; Description: "Associate .pmdb files with Property Management System"; GroupDescription: "File associations:"
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Main application files
Source: "installer_files\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Documentation
Source: "AIRTABLE_INTEGRATION_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "USER_MANUAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion
; Configuration templates
Source: "airtable_config.py"; DestDir: "{app}"; Flags: ignoreversion confirmoverwrite
; Icon files
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; README files (optional)
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme; Check: FileExists('README.md')

[Icons]
Name: "{group}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\Configuration Guide"; Filename: "{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md"
Name: "{group}\User Manual"; Filename: "{app}\docs\USER_MANUAL.md"
Name: "{group}\{cm:UninstallProgram,Property Management System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Property Management System"; Filename: "{app}\PropertyManager.exe"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Property Management System"; Filename: "{app}\PropertyManager.exe"; Tasks: quicklaunchicon

[Registry]
; File associations
Root: HKCR; Subkey: ".pmdb"; ValueType: string; ValueName: ""; ValueData: "PropertyManagementDB"; Flags: uninsdeletevalue; Tasks: associatefiles
Root: HKCR; Subkey: "PropertyManagementDB"; ValueType: string; ValueName: ""; ValueData: "Property Management Database"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "PropertyManagementDB\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\PropertyManager.exe,0"; Tasks: associatefiles
Root: HKCR; Subkey: "PropertyManagementDB\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\PropertyManager.exe"" ""%1"""; Tasks: associatefiles

; Application settings
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\PropertyManagementSystem"; ValueType: string; ValueName: "Version"; ValueData: "1.0.0"

[Run]
; Optional: Run application after installation
Filename: "{app}\PropertyManager.exe"; Description: "{cm:LaunchProgram,Property Management System}"; Flags: nowait postinstall skipifsilent
; Open documentation
Filename: "{app}\docs\AIRTABLE_INTEGRATION_GUIDE.md"; Description: "Open Setup Guide"; Flags: postinstall skipifsilent shellexec unchecked

[UninstallDelete]
Type: files; Name: "{app}\property_management.db"
Type: files; Name: "{app}\*.log"
Type: filesandordirs; Name: "{app}\property_images"
Type: filesandordirs; Name: "{app}\__pycache__"

[Code]
// Helper function to check if file exists
function FileExists(FileName: String): Boolean;
begin
  Result := FileOrDirExists(FileName);
end;

// Global variables for installation detection and user choice
var
  ConfigPage: TInputQueryWizardPage;
  InstallChoicePage: TInputOptionWizardPage;
  AirtableAPIKey: String;
  AirtableBaseID: String;
  ExistingInstallPath: String;
  ExistingVersion: String;
  InstallationType: Integer; // 0=New, 1=Repair, 2=Upgrade, 3=Uninstall
  IsExistingInstallation: Boolean;

// Function to detect existing installation
function DetectExistingInstallation(): Boolean;
var
  RegPath: String;
  UninstallString: String;
begin
  Result := False;
  ExistingInstallPath := '';
  ExistingVersion := '';
  
  // Check registry for existing installation
  RegPath := 'Software\PropertyManagementSystem';
  if RegQueryStringValue(HKCU, RegPath, 'InstallPath', ExistingInstallPath) then
  begin
    RegQueryStringValue(HKCU, RegPath, 'Version', ExistingVersion);
    
    // Verify installation directory exists and has main executable
    if DirExists(ExistingInstallPath) and FileExists(ExistingInstallPath + '\PropertyManager.exe') then
    begin
      Result := True;
    end;
  end;
  
  // Also check default installation path
  if not Result then
  begin
    ExistingInstallPath := ExpandConstant('{autopf}\Property Management System');
    if DirExists(ExistingInstallPath) and FileExists(ExistingInstallPath + '\PropertyManager.exe') then
    begin
      Result := True;
      ExistingVersion := 'Unknown';
    end;
  end;
end;

// Function to get uninstall string from registry
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\Property Management System_is1';
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

// Function to run uninstaller
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := iResultCode
    else
      Result := -1;
  end else
    Result := -1;
end;

procedure InitializeWizard;
begin
  // Detect existing installation
  IsExistingInstallation := DetectExistingInstallation();
  
  if IsExistingInstallation then
  begin
    // Create installation choice page
    InstallChoicePage := CreateInputOptionPage(wpWelcome,
      'Existing Installation Detected',
      'Property Management System is already installed on this computer.',
      'An existing installation has been detected. Please choose what you would like to do:',
      True, False);
    
    InstallChoicePage.Add('Repair Installation - Fix any corrupted files and restore default settings');
    InstallChoicePage.Add('Upgrade Installation - Update to the latest version (preserves data)');
    InstallChoicePage.Add('Uninstall Existing - Remove the current installation completely');
    InstallChoicePage.Add('Cancel - Exit the installer without making changes');
    
    // Set default choice to Repair
    InstallChoicePage.SelectedValueIndex := 0;
  end;
  
  // Create custom configuration page
  ConfigPage := CreateInputQueryPage(wpSelectDir,
    'Airtable Configuration', 'Enter your Airtable credentials',
    'Please enter your Airtable API key and Base ID. You can skip this and configure later.');
  
  ConfigPage.Add('Airtable API Key:', False);
  ConfigPage.Add('Airtable Base ID:', False);
  
  // Set default values
  ConfigPage.Values[0] := 'your-api-key-here';
  ConfigPage.Values[1] := 'your-base-id-here';
  
  // If upgrading/repairing, try to load existing config
  if IsExistingInstallation and FileExists(ExistingInstallPath + '\airtable_config.py') then
  begin
    // Try to read existing configuration (simplified)
    ConfigPage.Values[0] := 'Existing configuration will be preserved';
    ConfigPage.Values[1] := 'Existing configuration will be preserved';
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  UninstallResult: Integer;
begin
  Result := True;
  
  // Handle installation choice page
  if (CurPageID = InstallChoicePage.ID) and IsExistingInstallation then
  begin
    InstallationType := InstallChoicePage.SelectedValueIndex;
    
    case InstallationType of
      0: // Repair Installation
        begin
          // Continue with installation process
          Result := True;
        end;
      1: // Upgrade Installation
        begin
          // Continue with installation process, preserving data
          Result := True;
        end;
      2: // Uninstall Existing
        begin
          if MsgBox('Are you sure you want to uninstall Property Management System?' + #13#10 +
                    'This will remove the application and all its components.' + #13#10#13#10 +
                    'Your data files may be preserved depending on your choice during uninstallation.',
                    mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
          begin
            // Run uninstaller
            UninstallResult := UnInstallOldVersion();
            if UninstallResult = 0 then
            begin
              MsgBox('The previous installation has been successfully removed.', mbInformation, MB_OK);
              // Exit installer after uninstall
              Result := False;
              WizardForm.Close;
            end
            else
            begin
              MsgBox('Failed to uninstall the existing version. Error code: ' + IntToStr(UninstallResult) + #13#10 +
                     'You may need to uninstall manually from Control Panel.',
                     mbError, MB_OK);
              Result := False;
            end;
          end
          else
            Result := False;
        end;
      3: // Cancel
        begin
          Result := False;
          WizardForm.Close;
        end;
    end;
  end;
  
  // Handle configuration page
  if CurPageID = ConfigPage.ID then
  begin
    AirtableAPIKey := ConfigPage.Values[0];
    AirtableBaseID := ConfigPage.Values[1];
    
    // Skip validation if preserving existing config
    if (AirtableAPIKey = 'Existing configuration will be preserved') then
    begin
      Result := True;
    end
    else
    begin
      // Validate inputs (basic check)
      if (Length(AirtableAPIKey) > 0) and (AirtableAPIKey <> 'your-api-key-here') then
      begin
        if (Length(AirtableBaseID) > 0) and (AirtableBaseID <> 'your-base-id-here') then
        begin
          // Input looks valid
          Result := True;
        end
        else
        begin
          if MsgBox('Base ID appears to be invalid. Continue anyway?', mbConfirmation, MB_YESNO) = IDNO then
            Result := False;
        end;
      end
      else
      begin
        if MsgBox('API Key appears to be invalid. You can configure this later. Continue?', mbConfirmation, MB_YESNO) = IDNO then
          Result := False;
      end;
    end;
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  // Skip configuration page if uninstalling
  if (PageID = ConfigPage.ID) and (InstallationType = 2) then
    Result := True;
    
  // Skip installation choice page if no existing installation
  if (PageID = InstallChoicePage.ID) and not IsExistingInstallation then
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  ConfigContent: String;
  BackupConfigFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Handle configuration based on installation type
    ConfigFile := ExpandConstant('{app}\airtable_config.py');
    
    // For repair/upgrade, try to preserve existing configuration
    if IsExistingInstallation and (InstallationType = 1) then // Upgrade
    begin
      BackupConfigFile := ExistingInstallPath + '\airtable_config.py';
      if FileExists(BackupConfigFile) and FileExists(ConfigFile) then
      begin
        // Copy existing config over new one
        FileCopy(BackupConfigFile, ConfigFile, False);
      end;
    end;
    
    // Update configuration file with user inputs (if new values provided)
    if (AirtableAPIKey <> '') and (AirtableAPIKey <> 'your-api-key-here') and 
       (AirtableAPIKey <> 'Existing configuration will be preserved') then
    begin
      // Load current config file
      if LoadStringFromFile(ConfigFile, ConfigContent) then
      begin
        // Replace placeholder values
        StringChangeEx(ConfigContent, 'pat0cJUQcyOFxDllX.1b4ef2922fe5c17c88ff46ec85e66d40e1d6fe9f45db53d43a79e9481680e728', AirtableAPIKey, True);
        StringChangeEx(ConfigContent, 'appx1T49Qqh0g3AcF', AirtableBaseID, True);
        
        // Save updated config
        SaveStringToFile(ConfigFile, ConfigContent, False);
      end;
    end;
    
    // Create application data directory
    CreateDir(ExpandConstant('{userappdata}\PropertyManagementSystem'));
    
    // Display completion message based on installation type
    case InstallationType of
      0: // Repair
        MsgBox('Property Management System has been successfully repaired!', mbInformation, MB_OK);
      1: // Upgrade
        MsgBox('Property Management System has been successfully upgraded!' + #13#10 +
               'Your existing data and configuration have been preserved.', mbInformation, MB_OK);
    end;
  end;
end;

// Check for prerequisites and existing installation
function InitializeSetup(): Boolean;
var
  ExecResult: Integer;
begin
  Result := True;
  
  // Check if another instance of the installer is running
  if CheckForMutexes('Global\PropertyManagementSystemSetup') then
  begin
    MsgBox('Another instance of Property Management System installer is already running. Please wait for it to complete.', 
           mbError, MB_OK);
    Result := False;
    Exit;
  end;
  CreateMutex('Global\PropertyManagementSystemSetup');
  
  // Additional prerequisite checks can be added here
  // Note: Prerequisite checking simplified to avoid installation issues
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Ask if user wants to keep data
    if MsgBox('Do you want to keep your property database and images?' + #13#10#13#10 +
              'Choose "Yes" to preserve your data for future installations.' + #13#10 +
              'Choose "No" to completely remove all data.',
              mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDNO then
    begin
      // Remove user data
      DelTree(ExpandConstant('{userappdata}\PropertyManagementSystem'), True, True, True);
      // Also remove database and images from installation directory
      DeleteFile(ExpandConstant('{app}\property_management.db'));
      DelTree(ExpandConstant('{app}\property_images'), True, True, True);
    end;
    
    MsgBox('Property Management System has been successfully uninstalled.' + #13#10 +
           'Thank you for using our software!', mbInformation, MB_OK);
  end;
end; 