from tkinter import filedialog, messagebox, Button, Tk, Label
import shutil
import os
import easygui


def file_open_box():
    path = easygui.fileopenbox()
    return path


def directory_open_box():
    path = filedialog.askdirectory()
    return path


def open_file():
    path = file_open_box()
    try:
        os.startfile(path)
    except TypeError:
        messagebox.showinfo("!خطا", "!فایل مورد نظر یافت نشد")


def copy_file():
    source = file_open_box()
    destination = directory_open_box()
    try:
        shutil.copy(source, destination)
        messagebox.showinfo("!موفق", "!فایل با موفقیت کپی شد")
    except:
        messagebox.showinfo("!خطا", "!کپی با شکست مواجه شد")


def delete_file():
    path = file_open_box()
    try:
        os.remove(path)
        messagebox.showinfo("!موفق", "!فایل با موفقیت حذف شد")
    except:
        messagebox.showinfo("!خطا", "!فایل حذف نشد")


def rename_file():
    try:
        file = file_open_box()
        path1 = os.path.dirname(file)
        extension = os.path.splitext(file)[1]
        new_name = input("new name: ")
        path2 = os.path.join(path1, new_name + extension)
        os.rename(file, path2)
        # messagebox.showinfo("!موفق", "!نام فایل با موفقیت تغییر یافت")
    except:
        messagebox.showinfo("!خطا", "!تغییر نام ناموفق بود")


def move_file():
    source = file_open_box()
    destination = directory_open_box()
    if source == destination:
        messagebox.showinfo("!خطا", "مسیر انتقال تغییر نکرده است")
    else:
        try:
            shutil.move(source, destination)
            messagebox.showinfo("!موفق", "!فایل با موفقیت انتقال یافت")
        except:
            messagebox.showinfo("!خطا", "انتقال فایل ناموفق بود")


def make_directory():
    path = directory_open_box()
    name = input("name: ")
    path = os.path.join(path, name)
    try:
        os.mkdir(path)
        # messagebox.showinfo("!موفق", "!دایرکتوری با موفقیت ایجاد شد")
    except:
        messagebox.showinfo("!خطا", "!دایرکتوری ساخته نشد")


def remove_directory():
    path = directory_open_box()
    try:
        os.rmdir(path)
    except:
        messagebox.showinfo("!خطا", "!دایرکتوری حذف نشد")


def list_files():
    path = directory_open_box()
    file_list = sorted(os.listdir(path))
    for i in file_list:
        print(i)


window = Tk()
window.title("مدیریت فایل")
window.configure(bg="black")
window.geometry("300x400")
Label(window, text="چه کاری انجام دهم؟").pack()
Button(window, command=open_file, text="بازکردن فایل",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=copy_file, text="کپی فایل",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=delete_file, text="حذف فایل",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=rename_file, text="تغییر نام فایل",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=move_file, text="انتقال فایل",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=make_directory, text="ایجاد فولدر",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=remove_directory, text="حذف فولدر",
       fg="blue", activebackground="red", bg="white").pack()
Button(window, command=list_files, text="لیست تمام فایل ها",
       fg="blue", activebackground="red", bg="white").pack()
window.mainloop()