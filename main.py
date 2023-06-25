import uvicorn
import validators
import pyqrcode
from fastapi import FastAPI,Request,Depends,HTTPException,Form,status,UploadFile,File
from routers import profile,qrcode,url_analysis
from routers import user,customs_url
from routers import authentication,short_urls
from fastapi.responses import HTMLResponse,RedirectResponse,Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.models import Profile,User,ProfileImage,URL,QR
from sqlalchemy.orm import Session
from models.database import get_db
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT
from models.schemas import Setting
from security.hashing import Hash
from werkzeug.utils import secure_filename
import shutil
from security.config import base_settings
from security.error import not_found
from security.key_generator import create_unique_key




app= FastAPI(
    docs_url = "/docs",
    redoc_url= "/redocs",
    title="SIRMUSO SCISSOR API",
    description="FRAMEWORK FOR SIRMUSO SCISSOR API",
    version="4.0",
    openapi_url="/api/v2/openapi.json"
    
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(short_urls.router)
app.include_router(customs_url.router)
app.include_router(url_analysis.router)
app.include_router(qrcode.router)

templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

access_token_expire =timedelta(minutes=120)
refresh_token_expire = timedelta(days=1)
new_access_token_expire = timedelta(days=7)
access_algorithm = "HS384"
refresh_algorithm = "HS512"

@AuthJWT.load_config
def get_config():
    return Setting()

@app.get("/main")
def read_main():
    return {"msg":"hello world"}

#Welcome page
@app.get("/",response_class=HTMLResponse,tags=["Template"])
def welcome(request: Request,Authorize:AuthJWT=Depends()):
    
    return templates.TemplateResponse("welcome.html",{"request":request})

# Home page
@app.get("/home",response_class=HTMLResponse,tags=["Template"])
def home(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/home",response_class=HTMLResponse,tags=["Template"])
def home(request: Request,original_url:str=Form(...),user_id:int=Form(...),Authorize:AuthJWT=Depends(),db:Session = Depends(get_db)):
    errors = []
    #check if URL already exist
    url_exist = db.query(URL).filter(URL.original_url == original_url).first()
    # validate the URL to be it is valid
    if not validators.url(original_url):
        errors.append(f"Your provided URL:{original_url} is not valid, Please verify")
    if url_exist:
        errors.append(f"Your provided URL:{original_url} already exist, Please verify")
    else:
        # Generating URL key
        url_key = create_unique_key(db)
        # Base environment URL
        base_url = base_settings().base_url
        # creating short URL
        short_url = str(base_url  + url_key)
        # saving URL into the database
        db_url = URL(
            original_url = original_url,
            user_id = user_id,
            short_url = short_url,
            url_key = url_key
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        redirect_url = "home/short_url"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("home.html",{"request":request,"original":original_url,"errors":errors})

# display home content
@app.get("/home/short_url",response_class=HTMLResponse,tags=["Template"])
def display(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    user_id = user.id
    urls = db.query(URL).order_by(URL.id.desc()).limit(1)
    return templates.TemplateResponse("home.html",{"request":request,"current_user":current_user,"user_id":user_id,"urls":urls})

# USER REGISTRATION
@app.get("/register",response_class=HTMLResponse,tags=["Template"])
def signup(request: Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@app.post("/register",response_class=HTMLResponse,tags=["Template"])
def signup(request: Request,username:str=Form(...),email:str=Form(...),password:str=Form(...),password2:str=Form(...), db:Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.username==username).first()
    email_exist = db.query(User).filter(User.email==email).first()
    errors=[]

    if email_exist:
        errors.append("Email Already Exist,Login or Change Email.")

    if user_exist:
        errors.append("Username Already Exist,Try another one.")
    
    if not email :
        errors.append("Not a proper Email")

    if password == password2 and len(password) > 7 :
        new_user = User(username=username,email=email,password=Hash.bcrypt(password))

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        redirect_url = "signin"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    
    if len(errors) > 0 :
        return templates.TemplateResponse("signup.html",{"request":request,"errors":errors})
    else:
        errors.append("Password dont match or less than 8 charaters")
        return templates.TemplateResponse("signup.html",{"request":request,"errors":errors})

#LOGIN AUTHENTICATION
@app.get("/signin",tags=["Template"])
def login(request: Request):
    return templates.TemplateResponse("signin.html",{"request":request})


@app.post("/signin",tags=["Template"])
def login(request: Request,response:Response,Authorize:AuthJWT=Depends(),username:str=Form(...),password:str=Form(...),db:Session = Depends(get_db)):
    errors = []
    user = db.query(User).filter(User.username==username).first()

    if user is None:
        errors.append("Invalid Credentials,Please check username or password")
        return templates.TemplateResponse("signin.html",{"request":request,"errors":errors})
    
    verify_password = Hash.verify_password(password,user.password)

    if (username == user.username and verify_password):
        access_token = Authorize.create_access_token(subject=user.username,expires_time=access_token_expire)
        redirect_url = "/profile_settings"
        resp = RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
        Authorize.set_access_cookies(access_token,resp)
        return resp
    else:
        errors.append("Invalid Credentials,Please check username or password")
        return templates.TemplateResponse("signin.html",{"request":request,"errors":errors})

# profile settings route
@app.get("/profile_settings",response_class=HTMLResponse,tags=["Template"])
def settings(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username==current_user).first()
    return templates.TemplateResponse("settings.html",{"request":request,"user":user})

@app.post("/profile_settings",response_class=HTMLResponse,tags=["Template"])
def settings(request: Request,user_id:int=Form(...),firstname:str=Form(...),lastname:str=Form(...),gender:str=Form(...),bio:str=Form(...), db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    errors = []
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        errors.append(f"Profile with user id : {user_id} already exists")
        return templates.TemplateResponse("settings.html",{"request":request,"errors":errors})
    else: 
        new_profile = Profile(lastname=lastname,user_id=user_id,bio=bio,gender=gender,firstname=firstname)
        db.add(new_profile)
        db.commit()
        redirect_url = "/profile"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)    
    
#profile page
@app.get("/profile",response_class=HTMLResponse,tags=["Template"])
def dashboard(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    current_user = Authorize.get_jwt_subject()
    users = db.query(User).all()
    profiles = db.query(Profile).all()
    images = db.query(ProfileImage).all()
    return templates.TemplateResponse("profile_page.html",{"request":request,"users":users,"profiles":profiles,'current_user':current_user,'images':images})

#update profile
@app.get("/profile/{id}",response_class=HTMLResponse,tags=["Template"])
def dashboard(request: Request,id:int,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    profile = db.query(Profile).filter(Profile.id == id).first()
    return templates.TemplateResponse("profile_page.html",{"request":request,"profile":profile})

@app.post("/profile/{id}",response_class=HTMLResponse,tags=["Template"])
def dashboard(request: Request, id:int,firstname:str=Form(...),lastname:str=Form(...),gender:str=Form(...),bio:str=Form(...), db:Session = Depends(get_db)):
    try:
        update_profile = db.query(Profile).filter(Profile.id == id).first()

        update_profile.lastname = lastname,
        update_profile.firstname = firstname,
        update_profile.bio = bio,
        update_profile.gender = gender,
    
        db.commit()
        redirect_url = "/profile"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    except:
        return templates.TemplateResponse("profile_page.html",{"request":request,"update_profile":update_profile})


#delete profile
@app.get("/delete_profile/{id}",response_class=HTMLResponse,tags=["Template"])
def profile_delete(request: Request,id:int,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    delete_profile = db.query(Profile).filter(Profile.id == id).first()
    if delete_profile  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resources not Found")
    else:
        db.delete(delete_profile)
        db.commit()
        redirect_url = "/profile_settings"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

#Profile Image Upload 
@app.get("/profile_image",response_class=HTMLResponse,tags=["Template"])
def upload_pimage(request: Request,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    return templates.TemplateResponse("upload_profile.html",{"request":request})

@app.post("/profile_image",response_class=HTMLResponse,tags=["Template"])
def upload_pimage(request: Request,user_id:int=Form(...),file:UploadFile = File(...),db:Session = Depends(get_db)):
    
    with open(f"static/profileimages/{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name = secure_filename(file.filename)
    mimetype = file.content_type

    image_upload = ProfileImage(img = file.file.read(),minetype=mimetype, name=name,user_id=user_id)
    db.add(image_upload)
    db.commit()
    redirect_url = "/profile"
    return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)


# Customized page
@app.get("/customurl/{id}",response_class=HTMLResponse,tags=["Template"])
def custom_url(request: Request,id:int,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    url = db.query(URL).filter(URL.id==id).first()
    return templates.TemplateResponse("custom.html",{"request":request,"url":url,"id":id})

@app.post("/customurl/{id}",response_class=HTMLResponse,tags=["Template"])
def custom_url(request: Request,id:int,custom_domain:str=Form(...),db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    errors = []
    # check if the custom URL is still available
    custom_exist = db.query(URL).filter(URL.custom_domain==custom_domain,URL.is_active).first()
    if custom_exist :
        errors.append(f"Your provided URL:{custom_domain} already exist, Please verify")
    
    # Retrieve the short URL details from db and create a customize URL
    url = db.query(URL).filter(URL.id == id,URL.is_active).first()
    base_url = "http://127.0.0.1:8000/"
    if url:
        url.custom_domain = custom_domain
        url.custom_url = str(base_url + custom_domain)
        db.commit()

        redirect_url = f"/customized_url/{id}"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

    else:
        errors.append(f"URL:{id} doesn't exist")
    return templates.TemplateResponse("custom.html",{"request":request})    

@app.get("/customized_url/{id}",response_class=HTMLResponse,tags=["Template"])
def custom_display(request: Request,id:int,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    urls = db.query(URL).all()
    return templates.TemplateResponse("custom.html",{"request":request,"id":id,"urls":urls})


# Customized Your short url page
@app.get("/customurl_page",response_class=HTMLResponse,tags=["Template"])
def custom_url(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    
    return templates.TemplateResponse("custom_page.html",{"request":request})

@app.post("/customurl_page",response_class=HTMLResponse,tags=["Template"])
def custom_url(request: Request,short_url:str=Form(...),custom_domain:str=Form(...),db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    errors = []
    # check if the custom URL is still available
    custom_exist = db.query(URL).filter(URL.custom_domain==custom_domain,URL.is_active).first()
    if custom_exist :
        errors.append(f"Your provided URL:{custom_domain} already exist, Please verify")
    
    # Retrieve the short URL details from db and create a customize URL
    url = db.query(URL).filter(URL.short_url == short_url,URL.is_active).first()
    url_key = url.url_key
    base_url = "http://127.0.0.1:8000/"
    if url:
        url.custom_domain = custom_domain
        url.custom_url = str(base_url + custom_domain)
        db.commit()

        redirect_url = f"/custom_page_url/{url_key}"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

    else:
        errors.append(f"URL:{short_url} doesn't exist")
    return templates.TemplateResponse("custom_page.html",{"request":request})    

@app.get("/custom_page_url/{url_key}",response_class=HTMLResponse,tags=["Template"])
def custom_page_display(request: Request,url_key:str,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    urls = db.query(URL).all()
    return templates.TemplateResponse("custom_page.html",{"request":request,"url_key":url_key,"urls":urls})

# Loading short URL
@app.get("/{url_key}",response_class=HTMLResponse,tags=["Template"])
def short_to_target(request: Request,url_key:str,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):

    # Get original  url using short url
    urls = db.query(URL).all()
    db_url = db.query(URL).filter(URL.url_key == url_key,URL.is_active).first()
    if db_url:
        # update the url click by increasing it by +1
        db_url.clicks += 1
        db.commit()
        redirect_url = db_url.original_url
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    # Loading Custom URL
    for url in urls:
        if url.custom_domain == url_key :
        # update the url click by increasing it by +1
            url.clicks += 1
            db.commit()
            redirect_url = url.original_url
            return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    else:
        not_found(f"URL KEY:{url_key} doesn't exist")
        

# Generating QR image
@app.get("/qrcode/url", response_class=HTMLResponse)
def QRCode(request: Request,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    return templates.TemplateResponse("qrcode.html", {"request": request,})


@app.post("/qrcode/url", response_class=HTMLResponse)
def QRCode(request: Request, url: str = Form(...),Authorize:AuthJWT=Depends()):
    code = pyqrcode.create(url)
    qr_data = code.png_as_base64_str(scale=5)
    return templates.TemplateResponse("qrcode.html", {"request": request, "url": url, "qr_data": qr_data})

# URL analysis
@app.get("/urls/analysis", response_class=HTMLResponse)
def analysis(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    current_user = Authorize.get_jwt_subject()
    urls = db.query(URL).order_by(URL.id.desc()).limit(20)
    total_urls = 0
    total_clicks = 0
    total_custom = 0
    db_urls = db.query(URL).all()
    for url in db_urls:
        if url:
            total_urls += 1
    for url in db_urls:
        if url.clicks:
            total_clicks += url.clicks
    for url in db_urls:
        if url.custom_url:
            total_custom += 1
    total_urls = total_urls
    total_clicks = total_clicks
    total_custom = total_custom
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "urls":urls,
        "total_urls":total_urls,
        "total_clicks":total_clicks,
        "total_custom":total_custom,
        "current_user":current_user
        })

# URL Dashboard
@app.get("/user/dashboard", response_class=HTMLResponse)
def url_dashboard(request: Request,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    profiles = db.query(Profile).all()
    urls = db.query(URL).all()
    total_urls = 0
    total_clicks = 0
    total_custom = 0
    db_urls = db.query(URL).all()
    for url in db_urls:
        if url.user_id == user.id :
            total_urls += 1
            total_clicks += url.clicks
    for url in db_urls:
        if url.user_id == user.id and url.custom_url:
            total_custom += 1
    total_urls = total_urls
    total_clicks = total_clicks
    total_custom = total_custom
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user":user,
        "profiles":profiles,
        "urls":urls,
        "total_urls":total_urls,
        "total_clicks":total_clicks,
        "total_custom":total_custom,
        "current_user":current_user
        })

# URL information
@app.get("/urls/info/{id}", response_class=HTMLResponse)
def info(request: Request,id:int,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    users = db.query(User).all()
    profiles = db.query(Profile).all()
    url = db.query(URL).filter(URL.id == id).first()
    names = db.query(Profile).all()
    return templates.TemplateResponse("url_info.html", {"request": request,"url":url,"users":users,"profile":profiles,"names":names})

# delete url
@app.get("/delete_url/{id}",response_class=HTMLResponse,tags=["Template"])
def url_delete(request: Request,id:int,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized, You need to authenticate your access token")
    delete_url = db.query(URL).filter(URL.id == id).first()
    if delete_url  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resources not Found")
    else:
        db.delete(delete_url)
        db.commit()
        redirect_url = "/user/dashboard"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

# log out route
@app.get("/logout")
def logout(Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies
    
    redirect_url = "/"
    return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",port=8000,reload= True)
