# ONLINE SIRMUSO SCISSOR APP
## CONTENT
### Title
### Introduction 
### Project Environment
### Installation
### Folder Creation
### File Creation
### Authentication and Authorization
### Jinja2 Template
### What i learned
### Challenges
### Conclusion

# TITLE:
# ONLINE SHOPPING STORE AND BLOG WEBSITE.

# INTRODUCTION :
This project Sirmuso Scissor Websiteis a website that you can use to shorten your long url into something smaller and you can as well customized your own url with your domain name,the most exciting part is that you can get a QRCode for your url to get all informations about your url.
This website is fully authenticated and also a token  is required for users' full authorization to the website. 
This website is built using fast API framework and jinja2 template is used for the frontend side of this website.

The Welcome Page which is the landing page of the website contains all the other webpages. The website contains many web pages, user authentication, and authorization with a well-structured database that is used in storing all users' information, url inormation, and profile information.

# BUILT WITH:
<p align="left"> <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a>
<a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/></a>
<a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> 
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <br> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg"  alt="flask" width="40" height="40"/></a> </p>

# PROJECT ENVIRONMENT: 
This project requires a virtual environment for the proper functioning of the project. This section gives a short demonstration of how to create a virtual environment(windows users) which is as follows:
## Step 1:
Open your system command prompt from your window search bar "search command prompt".

## Step 2 :
Make a directory to your desktop or any preferable location.
### Command: cd Desktop
## Step 3:
Install virtual environment if not installed before.
### Command: pip install virtual environment
## Step 4:
Create your flask environment with any name you want. (i will be using flaskenv for demonstration)
### Command: virtualenv flaskenv
## Step 5:
Make a directory to your environment
### Command: cd flaskenv
## Step 6:
Make a directory to scripts
### Command: cd scripts
## Step 7:
Activate your environment
### Command: activate
Yes, your environment is ready for use.
### Note: The above illustrations are for windows users only.

# INSTALLATION:
This section contains all the packages to be installed for this project.
Before installation make sure your environment is activated and packages are installed in the terminal( e.g command prompt, PowerShell, Git Bash, etc) using  "pip install package".
## Packages to be installed:
### FastAPI
### uvicorn[standard]
### flask-sqlalchemy
### fastapi_jwt_auth
### python-jose
### Passlib
### Bcrypt
### Python-multipart
### Python-dotenv
### Pytest
### PyQRCode
### pypng
### request
### https
### Jinja2



### The command for installation:
pip install " package name"

# FOLDER CREATION:
This section contains all the folders required for the creation of this project.This folders include:

### Routers Folder
### Repository Folder
### Security Folder
### Templates Folder
### Static Folder
### Models Folder
### Test Folder


## BlogPosts Folder:
This folder contains all the files and folders in this project except the main.py file, virtual environment folder, and the requirements.txt file.
## Routers Folder:
user.py file 
profile.py file
authentication.py file
short_url.py file 
custom_url.py file
url_analysis.py file
qrcode.py file

## Repository Folder:
user.py file 
profile.py file
short_url.py file 
custom_url.py file
url_analysis.py file
qrcode.py file
 
## Security Folder
This folder contains some file which is the backbone for the proper authentication and authorization of this website.
These files include:
Hashing.py file
Oauth2.py file
Token.py file
error.py file
key_generator.py file
config.py file

## Models Folder
database.py file
models.py file
schemas.py file

## Tests Folder
test_main.py file
test_url.py file
test_profile.py file
test_user.py file


# FILE CREATION
This section contains all the files needed for the creation of this project which is:

## main.py
This file is the engine of the project which is used for running the project. 
It is used to run all API endpoints using FastAPI.
This file contains a declared app that is used to connect all routers to the API Endpoint. This also contained the display endpoints which are used to connect the API Endpoint with jinja2 template that is used to display some information.

# AUTHENTICATION AND AUTHORIZATION
This website authentication is solely based on Oauth2.
OAuth2 is a specification that defines several ways to handle authentication and authorization.
It is quite an extensive specification and covers several complex use cases.
It includes ways to authenticate using a "third party".
An OAUTH2PasswordBearer can be imported from fastapi security module.
This also has a built-in form known as the OUATH2PasswordRequestForm which is  an authorized form for user authorization.
Jwt and jwtError are imported from the python- Jose which is used to encode and decode tokens, data, secret keys, algorithms, and so on.

# JINJA2 Template
Jinja2 is a modern-day templating language for Python developers. It was made after Django’s template. It is used to create HTML, XML, or other markup formats that are returned to the user via an HTTP request.

## Using Jinja2Templates
#### Import Jinja2Templates.
#### Create a templates object that you can re-use later.
#### Declare a Request parameter in the path operation that will return a template.
#### Use the templates you created to render and return a TemplateResponse, passing the request as one of the key-value pairs in the Jinja2 "context".

The folders under jinja2 template are: 
### Static folder
### Templates folder

## Static Folder
### Main.css
The main.css file is the file that contains all the CSS styling for the website frontend side.

## Template Folder
### Base.html

### Home.html

### analysis.html
### custom_page.html

### custom.html

### dashboard.html
### profile_page.html

### qrcode.html
### settings.html

### signin.html

### signup.html
### upload_profile.html
### url_info.html

### welcome.html

The jinja2 template is the backbone of the client side in this project and used to displayed all information on the website.


# What I learned 
### How to generate an access token.
### Effectively use of pydantic schema.
### Swagger UI configuration.
### Full API authentication and authorization.
### Uploading of files and storing of files to the database.
### Retrieving uploaded images from the database to display on the website.
### Uploading of files to the static folder and any desired path.



# THE Challenges’
### How to reset a forgotten Password
### How to get images directly from database using fastapi.



# CONCLUSION
This project's Sirmuso Scissor App is a full stack project that allowed user to shorten their long url and can also get a QRcode for their url as well as customizing their own url. 

This project(both frontend and backend) is created by ADEYEMO MUSODIQ OLALEKAN an AltSchool Africa School of Engineering student.
This project is open for contribution.
You can contact me on WhatsApp  08141171294


<h1 align="left" font-weight="bold">Connect with me:</h1>
<p align="left">
<a href="https://twitter.com/sirmuso" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="sirmuso" height="30" width="40" /></a>
<a href="https://linkedin.com/in/musodiq-adeyemo" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="musodiq-adeyemo" height="30" width="40" /></a>
<a href="https://fb.com/https://www.facebook.com/adeyemo.musodiq" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="https://www.facebook.com/adeyemo.musodiq" height="30" width="40" /></a>
</p>

- 📫 How to reach me **adeyemomusodiq@gmail.com**

- ⚡ Fun fact **I'm currently studying at AltSchool Africa School of Software Engineering Class of 2022.**


You can contact me on WhatsApp at 08141171294

## GOD BLESS ALT SCHOOL  AFRICA






