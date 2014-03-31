import web
import os
import time
import requests
import urllib
import urllib2
import json as simplejson
import dl_image as IMAGES

urls = (
    '/', 'IndexHandler',
    '/login', 'LoginHandler',
    '/filenames', 'FilenameHandler',
)

CLIENT_ID = "" # client ID goes here
CLIENT_SECRET = "" # client SECRET goes here

class IndexHandler:
    def GET(self):
        url = "https://api.instagram.com/oauth/authorize/?client_id="
        url += CLIENT_ID
        url += "&redirect_uri="
        url += "http://localhost:8080/login"
        url += "&response_type=code"

        web.redirect(url)

class LoginHandler:
    def GET(self):
        data = web.input(code=None)
        print data.code

        url = "https://api.instagram.com/oauth/access_token"

        data = {
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET,
            'grant_type':'authorization_code',
            'redirect_uri':'http://localhost:8080/login',
            'code':data.code
        }

        form_data = urllib.urlencode(data)

        r = requests.post(str(url), data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})

        print r.url
        print r.content

        response = simplejson.loads(r.content)
        image_lists = []
        ctr = 1
        token = response["access_token"]



        while True:
            try:
                if len(image_lists) == 0:
                    image_lists = IMAGES.get_txt()
                    ctr = len(image_lists)

                has = False
                image_url = "https://api.instagram.com/v1/tags/richard/media/recent?access_token=" + token
                insta_data = requests.get(image_url)
                json_datas = simplejson.loads(insta_data.content)

                for item in json_datas["data"]:
                    this_image_url = item["images"]["standard_resolution"]["url"]
                    owner = item["user"]["username"]

                    user_url = item["user"]["profile_picture"]

                    if this_image_url not in image_lists:
                        file_name = IMAGES.format_counter(ctr) + "_image_" + owner + ".jpg"
                        IMAGES.download_photo(this_image_url, file_name)

                        profile_filename = owner + ".jpg"
                        IMAGES.user_photo(user_url, profile_filename)

                        ctr += 1
                        print file_name

                        image_lists.append(this_image_url)
                        has = True

                if has:
                    IMAGES.create_txt(image_lists)


            except:
                new_data = requests.post(str(url), data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
                new_response = simplejson.loads(new_data.content)
                token = new_response["access_token"]

class FilenameHandler:
    def GET(self):
        callbacks = web.input(callback=None)
        print callbacks.callback

        path = os.getcwd() + "/images"
        data = os.listdir(path)

        filenames = {}
        filenames["images"] = []
        filenames["users"] = []

        data_length = len(data)

        print data_length
        print data.reverse()

        print len(data)

        counter = 1
        for item in data:
            if ".jpg" in item:
                if counter <= 120:
                    filenames["images"].append(item)

                counter += 1

        user_path = os.getcwd() + "/users"
        user_data = os.listdir(user_path)

        for item in user_data:
            if ".jpg" in item:
                filenames["users"].append(item)

        return str(callbacks.callback) + "(" + simplejson.dumps(filenames) + ");"



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()