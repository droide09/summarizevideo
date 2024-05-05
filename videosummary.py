import os
from pytube import YouTube
from transformers import pipeline
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment

def download_youtube_video(url,ffilename):
    print("scarico il video");
    yt = YouTube(url)
    stream = yt.streams.filter(res='360p',progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(output_path='.', filename=ffilename)
    print("Video scaricato con successo!")
    
def extract_text_from_video(video_path,min_plength,max_plength,planguage): 
  clip = mp.VideoFileClip(video_path)
  audio = clip.audio
  audio_path = "temp_audio.wav"
  audio.write_audiofile(audio_path)
  recognizer = sr.Recognizer()

  audio = AudioSegment.from_file("temp_audio.wav")
  chunks = []
  for i in range(0, len(audio), 120000):  # 60 seconds chunks
    chunk = audio[i:i+120000]
    chunks.append(chunk)
    print("X")

  alltext = "";

  for chunk in chunks:
      with sr.AudioFile(chunk.export("temp.wav", format="wav")) as source:
          audio = recognizer.record(source)
      try:
          text = recognizer.recognize_google(audio, language=planguage)
          print(".", text)
          alltext = alltext + " "+text
      except sr.UnknownValueError:
          print("Unable to recognize speech")
      except sr.RequestError as e:
          print("Error:", e)
  
  print(f"Extracted Text: {alltext}")
    
  summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
  summary = summarizer(alltext, max_length=max_plength, min_length=min_plength)
  print ("riassunto:\n\n")
  print(summary)

  os.remove(audio_path)    

if __name__ == "__main__":
    import sys
    print (len(sys.argv))
    print (sys.argv[1])
    print (sys.argv[2])
    print (sys.argv[3])
    if len(sys.argv) != 5:
        print("Usage: python videosummary.py  <url> minwords maxwords language")
        print("Exampke: python videosummary.py  https://www.youtube.com/watch?v=co5g1noQn08 1500 2000 it-IT")
        sys.exit(1)
    
    url = sys.argv[1]
    ffilename = "video.mp4"
    download_youtube_video(url,ffilename)

    print (ffilename)
    extract_text_from_video(ffilename,int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
    os.remove(ffilename) 
    