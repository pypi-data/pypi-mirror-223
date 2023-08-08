import customtkinter as ctk
import requests
import speech_recognition as sr
api_key = ''
heart = ''
eyes = ''
num = ''
if input('are you on raspian:\nif no prees enter to contineo... ') == 'yes':
    from smbus import SMBus
    addr = 0x8 # bus address
    bus = SMBus(num)
else:
    print('continuo ....')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

######################################################################################################
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"    
    return query
def kalibandain():
    if takeCommand() == 'potato':
        bus.write_byte(eyes, 1)
    elif takeCommand() == 'banana':
        bus.write_byte(heart, 2)
    else:
        return'Error not raspben os\nplease retry runing the code'
def sel_data():
    if entry.get() == 'botato':
        return kalibandain()
    else:
        return entry.get()
#####################################################################################################
def login():
    url = api_key+'/login'
    data = {'username': username_entry.get(), 'password': password_entry.get()}
    response = requests.post(url, data=data)
    if response.text == 'Login successful':
        login_frame.pack_forget()
        main_frame.pack()
    else:
        print(response.text)    
def send_post_request():
    url = api_key+'/send_data'
    data = {'input': sel_data(), 'user_id': username_entry.get()}
    response = requests.post(url, data=data)
    print(response.text)

def send_get_request():
    url = api_key+'/get_sent_data'
    params = {'user_id': username_entry.get()}
    response = requests.get(url, params=params)
    label.configure(text=response.text)


root = ctk.CTk()

login_frame = ctk.CTkFrame(root)

username_label = ctk.CTkLabel(login_frame, text='Username:')
username_entry = ctk.CTkEntry(login_frame)
password_label = ctk.CTkLabel(login_frame, text='Password:')
password_entry = ctk.CTkEntry(login_frame, show='*')
login_button = ctk.CTkButton(login_frame, text='Login', command=login)

main_frame = ctk.CTkFrame(root)

entry = ctk.CTkEntry(main_frame)
post_button = ctk.CTkButton(main_frame, text='Send POST Request', command=send_post_request)
get_button = ctk.CTkButton(main_frame, text='Send GET Request', command=send_get_request)
label = ctk.CTkLabel(main_frame)

def AI():
    root.geometry('500x500')
    username_label.pack(pady=10)
    username_entry.pack(pady=10)
    password_label.pack(pady=10)
    password_entry.pack(pady=10)
    login_button.pack(pady=10)
    login_frame.pack()
    entry.pack(pady=10)
    post_button.pack(pady=10)
    get_button.pack(pady=10)
    # voice_button.pack(pady=10)
    label.pack(pady=10)
    root.mainloop()






