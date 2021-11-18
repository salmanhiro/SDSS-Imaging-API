import urllib.request
import os

coord = input("RA and dec in decimal [RA],[DE] : ").split(",")
scale = float(input("Enter the image scale (float, default 1): ") or "1")
dim = int(input("Enter the image dimension (int, default 200 px): ") or "200")

ra, dec = coord
LOC = "images"
os.makedirs(LOC, exist_ok=True)


def getter(right_ascension, declination, image_scale=1, dimension=200):
    url = f"http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={str(right_ascension)}&dec={str(declination)}&scale={str(image_scale)}&width={str(dimension)}&height={str(dimension)}"
    save_as = LOC+"/img_RAJ_" + \
        str(right_ascension)+"_DEJ_"+str(declination)+".jpg"
    urllib.request.urlretrieve(url, save_as)
    print(save_as, " downloaded")


getter(ra, dec, scale, dim)
