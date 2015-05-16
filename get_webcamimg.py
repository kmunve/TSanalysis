__author__ = 'kmu'
"""
TODO:

- check if last downloaded file is the same as the new one.
- if not add a new file else disregard

- make a db with webcam names and links to go through each run

Use imagemagick to make an animated gif than can be put on a website:
convert -set delay 3 -loop 0 -scale 50% *.jpg animation.gif
"""

import requests
import datetime
import os


def download_img(img_url, img_file="download.png"):
    f = open(img_file, 'wb')
    f.write(requests.get(img_url).content)
    f.close()

def get_webcam_img(webcam_name, webcam_url):

    _ct = datetime.datetime.now() # get current date and time
    _ct_str = _ct.strftime("%Y%m%dT%H%M")

    _main_path = os.path.dirname(os.path.realpath(__file__))
    _img_dir = r"webcamimg"
    _filename = "{0}{1}.jpg".format(webcam_name, _ct_str)
    img_path = os.path.join(_main_path, _img_dir, _filename)

    download_img(webcam_url, img_path)


if __name__ == "__main__":
    cam_dict = {"beiarfjellet": "http://webkamera.vegvesen.no/kamera?id=199416",
                "spiterstulen": "http://www.spiterstulen.no/kamera/video.jpg",
                "bjoberg": "http://bisp.no/_small_img.php"}

    for cam, url in cam_dict.iteritems():
        get_webcam_img(cam, url)



