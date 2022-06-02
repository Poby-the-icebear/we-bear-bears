from datetime import datetime
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import numpy as np


window = tk.Tk()
window.geometry("500x500")
window.title("PLAN_A")
window.config(bg='lavender')
window.resizable(False, False)
treeview = ttk.Treeview(window, selectmode='browse')
treeview.grid(row=1, column=1, columnspan=4, padx=20, pady=20)
treeview["columns"] = ("1", "2", "3", "4")
treeview['show'] = 'headings'
treeview.column("1", width=50, anchor='center')
treeview.column("2", width=130, anchor='center')
treeview.column("3", width=80, anchor='center')
treeview.column("4", width=197, anchor='center')
treeview.heading("1", text="D-day")
treeview.heading("2", text="내용")
treeview.heading("3", text="과제/시험")
treeview.heading("4", text="일정")

Today = datetime.today().strftime("%Y-%m-%d")

l0 = tk.Label(window, text=Today, font=16, width=30, anchor="center")
l0.grid(row=2, column=1, columnspan=4)

l1 = tk.Label(window, text='내용: ', width=10, anchor="center", bg='lavender')
l1.grid(row=3, column=1, pady=20)

t1 = tk.Text(window, height=1, width=10, bg='white')
t1.grid(row=3, column=2)

radio_v = tk.StringVar()
radio_v.set('과제')
r1 = tk.Radiobutton(window, text='과제', variable=radio_v, value='과제', bg='lavender')
r1.grid(row=3, column=3, pady=20)

r2 = tk.Radiobutton(window, text='시험', variable=radio_v, value='시험', bg='lavender')
r2.grid(row=3, column=4, pady=20)

l3 = tk.Label(window, text='날짜: ', width=10, bg='lavender')
l3.grid(row=5, column=1, pady=20)

t3 = tk.Text(window, height=1, width=20, bg='white')
t3.grid(row=5, column=2, pady=20)

b1 = tk.Button(window, text='일정 추가', width=10,
               command=lambda: add_data(), bg='lavender')
b1.grid(row=6, column=3, pady=20)

b2 = tk.Button(window, text='일정 삭제', width=10, command=lambda: delete_data(), bg='lavender')
b2.grid(row=6, column=4, pady=20)


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def fixed_map(option):
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]


style = ttk.Style()
style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))


def add_data():
    all_data = [datetime.strptime(treeview.item(child)['values'][-1].rstrip(), "%Y-%m-%d") for child in
                treeview.get_children()]
    my_task = t1.get("1.0", END)
    my_selection = radio_v.get()
    my_date = t3.get("1.0", END)
    present = validate_date(my_date.rstrip())
    if present is True and my_date.rstrip() != '':
        new_date = datetime.strptime(my_date.rstrip(), "%Y-%m-%d")
        try:
            array = np.asarray(all_data)
            idx = (np.abs(array - new_date)).argmin()
            if (array[idx] - new_date).days >= 0:
                index = idx
            else:
                index = idx + 1
        except:
            index = 0
        right_now = datetime.strptime(Today, "%Y-%m-%d")
        due_date = new_date - right_now
        if due_date.days < 0:
            messagebox.showwarning('warning', '이미 지난 날짜입니다.')
        elif due_date.days == 0:
            treeview.insert("", index=index, values=('D-day', my_task, my_selection, my_date), tags=str(due_date.days))
            color_change(index)
        else:
            treeview.insert("", index=index, values=('D-' + str(due_date.days), my_task, my_selection, my_date),
                            tags=str(due_date.days))
            color_change(index)

    elif present is False and my_date.rstrip() != '':
        messagebox.showwarning("warning", "유효한 날짜가 아닙니다.")
    else:
        messagebox.showwarning("warning", "아무 것도 입력 되지 않았습니다.")

    t1.delete('1.0', END)
    t3.delete('1.0', END)
    t1.focus()


def delete_data():
    selected_item = treeview.selection()[0]
    treeview.delete(selected_item)


def color_change(value):
    tg = [(treeview.item(child)['tags']) for child in treeview.get_children()]
    tg_value = int(tg[value][0])
    tg_name = tg[value][0]
    if 5 < tg_value <= 7:
        treeview.tag_configure(tg_name, foreground='yellow')
    elif 2 < tg_value <= 5:
        treeview.tag_configure(tg_name, foreground='orange')
    elif 0 <= tg_value <= 2:
        treeview.tag_configure(tg_name, foreground='red')


window.mainloop()
