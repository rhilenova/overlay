from channels import Group
import time
import json
from threading import Thread
import textwrap
import glob

import win32file
import win32event
import win32con
import os

PATH_TO_WATCH = 'C:\\Users\\Rhile.DESKTOP-EUSETK8\\Desktop\\'
PLAYING_FILE = os.path.join(PATH_TO_WATCH, 'now_playing.txt')
MESSAGES_FILE = os.path.join(PATH_TO_WATCH, 'messages.json')
ALBUM_DIR = 'D:\\Django\\overlay\\overlay_content\\static\\overlay_content\\test_album'

def ws_connect(message):
    global count
    global running

    Group('websock').add(message.reply_channel)
    count += 1
    if not running:
        ws_text_thread.start()
        ws_img_thread.start()
        running = True

    update_slides()
    update_playing()
    update_messages()

def ws_disconnect(message):
    global count
    Group('websock').discard(message.reply_channel)
    count -= 1
    if count == 0:
        running = False

def update_slides():
    images = ['static/overlay_content/test_album/' + x[len(ALBUM_DIR):] for x in glob.glob(os.path.join(ALBUM_DIR, '*.jpg'))]
    names = [os.path.splitext(os.path.split(x)[1])[0] for x in images]
    with open(os.path.join(ALBUM_DIR, 'captions.json'), 'r') as json_file:
        captions = json.load(json_file)
    text = [(image, captions[name]) for image, name in zip(images, names)]
    json_msg = json.dumps({"type": "slides", "text": text})
    print(json_msg)
    Group('websock').send({"text": json_msg})

def update_playing():
    with open(PLAYING_FILE, 'r') as f:
        # For some reason, foobar plugin has 3 random characters at the beginning
        now_playing_lines = textwrap.wrap(f.read()[3:], 50)
    json_msg = json.dumps({"type": "play", "text": now_playing_lines})
    print(json_msg)
    Group('websock').send({"text": json_msg})

def update_messages():
    with open(MESSAGES_FILE, 'r') as f:
        json_content = json.load(f)

    now_making_lines = textwrap.wrap(json_content['making'], 50)
    json_msg = json.dumps({"type": "make", "text": now_making_lines})
    print(json_msg)
    Group('websock').send({"text": json_msg})

    json_msg = json.dumps({"type": "hello", "text": json_content['hello']})
    print(json_msg)
    Group('websock').send({"text": json_msg})

class WSImgThread(Thread):
    def run(self):
        change_handle = win32file.FindFirstChangeNotification (
            PATH_TO_WATCH,
            0,
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        )
        playing_start = os.path.getmtime(PLAYING_FILE)
        messages_start = os.path.getmtime(MESSAGES_FILE)
        while running:
            result = win32event.WaitForSingleObject(change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                playing_new = os.path.getmtime(PLAYING_FILE)
                messages_new = os.path.getmtime(MESSAGES_FILE)
                if playing_new > playing_start:
                    update_playing()

                    playing_start = playing_new
                if messages_new > messages_start:
                    update_messages()

                    playing_start = playing_new
                win32file.FindNextChangeNotification(change_handle)

        win32file.FindCloseChangeNotification(change_handle)
        print('Stopped')

class WSTextThread(Thread):
    def run(self):
        change_handle = win32file.FindFirstChangeNotification (
            ALBUM_DIR,
            0,
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        )
        while running:
            result = win32event.WaitForSingleObject(change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                win32file.FindNextChangeNotification(change_handle)

        win32file.FindCloseChangeNotification(change_handle)
        print('Stopped')


count = 0
running = False
ws_text_thread = WSTextThread()
ws_img_thread = WSImgThread()
