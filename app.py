import cv2
import numpy as np
import urllib.request

# input coordinate
# ongoing in dd mm ss
COORD = input('RA and dec in decimal [RA] [DE] : ').split(' ')
SCALE = float(input("Enter the image scale (float, default 1): ") or "1")
DIM = int(input("Enter the image dimension (int, default 200 px): ") or "200")
RA, DEC = COORD

loc = ""
def getter(RA, DEC, SCALE = 1, DIM = 200):
# Download the file from `url` and save it locally under `file_name`:
#url = "http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra="+str(RAJ2000[i])+"&dec="+str(DEJ2000[i])+"&scale=0.2&width=400&height=400"
    url = f"http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={str(RA)}&dec={str(DEC)}&scale={str(SCALE)}&width={str(DIM)}&height={str(DIM)}"
    save_as = loc+"img_RAJ_"+str(RA)+"_DEJ_"+str(DEC)+".jpg"
    urllib.request.urlretrieve(url ,save_as)
    print(save_as, " downloaded")

getter(RA, DEC, SCALE, DIM)

