import os
import urllib
import urllib2

DOWNLOADED_IMAGE_PATH = "/images"

def download_photo(img_url, filename):
    try:
        image_on_web = urllib.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()

            path = os.getcwd() + DOWNLOADED_IMAGE_PATH
            file_path = "%s/%s" % (path, filename)
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False

    return True

def user_photo(img_url, filename):
    try:
        image_on_web = urllib.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()

            path = os.getcwd() + "/users"
            file_path = "%s/%s" % (path, filename)
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False

    return True


def create_txt(image_lists):
    filename = "list_of_image.txt"

    target = open(filename, 'w')
    for url in image_lists:
        if url:
            target.write(url)
            target.write(", ")


def get_txt():
    filename = "list_of_image.txt"
    text_file = open(filename, "r")
    lines = text_file.read().split(', ')

    print lines
    print len(lines)
    text_file.close()

    return lines


def format_counter(num):
    num = str(num)
    if len(num) == 1:
        return "000" + num
    elif len(num) == 2:
        return "00" + num
    elif len(num) == 3:
        return "0" + num
    elif len(num) == 4:
        return num

# def wrap_response(user_request, response, callback = False):
#     if user_request.request.get("callback") and callback:
#         user_request.response.headers['Content-Type'] = "text/javascript"
#         response_text =


#     else:
#         user_request.response.headers['Content-Type'] = "application/json"
#         response_text = simplejson.dumps(response, False, False)


