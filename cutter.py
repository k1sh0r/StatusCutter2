from flask import *
from moviepy.editor import *
from datetime import datetime
import os, webbrowser

webbrowser.open('http://localhost:5000/')

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.htm')

@app.route('/uploaded',methods = ['POST', 'GET'])
def upload():
   if request.method == 'POST':
      result = request.form
      fileitem = request.files['filename']
      print("worked until here")
      #print(type(fileitem))
      #print(str(fileitem.filename))
      if fileitem.filename:
         fn = os.path.basename(fileitem.filename)
         open('uploads/' + fn, 'wb').write(fileitem.file.read())
         print('The file "' + fn + '" was copied inside uploads folder')
      else:
         print('not copied')

      return render_template('uploaded.html', fn = fn)
   
@app.route('/process',methods = ['POST','GET'])
def process():
      if request.method == 'POST':
         fn = request.form.get('fn')
         datentime = datetime.now()
         clipname = datentime.strftime("%d%m%H%M%S%f")
         print('fn'+ fn + 'recieved')
         #print(fn)
         fn = str("uploads/"+fn)
         clip = VideoFileClip(fn)
         cuts = clip.duration/15
         cuts = int(cuts)
         #print(cuts)
         subclips = []
         def st(value):
             x=value*15
             return x
         def et(value):
             x=value+1
             x=x*15
             return x
         for i in range(0,cuts):
             subclips.append(clip.subclip(st(i),et(i)))
             subclips[i].write_videofile("downloads/" + clipname + str(i+1) + '.mp4')
             #print(subclips[i].duration)

         subclips.append(clip.subclip(st(cuts),clip.duration))
         #print(subclips[cuts].duration)
         subclips[cuts].write_videofile("downloads/" + clipname + str(cuts+1) + '.mp4')

      return render_template('download.html', cuts = cuts, clipname = clipname)

if __name__ == '__main__':
   app.run()
