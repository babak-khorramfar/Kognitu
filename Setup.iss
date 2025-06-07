[Setup]
AppName=HipHop
AppVersion=1.0
DefaultDirName={pf}\HipHop
DefaultGroupName=HipHop
OutputBaseFilename=HipHopInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=dist\icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\HipHop.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\HipHop"; Filename: "{app}\HipHop.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall HipHop"; Filename: "{uninstallexe}"
Name: "{commondesktop}\HipHop"; Filename: "{app}\HipHop.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\HipHop.exe"; Description: "Launch HipHop"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCR; Subkey: ".hht"; ValueType: string; ValueData: "HipHop.HHT"; Flags: uninsdeletekey
Root: HKCR; Subkey: "HipHop.HHT"; ValueType: string; ValueData: "Kognitu Layout File"
Root: HKCR; Subkey: "HipHop.HHT\DefaultIcon"; ValueType: string; ValueData: "{app}\resources\images\hht.ico"
Root: HKCR; Subkey: "HipHop.HHT\shell\open\command"; ValueType: string; ValueData: """{app}\HipHop.exe"" ""%1"""

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked
