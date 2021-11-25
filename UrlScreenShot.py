import re
import asyncio
from pyppeteer import launch
import PIL
from PIL import Image
import os
import itertools
import threading
from multiprocessing import Process
import time
import os
#import dns.resolver
import traceback
import multiprocessing
import base64
from io import BytesIO

#DEBUG = false
DEBUG = str(os.getenv('DEBUG')).lower() == "true"


def debugPrint(str):
    if(DEBUG):
        print(str)

def PIL2Base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

async def getScreenShot(urls, retObject, disableJavascript=True):
    debugPrint("getScreenShot: " + str(len(urls)))
    ret = []
    debugPrint("Launching browser")
    #Note regarding the following. In a perfect world, use a sandbox. 
    #For some reason, chrome's sandboxing doesnt work with pyppeteer on linux
    browser = await launch({ 'headless': True,  'args': [
        '--no-sandbox',
        '--single-process',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-zygote'
    ] })
    debugPrint("Browser Launched")
    page = await browser.newPage()
    if (disableJavascript): #Disabled javascript for safety
        await page.setJavaScriptEnabled(False)
    else:
        await page.setJavaScriptEnabled(True)
    start = time.time()
    for s in urls:
        start = time.time()
        url = s
        if ("https://" in url):
            url = url.replace("https://", "")
        if ("http://" in url):
            url = url.replace("http://", "")

        s = s.replace(".", "_")
        s = s.replace("/", "-")
        s = s.replace("\\", "-") #here we are removing characters that will cause problems with filenames
        debugPrint(s)

        try:
            debugPrint(f'=========================')
            #debugPrint(f'Testing for A record. url:{url}')
            #A = getARecord(url)
            #if (A == ""):
            #    raise
            #debugPrint(f'Got A record:{A}')
            debugPrint(f'Going to {url}, saving as {s}')
            data = await asyncio.wait_for(page.goto("http://" + url), 10)
            await page.screenshot({'path': str(s) + '.png', 'fullPage': False})
            im = Image.open(str(s) + ".png") #save the image to a temporary file, then read it
            bg = Image.new("RGB", im.size, (255,255,255))
            bg.paste(im,im) #copy the image to a new image object
            size = 512, 512
            bg.thumbnail(size)
            os.remove(str(s) + ".png") #We dont need the file anymore
            ret.append(PIL2Base64(bg))
            end = time.time()
            debugPrint("SUCCESS time taken: " + str(end - start))
        except:
            debugPrint("error checking " + url)
            end = time.time()
            debugPrint("FAIL time taken: " + str(end - start))
            traceback.debugPrint_exc()
        debugPrint(f'-------------------------')

    await browser.close()
    debugPrint("getScreenShot len(ret): " + str2(len(ret)))
    return ret

def main_start(s):
    asyncio.run(main(s))

def main2(s):
    asyncio.get_event_loop().run_until_complete(main(s))

#def getARecord(url):
#    result = dns.resolver.query('tutorialspoint.com', 'A')
#    for ipval in result:
#        print('IP', ipval.to_text())
#    if (len(result) > 0):
#        return str(result[0])
#    else:
#        return ""

def str2(str1): #debug function, useful to view returns without the base64 clogging the screen
    str_t = str(str1)
    return re.sub(r'[a-zA-Z0-9\+\/\=]{100,99999999}', 'BASE64', str_t)

def StartEventLoop(s, retObject, disableJavascript=True):
    loop = asyncio.new_event_loop() #pyppeteer uses asyncio, we're running in a thread here and making a new asyncio event loop. This allows threading.
    asyncio.set_event_loop(loop)
    retObject["ret"] = loop.run_until_complete(getScreenShot(s, {}, disableJavascript))
    debugPrint(str2(retObject))
    return retObject["ret"]
allUrls = []

def ScreenShotSingle(url, disableJavascript=True): #entry point of flask app
    manager = multiprocessing.Manager() #this allows us to pass an object to get the returned data
    ret = manager.dict()
    tmp = Process(target=StartEventLoop, args=([str(url)], ret, disableJavascript,))
    debugPrint(str(ret))
    tmp.start()
    tmp.join()
    return ret["ret"]


def ScreenshotMulti(urls, numThreads=1, disableJavascript=True): #assumes the urls are comma seperated
    manager = multiprocessing.Manager()
    processes = [] #keep track of the running processes, and the returned data

    allUrls = urls.split(",")
    numUrls = len(allUrls)

    urlsPerBucket = int(numUrls / numThreads)

    while (len(allUrls) > 0):
        bucketSize = urlsPerBucket
        if (len(allUrls) > bucketSize):
            bucketSize = len(allUrls)
        urls = allUrls[0:bucketSize]
        start = time.time()
        counter = 0
        while (len(allUrls) > 0):
            bucket = [] #The bucket of urls this process will handle.

            #This should be handled by the while statement
            bucket = allUrls[:urlsPerBucket+1]
            allUrls = allUrls[(urlsPerBucket + 1):] #take out the urls for this bucket

            print(f'bucket #{counter} contains {len(bucket)} urls. urls: {",".join(bucket)}')

            #start the process and keep track of it
            tmp = {} #dict to hold the data and process
            tmp["return"] = manager.dict()

            tmp2 = Process(target=StartEventLoop, args=(bucket, tmp["return"], disableJavascript,))
            tmp2.start()
            print(f'Thread #{len(processes)} started.')
            tmp["process"] = tmp2
            processes.append(tmp)
            counter += 1

    ret = []
    #wait for the threads to finish.
    print("There are " + str(len(processes)) + " processes")
    for i in range(len(processes)):
        proc = processes[i]
        proc["process"].join()
        ret += proc["return"]["ret"] #list concat here
    end = time.time()
    return ret


if __name__ == '__main__':
    tmp = ScreenShotSingle("https://www.whatismybrowser.com/detect/is-javascript-enabled")
    multi = [
    "www.whatismybrowser.com/detect/is-javascript-enabled",
    "google.com",
    "bing.com"
    ]
    #tmp = ScreenshotMulti(",".join(multi), 2)
    for i in range(len(tmp)):
        image_64_decode = base64.decodebytes(tmp[i]) 
        image_result = open("./" + str(i) + '.jpg', 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        image_result.close()
    #print("DONE")