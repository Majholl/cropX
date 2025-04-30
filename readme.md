<h1 style="text-align: center;">CropX - Tiff file Processing Tool</h1>

<p> CropX is a Django-based Tiff file processing tool that allows users to manipulate .tiff images, including 


# Features
-✅ Upload and process tiff file 

-✅ Rotate, delete and reorder images

-✅ Recreate tiff file by adding changes and prepare if for download 


# 🔧 Tech Stack
- <b>FronEnd by</b> : <a href='https://github.com/PAPAshady'><img src='icon/PAPAshady.jpg' width="20px" height="20px" style='border-radius:20px'></img>PAPAshady</a>

- <b>BackEnd by</b> : <a href='https://github.com/Majholl'><img src='icon/Majholl.jpg' width="20px" height="20px" style='border-radius:20px'></img>Majholl</a> 


- <b>Language</b> : Python

- <b>BackEnd</b> : Django / Rest-Framework 

- <b>Databse</b> : -


** Special thanks to PAPAshady for making it's frontend page <a href='https://github.com/PAPAshady/tiff-viewer'>Front end repo</a>

<hr>

### Requirements
- python = 3.11.5
- django = 5.2
- pillow = 11.1.0



## 📌 API Endpoints
 
| EndPoint |  Method | Description |
|----------|----------|----------|
| api/upload | POST | Upload tiff file|
| api/rotate | POST | Rotate list of imgs |
| api/delete | POST | Delete list of imgs|
| api/reorder| POST | Rorder list of imgs |

<b>Full doc </b>: <a href='https://www.postman.com/grey-escape-224969/workspace/nameless'>Full Documentation api requests</a>



#### How to run
⚠️  <b>dont forget to make .env file in same as the project folder and populate it with .env.exmaple  </b>

- First install python <a href='https://www.python.org/'>Python Page</a>
- Simply clone the project 
- Make <a href='https://stackoverflow.com/questions/43069780/how-to-create-virtual-env-with-python-3'>venv and activating it </a>
- After successfully activating run following command to install dependent libraries :
```bash 
>>> pip install -r requiremenets.txt
```
- Run these command's in a single line
```bash 
>>> py manage.py migrate 
```

- Finally run the server 
``` bash 
>>> py manage.py runserver
```

<a href="http://127.0.0.1:8000/" target="_blank">
  🚀 The server is running! Click here to open it in your browser.
</a>


<hr>



#### License

This project is open-source and free to use.
Feel free to open issues or submit pull requests! 🚀