
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it's better to be explicit
build_options = {
    'packages': ['tkinter', 'sqlite3', 'requests', 'urllib3', 'urllib3.util', 'urllib3.exceptions', 'urllib3.poolmanager', 'http', 'http.client', 'http.server', 'http.cookies', 'http.cookiejar', 'certifi', 'charset_normalizer', 'idna', 'PIL', 'pathlib', 'json', 'hashlib', 'datetime', 'os', 'shutil', 'webbrowser', 'urllib', 'urllib.parse', 'urllib.request', 'urllib.response', 'urllib.error', 'mimetypes'],
    'excludes': ['test', 'unittest', 'email', 'html', 'xml', 'pydoc'],
    'include_files': [
        ('airtable_config.py', 'airtable_config.py'),
        ('airtable_sync.py', 'airtable_sync.py'),
        ('AIRTABLE_INTEGRATION_GUIDE.md', 'AIRTABLE_INTEGRATION_GUIDE.md'),
        ('USER_MANUAL.md', 'USER_MANUAL.md'),
        ('requirements.txt', 'requirements.txt'),
        ('app_icon.ico', 'app_icon.ico')
    ],
    'optimize': 2
}

# GUI applications require a different base on Windows
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        target_name='PropertyManager.exe',
        icon='app_icon.ico',
        shortcut_name='Property Management System',
        shortcut_dir='DesktopFolder'
    )
]

setup(
    name='Property Management System',
    version='1.0.0',
    description='Desktop Property Management Application with Airtable Integration',
    author='Property Management Team',
    options={'build_exe': build_options},
    executables=executables
)
