from tkinter import LabelFrame, Label, Entry, Button, Tk, messagebox, DISABLED, NORMAL
from datetime import datetime
from time import sleep
from threading import Thread
from pygame import mixer
from os import path


def alarmThread(total_sec=0, k=0):
    if mixer.music.get_busy():
        mixer.music.stop()

    btn_alarm['state'] = DISABLED

    while total_sec > 0:
        sleep(total_sec % 4294967)
        total_sec -= 4294967

    textview_now.configure(text="알람이 울리는 중입니다.")

    if path.isfile(path_music):
        mixer.music.load(path_music)
    mixer.music.play()
    sleep(10)

    textview_now.configure(text="현재 알람이 없습니다.")
    btn_alarm['state'] = NORMAL

    sleep(60)
    mixer.music.stop()


def alarm():
    hour = 0
    minute = 0
    sec = 0

    try:
        hour = int(input_hour.get())
        minute = int(input_minute.get())
        sec = int(input_sec.get())
    except ValueError:
        messagebox.showinfo("입력 오류", "숫자를 입력하셨나요?")
        return
    if hour == 0 and minute == 0 and sec == 0:
        messagebox.showinfo("엥?", "지금인데요?")
        return
    elif hour < 0 or minute < 0 or sec < 0:
        messagebox.showinfo("엥?", "지났는데요?")
        return

    now = datetime.now()
    nexth = hour + now.hour
    nextm = minute + now.minute
    nextc = sec + now.second

    dayafterday = ['오늘 ', '내일 ', '이틀 뒤 ', '3일 뒤 ', '4일 뒤 ', '한참 뒤 ', '한~~참 뒤 ']

    nextm += int(nextc / 60)
    nextc %= 60
    nexth += int(nextm / 60)
    nextm %= 60
    nextd = int(nexth / 24)
    if nextd > 10: nextd = 6
    elif nextd > 5: nextd = 5
    nexth %= 24

    textview_now.configure(
        text=dayafterday[nextd] + str(nexth) + "시 " + str(nextm) + "분 " + str(nextc) + "초에 알람이 울립니다.")

    total_sec = hour * 3600 + minute * 60 + sec

    alarmT = Thread(target=alarmThread, args=(total_sec, sec))
    alarmT.daemon = True
    alarmT.start()


if __name__ == "__main__":
    path_music = path.join(path.dirname(__file__), '알람소리.mp3')
    path_icon = path.join(path.dirname(__file__), 'clock.ico')

    mixer.init()

    win = Tk()
    win.title("알람따리 알람따")
    win.geometry("260x170")
    if path.isfile(path_icon):
        win.iconbitmap(path_icon)

    # 프레임
    frame_alarm = LabelFrame(win, text="얼마 뒤 울리게 할까요?")
    frame_alarm.grid(row=0, columnspan=7, padx=5, pady=5, ipadx=5, ipady=5)

    # 시분초 뷰
    textview_hour = Label(frame_alarm, text="시간")
    textview_hour.grid(row=0, column=1, padx=5, pady=5)
    textview_min = Label(frame_alarm, text="분")
    textview_min.grid(row=1, column=1, padx=5, pady=5)
    textview_sec = Label(frame_alarm, text="초")
    textview_sec.grid(row=2, column=1, padx=5, pady=5)

    # 시분초 입력
    input_hour = Entry(frame_alarm, justify='right')
    input_hour.grid(row=0, column=0, padx=5, pady=5)
    input_hour.insert(0, "0")
    input_minute = Entry(frame_alarm, justify='right')
    input_minute.grid(row=1, column=0, padx=5, pady=5)
    input_minute.insert(0, "0")
    input_sec = Entry(frame_alarm, justify='right')
    input_sec.grid(row=2, column=0, padx=5, pady=5)
    input_sec.insert(0, "0")

    # 알람세팅 버튼
    btn_alarm = Button(frame_alarm, text="알람", height=5, command=alarm)
    btn_alarm.grid(row=0, column=2, rowspan=5, padx=5, pady=5)

    # 알람현황 뷰
    textview_now = Label(win, anchor='center', text="현재 알람이 없습니다.")
    textview_now.grid(row=5, column=3, padx=5, pady=5)

    win.mainloop()
