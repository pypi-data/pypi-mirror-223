
# to override print <= can be a big problem with exceptions
#from __future__ import print_function # must be 1st
#import builtins
'''
This is flask interface
'''
from flashcam.version import __version__
from fire import Fire
import sys
from flashcam import config

config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"
if not config.load_config():
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")
    sys.exit(1)
print("---------------------------------------- LOADED IN WEBPY")
print(config.CONFIG)
print(config.CONFIG["Histogram"], "==histo in web")
# print("------------JUST LOADED---------------")





from importlib import import_module
import os
import sys  #exit
from flask import Flask, render_template, render_template_string, Response, url_for
from flask import request
from flask import jsonify

import getpass


import datetime as dt
import time

from flask import request
#===== another auth.
from flask_httpauth import HTTPBasicAuth

# import pantilthat

# block stuff depending on PC
import socket

import random

import cv2
import numpy as np

from flashcam.real_camera import Camera
from flashcam import real_camera # for is_int()

#----------------------------------------------
from flashcam.mmapwr import mmwrite

try:
    import pantilthat
except:
    class pantilthat:
        @classmethod
        def tilt(self,a):
            return
        @classmethod
        def pan(self,a):
            return
        @classmethod
        def get_tilt(self):
            return 0
        @classmethod
        def get_pan(self):
            return 0



app = Flask(__name__)




#==================== ALL config changes must be here ============
#
#  1st   'filename'     2nd load config       !!!!!!!!!!!!!!!!!
#
#config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"
#config.load_config()

#
config.CONFIG['camera_on'] = False # for everyone -
#               nobodyhas the camera at this point
#               ?? it is used in real_camera.py ...
#
if  not("debug" in config.CONFIG):
    config.CONFIG['debug'] = True



#config.show_config()
# CONFIG WILL BE SAVED WHEN RUN FROM MAIN

# Camera = Camera #  This was a lucky error.... CLass from Class
# it appears - flask works when I run directly the class .....


cross_dx, cross_dy = 0,0
cross_on = False
zoom2_on = 1

save_fg = False
mix_fg = False
save_bg = False
sub_bg = False

frame_fg = None
frame_fg2 = None
frame_bg = None
frame_bg2 = None
frame_mask = None
frame_mask_inv = None

# background path
BGFILE = os.path.expanduser('~/.config/flashcam/background.jpg')
FGFILE = os.path.expanduser('~/.config/flashcam/foreground.jpg')




def logthis( ttt="Started" ):
    sss=dt.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S")+" "+ttt+"\n"
    print(sss , end="")
    with open( os.path.expanduser("~/flashcam.log") ,"a+") as f:
        f.write( sss )


logthis() #-------- keep track about logins ---------
remote_ip=""
auth = HTTPBasicAuth()

#---not fstring- {} would colide

index_page = """
 <!--meta http-equiv="refresh" content="5";-->

<html>
<script>
function doDate()
{
    var str = "";

    var days = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
    var months = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

    var now = new Date();

    str += " &nbsp; &nbsp;&nbsp;&nbsp;" +  now.getHours() +":" + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes() + ":" + (now.getSeconds() < 10 ? '0' : '') + now.getSeconds() ;
    document.getElementById("todaysDate").innerHTML = str;
}

setInterval(doDate, 200);
</script>
  <head>
    <title>Video Streaming</title>
  </head>
  <body>


<div id="todaysDate"></div>

    <img src="{{url}}">
<br>
<form method="post" action="/cross">
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="up2" value="UP2">up2</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="up" value="UP">up</button>
      <button style="width:10%" name="crosson" value="CROSSON">crossON</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:3%" name="left2" value="LEFT2"> << </button>
      <button style="width:3%" name="left" value="LEFT"> < </button>
      <button style="width:3%" name="center" value="CENTER"> o </button>
      <button style="width:3%" name="right" value="RIGHT"> > </button>
      <button style="width:3%" name="right2" value="RIGHT2"> >> </button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="down" value="DOWN">down</button>
      <button style="width:10%" name="crossoff" value="CROSSOFF">crossOFF</button>
  </div>
  <div class="btn-group" style="width:100%">
      <button style="width:20%" name="down2" value="DOWN2">down2</button>
<button style="width:10%" name="zoom2" value="ZOOM2">ZOOM2</button> </div>
<hr>

<table>
<tr>
<td>
   <button style="width:100%" name="savebg" value="SAVEBG">saveBG</button>
    <button style="width:100%" name="savefg" value="SAVEFG">saveFG</button>
</td>
 <td align="left" rowspan="2">
    <img src="{{url_bg}}" alt="Smiley face"  height="120" width="160" />
 </td>
 <td align="left" rowspan="2">
    <img src="{{url_fg}}" alt="Smiley face"  height="120" width="160" />
 </td>


 <td>
   <button style="width:100%" name="timelaps" value="TIMELAPS">LAPS</button> <input type = "text" name = "timelaps_input" size="5"  placeholder="0" />
 </td>
</tr>





<tr>
 <td>
    <button style="width:100%" name="subbg" value="SUBBG">subBG</button>
    <button style="width:100%" name="mixfg" value="MIXFG">mixFG</button>
 </td>
 <td> </td>
 <td>
   <button style="width:100%" name="rot0" value="ROT0">rot0</button>
   <button style="width:100%" name="rot180" value="ROT180">rot180</button>
 </td>
 <td>
   <button style="width:100%" name="live" value="LIVE">live</button>
   <button style="width:100%" name="fixed" value="FIXED">fixed</button>
 </td>
</tr>
</table>





<hr>
      <button style="width:3%" name="speedx" value="SPEEDX">dX</button>
    <input type = "text" name = "inputx"  size="5" />
      <button style="width:3%" name="speedy" value="SPEEDY">dY</button>
    <input type = "text" name = "inputy" size="5" />

      <button style="width:6%" name="restart_translate" value="RESTART_TRANSLATE">restart</button>
      <button style="width:4%" name="zero_translatex" value="ZERO_TRANSLATEX">zeroX</button>
      <button style="width:4%" name="zero_translatex" value="ZERO_TRANSLATEX">zeroY</button>
      <button style="width:5%" name="accum" value="ACCUM">Accum</button>
      &nbsp; &nbsp;&nbsp; <input type = "text" name = "accumtxt" size="6" />
<hr>
      <button style="width:6%" name="gamma2" value="GAMMA2">gm x2</button>
      <button style="width:6%" name="gamma05" value="GAMMA05">gm /2</button>
      <button style="width:6%" name="gamma" value="GAMMA">gm def</button>
      <button style="width:6%" name="gain2" value="GAIN2">ga x2</button>
      <button style="width:6%" name="gain05" value="GAIN05">ga /2</button>
      <button style="width:6%" name="gain" value="GAIN">ga def</button>
      <button style="width:6%" name="expo05" value="EXPO05">ex /2</button>
      <button style="width:6%" name="expo2" value="EXPO2">ex x2</button>
      <button style="width:6%" name="expo" value="EXPO">ex def</button>

  </div>

</form>


  </body>
</html>

"""
#    <img src="{{ url_for('video') }}">

def crossonw( img,  dix, diy):
    RADIUS=63
    y = int(img.shape[0]/2)
    x = int(img.shape[1]/2)

    ix = x+dix
    iy = y+diy

    i2=cv2.circle( img, (ix,iy), RADIUS, (0,255,55), 1)
    i2=cv2.line(i2, (ix-RADIUS+5,iy), (ix-5,iy), (0, 255, 55), thickness=1, lineType=8)
    i2=cv2.line(i2, (ix+RADIUS-5,iy), (ix+5,iy), (0, 255, 55), thickness=1, lineType=8)

    i2=cv2.line(i2, (ix,iy-RADIUS+5), (ix,iy-5), (0, 255, 55), thickness=1, lineType=8)
    i2=cv2.line(i2, (ix,iy+RADIUS-5), (ix,iy+5), (0, 255, 55), thickness=1, lineType=8)

    i2=cv2.line(i2, (ix,iy), (ix,iy), (0, 255, 55), thickness=1, lineType=8)
    return img



# ... this i dont remember
# --- probably a wrong guess ... @auth.verify_password
#
# i need  @auth.login_required
@auth.verify_password
@app.route("/cross", methods=['GET', 'POST'])
# @auth.login_required
def cross():
    global cross_dx, cross_dy, cross_on, save_bg, save_fg, mix_fg, sub_bg, zoom2_on
    global remote_ip
    # i will read it from file
    print("i... request (authenticated) on cross came...\n ...",request.form)

    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis(f"  {remote_ip}/{request.remote_addr}  {request.form}")
    crocfg = os.path.expanduser("~/.config/flashcam/cross.txt")
    if os.path.exists(crocfg):
        with open(crocfg) as f:
           cross_dx, cross_dy  = [int(x) for x in next(f).split()]

    print(request.method)
    if request.method == 'POST':

        # ------------------------------------------- EXECUTE EXECUTION part for real_camera
        if request.form.get('savebg') == 'SAVEBG':
            print("i... saving BG" )
            save_bg = True
            mmwrite(f"save_background {save_bg}" )

        if request.form.get('savefg') == 'SAVEFG':
            print("i... saving FG" )
            print("i... saving FG" )
            print("i... saving FG" )
            print("i... saving FG" )
            print("i... saving FG" )
            print("i... saving FG" )
            save_fg = True
            mmwrite(f"save_foreground {save_fg}" )

        if request.form.get('subbg') == 'SUBBG':
            print("i... substracting  BG" )
            sub_bg = not( sub_bg)
            mmwrite(f"substract_background {sub_bg}" )

        if request.form.get('mixfg') == 'MIXFG':
            print("i... mixing FG" )
            mix_fg = not( mix_fg)
            mmwrite(f"mix_foreground {mix_fg}" )


        if request.form.get('accum') == 'ACCUM':
            accum = request.form.get('accumtxt')
            try:
                accum = int(accum)
            except:
                accum = 0
            print("i...  ACCUM",  accum)
            mmwrite(f"average {accum}" )

        if request.form.get('speedx') == 'SPEEDX':
            speedx = request.form.get('inputx')
            try:
                speedx = float(speedx)
                print("i...  X",  speedx)
                mmwrite(f"speedx {speedx}" )
            except:
                print("D... unknown value speedx")

        if request.form.get('speedy') == 'SPEEDY':
            #time.sleep(0.2)  #=============== PROBLEM FOR SLOW FRAMES!
            speedy = request.form.get('inputy')
            try:
                speedy = float(speedy)
                print("i...  Y",  speedy)
                mmwrite(f"speedy {speedy}" )
            except:
                print("D... unknown value speedy")

        if request.form.get('restart_translate') == 'RESTART_TRANSLATE':
            mmwrite(f"restart_translate True" )

        if request.form.get('zero_translatex') == 'ZERO_TRANSLATEX':
            mmwrite(f"speedx {0}" )
        if request.form.get('zero_translatey') == 'ZERO_TRANSLATEY':
            mmwrite(f"speedy {0}" )

        if request.form.get('gamma2') == 'GAMMA2':
            mmwrite(f"gamma_multiply True" )
        if request.form.get('gamma05') == 'GAMMA05':
            mmwrite(f"gamma_divide True" )
        if request.form.get('gamma') == 'GAMMA':
            mmwrite(f"gamma_setdef True" )

        if request.form.get('gain2') == 'GAIN2':
            mmwrite(f"gain_multiply True" )
        if request.form.get('gain05') == 'GAIN05':
            mmwrite(f"gain_divide True" )
        if request.form.get('gain') == 'GAIN':
            mmwrite(f"gain_setdef True" )

        if request.form.get('expo2') == 'EXPO2':
            mmwrite(f"expo_multiply True" )
        if request.form.get('expo05') == 'EXPO05':
            mmwrite(f"expo_divide True" )
        if request.form.get('expo') == 'EXPO':
            mmwrite(f"expo_setdef True" )

        # FOR THE MOEMNT - HIDDEN CAPABILITY
        if request.form.get('exposet') == 'EXPOSET':
            expovalue = request.form.get('expovalue')
            mmwrite(f"expovalue {expovalue}" )
        # FOR THE MOEMNT - HIDDEN CAPABILITY
        if request.form.get('gainset') == 'GAINSET':
            gainvalue = request.form.get('gainvalue')
            mmwrite(f"gainvalue {gainvalue}" )


        if request.form.get('timelaps') == 'TIMELAPS':
            timelaps = request.form.get('timelaps_input')
            try:
                speedy = int(timelaps)
                print("i...  Y",  timelaps)
                mmwrite(f"timelaps {timelaps}" )
            except:
                print("D... unknown value timelaps")

        if request.form.get('rot0') == 'ROT0':
            mmwrite(f"rotate180 0" )
        if request.form.get('rot180') == 'ROT180':
            mmwrite(f"rotate180 180" )

        if request.form.get('live') == 'LIVE':
            mmwrite(f"fixed_image None" )
        if request.form.get('fixed') == 'FIXED':
            mmwrite(f'fixed_image "BEAM_ON_.jpg"' )
        # added 2302 - directly image display possible via curl
        elif  request.form.get('fixed') is not None and \
              request.form.get('fixed').find(".jpg")>1:
            diimg = request.form.get('fixed')
            mmwrite(f'fixed_image "{diimg}"' )


        if request.form.get('overtext') is not None:
            digits = request.form.get('overtext')
            mmwrite(f"overtext {digits}" )



        if request.form.get('framekind') == "HISTOGRAM":
            mmwrite(f"framekind histo" )
        if request.form.get('framekind') == "DIRECT":
            mmwrite(f"framekind direct" )
        if request.form.get('framekind') == "DETECT":
            mmwrite(f"framekind detect" )




        # ---------------------------------------------- Cross controls
        if cross_on:
            if request.form.get('left2') == 'LEFT2':
                print("left2")
                cross_dx-= 50
            if request.form.get('left') == 'LEFT':
                print("left")
                cross_dx-= 5
            if request.form.get('center') == 'CENTER':
                print("center")
                cross_dx= 0
                cross_dy= 0
            elif  request.form.get('right') == 'RIGHT':
                print("right")
                cross_dx+= 5
            elif  request.form.get('right2') == 'RIGHT2':
                print("right2")
                cross_dx+= 50
            elif  request.form.get('up') == 'UP':
                print("up")
                cross_dy-= 5
            elif  request.form.get('up2') == 'UP2':
                print("up2")
                cross_dy-= 50
            elif  request.form.get('down') == 'DOWN':
                print("down")
                cross_dy+= 5
            elif  request.form.get('down2') == 'DOWN2':
                print("down2")
                cross_dy+= 50
        else: # ---------------------------- PANTILT MODE
            # sudo apt install python3-smbus
            if request.form.get('down') == 'DOWN':
                print("PAN v")
                if (pantilthat.get_tilt()-2)>=-90:
                    pantilthat.tilt( pantilthat.get_tilt()-2  )
            if request.form.get('up') == 'UP':
                print("PAN ^")
                if (pantilthat.get_tilt()+2)<=90:
                    pantilthat.tilt( pantilthat.get_tilt()+2 )
            if request.form.get('right') == 'RIGHT':
                print("PAN ->")
                if (pantilthat.get_pan()-2)>=-90:
                    pantilthat.pan( pantilthat.get_pan()-2 )
            if request.form.get('left') == 'LEFT':
                print("PAN <-")
                if (pantilthat.get_pan()+2)<=90:
                    pantilthat.pan( pantilthat.get_pan()+2 )

            if request.form.get('down2') == 'DOWN2':
                print("PAN v")
                if (pantilthat.get_tilt()-8)>=-90:
                    pantilthat.tilt( pantilthat.get_tilt()-8  )
            if request.form.get('up2') == 'UP2':
                print("PAN ^")
                if (pantilthat.get_tilt()+8)<=90:
                    pantilthat.tilt( pantilthat.get_tilt()+8 )
            if request.form.get('right2') == 'RIGHT2':
                print("PAN ->")
                if (pantilthat.get_pan()-8)>=-90:
                    pantilthat.pan( pantilthat.get_pan()-8 )
            if request.form.get('left2') == 'LEFT2':
                print("PAN <-")
                if (pantilthat.get_pan()+8)<=90:
                    pantilthat.pan( pantilthat.get_pan()+8 )

        if  request.form.get('external_signal') is not None:
            excommand = str( request.form.get('external_signal') )
            #print(f"**** external signal == {excommand} *****")
            #print(f"**** external signal == {excommand} *****")
            #print(f"**** external signal == {excommand} *****")
            print(f"**** external signal == {excommand} *****")
            if excommand == "pausedmON":
                print("i... unpause   - Detect Motion         unpause   - Detect Motion ")
                mmwrite(f"pausedMOTION False" )
            if excommand == "pausedmOF":
                print("i... pause - NO Detect Motion              pause - NO Detect Motion")
                mmwrite(f"pausedMOTION True" )


        if  request.form.get('crosson') == 'CROSSON':
            print("green cross ON")
            cross_on = True
        elif  request.form.get('crossoff') == 'CROSSOFF':
            print("green cross OFF")
            cross_on = False

        if  request.form.get('zoom2') == 'ZOOM2':
            if zoom2_on==1:
                print("ZOOM2 ->2")
                zoom2_on = 2
                mmwrite(f"zoom 2" )
            elif zoom2_on==2:
                print("ZOOM2 ->4")
                zoom2_on = 4
                mmwrite(f"zoom 4" )
            elif zoom2_on==4:
                print("ZOOM2 ->6")
                zoom2_on = 8
                mmwrite(f"zoom 8" )
            else :
                print("ZOOM2 ->1")
                zoom2_on = 1
                mmwrite(f"zoom 1" )

        #---------------- I am blindly adding functionality ... compression now
        if  request.form.get('kompress') == 'KOMPRESS':
            kompressvalue = request.form.get('kompressvalue')
            if real_camera.is_int(kompressvalue):
                kompressvalue = int(kompressvalue)
            else:
                kompressvalue = 85
            print("kompress asked  ....... with value=", kompressvalue)
            config.CONFIG['kompress'] = kompressvalue
            # if config.CONFIG['kompress']>90:
            #     config.CONFIG['kompress'] = 9
            #     print("i... KOMPRESS", config.CONFIG['kompress'] )
            # else:
            #     config.CONFIG['kompress'] = 99
            #     print("i... KOMPRESS", config.CONFIG['kompress'] )
            #     #mmwrite(f"zoom 2" ) # not here...

        #---------------- TELEGRAM TEST
        if  request.form.get('telegram') == 'TELEGRAM':
            print("i...  telegram asked  ....... ")
            mmwrite(f"telegram TELEGRAM" )


        # .... save cross x and y inside a file at ~/.config/flashcam/
        with open(crocfg,"w") as f:
            f.write(f"{cross_dx} {cross_dy}")

    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " / remote      = "+request.remote_addr )
    logthis( " / remote xreal= "+remote_ip )
    url = url_for('video')
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    #time.sleep(0.5)
    return render_template_string(index_page, url=url, url_bg  = url_bg, url_fg  = url_fg)







@auth.verify_password
def verify_password(username, password):
    global remote_ip
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#    user = User.query.filter_by(username = username).first()
#    if not user or not user.verify_password(password):
#        return False
#    g.user = user
    # config.load_config() # IMPLIES THAT ALL changes in 'bin flask500' are lost
    # config.show_config()
    u = config.CONFIG["user"]
    p = config.CONFIG["password"]
    #u=getpass.getuser()
    #p=u+u
    # try:
    #     with open( os.path.expanduser("~/.pycamfw_pass") ) as f:
    #         print("YES---> FILE  ","~/.pycamfw_pass")
    #         p=f.readlines()[0].strip()
    # except:
    #     print("NO FILE  ","~/.pycamfw_pass")

    if (username==u) and (password==p):
        # logthis( "   TRUE  checking userpass (client)"+username+"/"+password+"/")
        logthis( f" TRUE  PASS {request.remote_addr:15s} {remote_ip:15s}: /{u}/{p}/")
        return True
    else:
        logthis( f" FALSE PASS {request.remote_addr:15s} {remote_ip:15s}: /{username}/{password}/")
        return False




@app.route('/')
@auth.login_required
def index():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " / remote      = "+request.remote_addr )
    logthis( " / remote xreal= "+remote_ip )
    url = url_for('video')
    print(url)
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    return render_template_string(index_page, url=url, url_bg  = url_bg, url_fg  = url_fg)

@app.route('/refresh30')
@auth.login_required
def index30():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " / remote      = "+request.remote_addr )
    logthis( " / remote xreal= "+remote_ip )
    url = url_for('video')
    print(url)
    url_bg = url_for('background')
    url_fg = url_for('foreground')
    return render_template_string(index_page_refresh30, url=url, url_bg  = url_bg, url_fg  = url_fg)


#('index.html')
@app.route('/foreground.jpg')
@auth.login_required
def foregroundjpg():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( FGFILE):
        blank = cv2.imread( FGFILE )
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD FOREGROUND IMAGE FOUND",r, frame_fg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO FOREGROUND - black image",r)

    # send direct JPG
    # return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # <img>
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/foreground')
@auth.login_required
def foreground():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( FGFILE):
        blank = cv2.imread( FGFILE )
        # print( blank )
        # # frame_bg = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        frame_fg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD FOREGROUND IMAGE FOUND",r, frame_fg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_fg = blank.copy() # propagate to the system
        #frame = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO FOREGROUND - black image",r)

    # send direct JPG
    return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/background.jpg')
@auth.login_required
def backgroundjpg():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    if os.path.exists( BGFILE):
        blank = cv2.imread( BGFILE )
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD BACKGROUND IMAGE FOUND",r, frame_bg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO BACKGROUND - black image",r)

    # send direct JPG
    #return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    # jpg direct?
    return Response( jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
    # with <img>
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background')
@auth.login_required
def background():
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE


    #if not(frame_bg is None):
    #    # print(frame_bg, "BGFRAME")
    #    # # frame = cv2.imdecode(frame_bg, cv2.IMREAD_COLOR)
    #    r, jpg = cv2.imencode('.jpg', frame_bg)
    #    # print("RESPONSE BACKGROUND",r)
    #else:
    if os.path.exists( BGFILE):
        blank = cv2.imread( BGFILE )
        # print( blank )
        # # frame_bg = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        frame_bg = blank.copy() # propagate to the system
        r, jpg = cv2.imencode('.jpg', blank)
        print("OLD BACKGROUND IMAGE FOUND",r, frame_bg.shape)
    else:
        blank = np.zeros((480,640,3), np.uint8)
        frame_bg = blank.copy() # propagate to the system
        #frame = cv2.imdecode(blank, cv2.IMREAD_COLOR)
        r, jpg = cv2.imencode('.jpg', blank)
        print("NO BACKGROUND - black image",r)

    # create mask----------------- appears not usefull-----
    # frame_mask = np.random.randint(2,
    #                                size = (frame_bg.shape[0],frame_bg.shape[1] ),
    #                                dtype=np.uint8) #
    # frame_mask = 255 *np.ones( (frame_bg.shape[0],frame_bg.shape[1] ),
    #                                dtype=np.uint8) #
    # frame_mask[:230,:] = 0
    # frame_mask[-20:-1,:] = 0
    # frame_mask_inv = 255 - frame_mask
    # r, jpg = cv2.imencode('.jpg', frame_mask)

    # send direct JPG
    return Response( jpg.tobytes() , direct_passthrough= True)
    # rather than <img />
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')





#==================== IN FACT == THIS IS THE START OF THE CAMERA =====
# with asking Camera()    I create an "instance" (static!) of the class
# and call init_cam
#
@app.route('/video')
@auth.login_required
def video():
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print("W... asking VIDEO",request.remote_addr, remote_ip)
    logthis( " /video remote      = "+request.remote_addr )
    logthis( " /video remote xreal= "+remote_ip )
    # i return JPG TO AXIS CAMERA....
    #---------------this is MJPEG-------------------------
    #config.CONFIG["product"] = "Webcam C270"
    # return Response(gen(Camera(config.CONFIG["product"], "640x480"),remote_ip),
    # --- i send here the CLASS ?????
    return Response(gen(Camera(),remote_ip),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



#========================================= CAMERA GEN ===
#========================================= CAMERA GEN ===
#========================================= CAMERA GEN === RESPONSE
#========================================= CAMERA GEN ===
#========================================= CAMERA GEN ===


def gen(camera, remote_ip, blend=False, bigtext=True):
    """ returns jpeg;
    MAY do modifications per USER ! BUT any fraME MOD => IS SENT TO ALL!
    can send only some frames
    """
    global  save_bg, frame_bg, frame_bg2, save_fg, frame_fg, frame_fg2, frame_mask, frame_mask_inv #, BGFILE

    print("D... entered gen, camera = ", camera)
    framecnt = 0
    framecnttrue = 0
    ss_time = 0



    while True:
        time.sleep(0.1)
        framecnt+=1
        #print("D... get_frame (gen)")
        frame = camera.get_frame()
        #print("i... got_frame (gen)", frame.shape )
        start = dt.datetime.now()
        blackframe = np.zeros((480,640,3), np.uint8)
        #frame = blackframe
        if blend:
            frame = 0.5*frame + 0.5*imgs[ random.randint(0,len(imgs)-1) ]

        if cross_on:
            if zoom2_on==1:
                frame = crossonw( frame, cross_dx, cross_dy )
            else:
                frame = crossonw( frame, 0,0  )



        if not(frame is None):  # 95 is default quality
#            frame=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tobytes()
            COMPR = config.CONFIG['kompress']
            # 480,640 --- print(frame.shape)
            frame=cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, COMPR])[1].tobytes()
        else:
            continue


        stop = dt.datetime.now()
        ss_time = (stop-start).total_seconds()

        #===== MAYBE THIS IS WASTING - it should throw get_frame
        #  but with -k sync   it restarts

        timetag = stop.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        TTAG = f"{framecnt:07d}#{timetag}#"
        # print(TTAG)
        # yield ( frame)  #--------- JPEG vs MJPEG
        yield (b'--frame\r\n' # ---- JPEG
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n' + b'#FRAME_ACQUISITION_TIME#' + TTAG.encode("utf8") )



if __name__ == '__main__':

    print("i... APP RUN FROM WEB.PY")
    app.run(host='0.0.0.0', port=config.CONFIG['port'], threaded=True)
