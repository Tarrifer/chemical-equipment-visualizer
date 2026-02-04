# Chemical Equipment Visualizer

This project is a hybrid application consisting of a web application and a desktop application, both powered by a common Django backend.  
The system is designed to upload, analyze, visualize, and report chemical equipment data from CSV files.

---

## Project Structure

- backend/        → Django backend (common for web and desktop)
- web_app/        → React-based web application
- desktop_app/    → PyQt5-based desktop application (Windows)

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite

### Web Application
- React (Vite)
- Axios
- Bootstrap
- Chart.js

### Desktop Application
- Python
- PyQt5
- Requests

---

## Backend Setup 

The backend must be running before starting either the web app or the desktop app.

```
cd backend
python manage.py migrate
python manage.py runserver 8001
```

### Backend URL:

http://127.0.0.1:8001/

### Admin Panel:
Django admin panel is available at:

http://127.0.0.1:8001/admin/

### Create an admin user using:

```
python manage.py createsuperuser
```

## Web Application Setup
```
cd web_app
npm install
npm run dev
```

### Open in browser:

http://localhost:5173

### Web App Usage:

- Sign up or log in
- Upload a CSV file
- View summary statistics and charts
- Download PDF report
- View upload history

## Desktop Application (Executable)

- The Windows executable was generated using PyInstaller.
- Due to GitHub file size limits, the executable is not included in this repository.
- To generate the executable locally:

```
cd desktop_app
python -m PyInstaller main.py --onefile --windowed --name ChemicalEquipmentVisualizer --icon assets/icon.ico --add-data "ui;ui" --add-data "assets;assets"
```

## Desktop Application Setup (Windows)

```
cd desktop_app
python main.py
```

### Desktop App Usage:

- Sign up or log in
- Upload a CSV file
- View summary and charts
- Download PDF report
- View upload history
- The desktop application uses the same backend and authentication system as the web application.

## CSV File Format

The uploaded CSV file should contain columns such as:

- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

A sample CSV file is included in the project for testing.

### Features:

- Common backend for web and desktop
- Token-based authentication
- CSV upload and validation
- Data summary and visualization
- PDF report generation
- Upload history tracking
- Password show/hide in login and signup
- Windows desktop support

## Notes:

- Backend must be running before using web or desktop app
- This project was developed as part of an intern screening task
- Focus is on functionality, integration, and clean structure
- After building with PyInstaller, the application can also be run directly using:
  - desktop_app/dist/ChemicalEquipmentVisualizer.exe
  - Backend must be running before launching the executable.
- Pre-built Windows executable (optional): https://drive.google.com/drive/folders/19cCsa4FzzqfCpw3VQkJeb_S8IQayTp9p?usp=sharing
- This project uses Python version 3.11.8
  
## Author:

Rahul Das
