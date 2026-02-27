MES WorkOrder Editor

A PyQt6-based desktop application for controlled modification of  parameters within multiple configuration `.ini` files that only start with a specific prefix.

Designed for Manufacturing Execution System (MES) environments where configuration integrity, traceability, and controlled parameter updates are required.

The application provides a structured interface to:

- Select production configuration files
- Update  values safely that start withh (your prefix )
- Manage and reorder WorkOrder options
- Prevent manual editing errors in production environments
- Enforce single-instance execution

---

Technical Overview

The application:

- Reads configuration paths from `settings.ini`
- Loads WorkOrder options from `options.ini`
- Updates  values in target `.ini` files
- Supports drag-and-drop reordering of WorkOrders (via Settings)
- Prevents multiple instances using a lock file
- Can be deployed as a standalone Windows executable

---

Recommended Project Structure

mes-workorder-editor/
│
├── work_order_editor.py      # Main application
├── icon.ico                  # Application icon
├── README.md
├── requirements.txt
│
├── settings.ini              # Stores config file paths (auto-created if missing)
├── options.ini               # Stores WorkOrder options (auto-created if missing)
│
├── model 1.ini                    # Target production configs
├── model 2.ini
├── model 3.ini
├── model 4.ini
├── model 5.ini

---
System Requirements

Development Requirements

- Python 3.9+
- Windows 10 / 11 (primary target environment)
- pip

Python Dependencies



PyQt6>=6.5

Install dependencies:


---
Running in Development Mode

python work_order_editor.py

---

Building a Standalone Executable (Windows)

Install PyInstaller:

pip install pyinstaller

Build command:

pyinstaller --onefile --windowed ^
--name "MES-WorkOrder-Editor" ^
--icon="icon.ico" ^
work_order_editor.py

The compiled executable will be located in:

dist/MES-WorkOrder-Editor.exe

---

Including Default Configuration Files in Build

pyinstaller --onefile --windowed ^
--name "MES-WorkOrder-Editor" ^
--icon="icon.ico" ^
--add-data "settings.ini;." ^
--add-data "options.ini;." ^
work_order_editor.py

 On macOS/Linux replace `;` with `:` in --add-data.

---

Configuration Files

settings.ini

Stores file paths for each configuration:

[Paths]
model 1=C:\MES\Config\model 1.ini
model 2=C:\MES\Config\model 2.ini

If missing, defaults are generated automatically.

---

options.ini
Stores selectable WorkOrder values:
[model 1]
WorkOrderOptions=OptionA|OptionB|OptionC

Single Instance Protection

The application creates:

WorkOrderEditor.lock

If this file exists, a second instance will not launch.  
The lock file is removed on proper shutdown.

---

Engineering Objectives

- Reduce risk of manual configuration edits
- Standardize parameter updates
- Support controlled MES workstation deployment
- Improve operator usability
- Maintain simple and predictable file-based configuration management


intended Environment

- Manufacturing workstations
- Controlled production PCs
- MES-connected systems
- Internal factory tooling


 License

Internal Engineering Tool  
(Replace with company license policy if needed)
