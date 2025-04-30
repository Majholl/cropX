# <p align="center">🌿 CropX - TIFF File Processing Tool</p>

CropX is a Django-based TIFF file processing tool that allows users to manipulate `.tiff` images, including rotation, deletion, and reordering.

---

## ✅ Features

- Upload and process TIFF files  
- Rotate, delete, and reorder images  
- Recreate TIFF file with changes and prepare it for download  

---

## 🔧 Tech Stack

- **Frontend by**:  
  [<img src="icon/PAPAshady.jpg" width="20px" height="20px" style="border-radius:50%;"> PAPAshady](https://github.com/PAPAshady)

- **Backend by**:  
  [<img src="icon/Majholl.jpg" width="20px" height="20px" style="border-radius:50%;"> Majholl](https://github.com/Majholl)

- **Language**: Python  
- **Backend**: Django / Django REST Framework  
- **Database**: – (No database used or specified)

> **Special thanks** to [PAPAshady](https://github.com/PAPAshady/tiff-viewer) for building the frontend UI.

---

## ⚙️ Requirements

- Python: `3.11.5`  
- Django: `5.2`  
- Pillow: `11.1.0`  

---

## 📌 API Endpoints

| Endpoint        | Method | Description               |
|-----------------|--------|---------------------------|
| `/api/upload`   | POST   | Upload TIFF file          |
| `/api/rotate`   | POST   | Rotate list of images     |
| `/api/delete`   | POST   | Delete list of images     |
| `/api/reorder`  | POST   | Reorder list of images    |

**Full docs**: [Postman API Collection](https://www.postman.com/grey-escape-224969/workspace/nameless)

---

## 🚀 How to Run

⚠️ **Don't forget to create a `.env` file in the project root and copy contents from `.env.example`.**

### 1. Install Python

Get it from the [official site](https://www.python.org/)

### 2. Clone the Project
<details>
<summary>📌Click to expand this section</summary>

```bash
git clone https://github.com/your-username/cropx.git # Clone the repo
cd cropx 
python -m venv venv # Make python env

# Activate it:
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows

pip install -r requirements.txt # Install depencies

python manage.py migrate # Add model to db
python manage.py runserver # Run server

```
Now visit: http://127.0.0.1:8000/
</details>

<hr>

### 💬 Contributors
Built with ❤️ by:
- Frontend: PAPAshady
- Backend: Majholl


#### License

This project is licensed as open-source and is free to use and contribute to.
Feel free to fork, star ⭐, or submit issues and PRs 🚀