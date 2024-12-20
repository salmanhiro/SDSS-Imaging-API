import streamlit as st
import urllib.request
import os
from astropy.coordinates import SkyCoord
from astropy import units as u
import random
import sqlite3
import requests
import csv
import tempfile

# Define the folder to save images
LOC = "images"
os.makedirs(LOC, exist_ok=True)

def getter(right_ascension, declination, image_scale=1, dimension=200):
    url = f"http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={str(right_ascension)}&dec={str(declination)}&scale={str(image_scale)}&width={str(dimension)}&height={str(dimension)}"
    save_as = os.path.join(LOC, f"img_RA_{right_ascension}_DE_{declination}.jpg")
    urllib.request.urlretrieve(url, save_as)
    return save_as

def resolve_object_name(object_name):
    try:
        coord = SkyCoord.from_name(object_name)
        return coord.ra.deg, coord.dec.deg
    except Exception as e:
        raise ValueError(f"Could not resolve object name: {e}")

def is_in_sdss_footprint(ra, dec):
    # Approximation: check if coordinates fall within SDSS DR16 footprint bounds
    # Actual implementation may require querying the SDSS database.
    return 0 <= ra <= 360 and -10 <= dec <= 70

def download_ngc_database():
    url = "https://raw.githubusercontent.com/mattiaverga/OpenNGC/refs/heads/master/database_files/NGC.csv"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to download NGC database.")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    with open(temp_file.name, "wb") as f:
        f.write(response.content)

    return temp_file.name

def get_random_object_and_download(scale=1, dim=200):
    # Download the NGC database
    ngc_file = download_ngc_database()

    with open(ngc_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        galaxies = [row for row in reader if row["RA"] and row["Dec"]]
        print(f"Found {len(galaxies)} galaxies in the NGC database.")

    if not galaxies:
        raise ValueError("No galaxies found in the NGC database.")

    while True:
        galaxy = random.choice(galaxies)
        name = galaxy["Name"]
        ra, dec = resolve_object_name(name)
        
        if is_in_sdss_footprint(ra, dec):
            try:
                filepath = getter(ra, dec, scale, dim)
                return name, ra, dec, filepath
            except Exception as e:
                print(f"Failed to download image for {name}: {e}")

# Streamlit UI
def main():
    st.title("SDSS Image Downloader")

    # Input fields
    option = st.selectbox("Select Input Mode:", ["RA and Dec", "Object Name", "Random Object"])

    if option == "RA and Dec":
        coord = st.text_input("Enter RA and Dec in decimal format (RA,Dec):", "")
    elif option == "Object Name":
        object_name = st.text_input("Enter the object name:", "")
    elif option == "Random Object":
        try:
            st.write("Getting random object and downloading image...")
            galaxy_name, ra, dec, filepath = get_random_object_and_download()
            st.success(f"Selected Random Object: {galaxy_name} (RA: {ra}, Dec: {dec})")
            st.image(filepath, caption=f"RA: {ra}, Dec: {dec}", use_column_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

    scale = st.number_input("Enter the image scale (default 1):", min_value=0.1, value=1.0, step=0.1)
    dim = st.number_input("Enter the image dimension in pixels (default 200):", min_value=50, value=200, step=10)

    if st.button("Download Image"):
        try:
            if option == "RA and Dec":
                ra, dec = map(float, coord.split(","))
                filepath = getter(ra, dec, scale, dim)
            elif option == "Object Name":
                ra, dec = resolve_object_name(object_name)
                filepath = getter(ra, dec, scale, dim)

            st.success(f"Image downloaded successfully: {filepath}")
            st.image(filepath, caption=f"RA: {ra}, Dec: {dec}", use_column_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
