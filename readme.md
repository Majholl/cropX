<div style="text-align: center;">
  <img src="./icon/Capture.JPG" width="250px" height="200px" />
</div>

<h1 style="text-align: center;">CropX - Image Processing Tool</h1>

<p> CropX is a Django-based image processing tool that allows users to manipulate .tiff images, including  <b>rotating</b>, <b>reordering</b>, <b>deleting</b> and merging multiple images into a single TIFF file. The project is designed for efficient image handling in web applications</p>


# Features
-✅ Upload and process .tiff images

-✅ Rotate and Delete images easily

-✅ Merge multiple images into a single .tiff file

-✅ Download the processed file

-✅ Supports Django backend with JavaScript (Fetch API) frontend


## Tech Stack
-Backend:  <b>Django, Pillow (PIL)</b>

-Frontend: <b> JavaScript (Fetch API, Sortable.js)</b>

-Database:  <b>SQLite</b> (can be switched to PostgreSQL or MySQL for you own purpose)

-Version Control: <b>Git & GitHub</b>

<hr>

### Requirements
- python = 3.11.5
- django = 5.1.6
- pillow 11.1.0


#### How to run
- First download Python on  <img src='./icon/pngwing.com.png' width='15px' height='15px'> <a href='https://www.python.org/'>Python Page</a>
- Simply clone the project 
- Make venv 
```bash
>>> python -m venv .venv
```

- activate it by navigating to 
``` bash
  >>> cd .venv/Sctipts/
  >>> activate or activate.bat
  >>> cd ../..
```

- After successfully activating run following command to install dependent libraries 
```bash 
>>> pip install requiremenets.txt
```

- Run these command's in a single line
```bash 
>>> py manage.py makemigrations 
>>> py manage.py migrate 
```

- Finally run the server 
``` bash 
>>> py manage.py runserver
```

<a href="http://127.0.0.1:8000/" target="_blank">
  🚀 The server is running! Click here to open it in your browser.
</a>

 - "See the file <b>cropX/tiff/management/commands/removeImgdir.py</b> for running a cron job that removes unused directories after a certain period to prevent disk space from being filled up."
<hr>


#### License

This project is open-source and free to use.

Feel free to open issues or submit pull requests! 🚀