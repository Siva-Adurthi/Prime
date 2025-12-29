
import speech_recognition as sr
import pyttsx3 as pt
import time
from playwright.sync_api import sync_playwright
import os
import re
import pyautogui as gui
from google import genai
import eel
import sys
    

eel.init('web')

GEMINI_API_KEY="AIzaSyDRKzx3JM5zPQbn0z0T7FpTBTHOFK3cSDs"
client=genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME="gemini-2.5-flash"

play=None
browser=None
page=None
context=None
lis=sr.Recognizer()

name="prime"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def speak(command):
    speech=pt.init()
    speech.setProperty('rate',135)
    speech.say(command)
    speech.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening.....")
            audio=lis.listen(source,phrase_time_limit=20)
            command=lis.recognize_google(audio)
            command=command.lower()
            print(command)
            return command
    except:
        return''
    
def skip_ad():
    global page
    try:
        selector=["button.ytp-skip-ad-button",
              "button.ytp-ad-button.ytp-skip-ad-button",
              "button#skip-button\\:2",
              "button:has-text('Skip')"]
        for sele in selector:
           btn=page.locator(sele)
           if btn.is_visible():
            btn.click()
            speak("Sir!, please keep your mic in mute mode")
            break
    except:
        return
    
def assistant(command):
    command=command.replace(name,'').strip()
    
    if "code " in command or "program " in command or "write " in command:
        response=client.models.generate_content(model=MODEL_NAME,contents="I want only code without any explanation even comments also"+command)
        for words in response.text:
            gui.typewrite(words,interval=0.1)
        speak("Sir !, Here is your program")
        
    else:
       response=client.models.generate_content(model=MODEL_NAME,contents="give with in 2 lines"+command)
       speak(response.text)

def command_exe(command):
    global play,page,browser,context   
    try:
        if 'youtube' in command: 
                play=sync_playwright().start()
                browser = play.chromium.launch(channel="msedge",headless=False,args=["--disable-blink-features=AutomationControlled",
                                                                        "--disable-features=IsolateOrigins,site-per-process",
                                                                        "--disable-site-isolation-trials",
                                                                        "--no-sandbox",
                                                                        "--disable-dev-shm-usage",
                                                                        "--start-maximized"])
                context=browser.new_context(user_agent="Mozilla/5.0(Window NT 10.0;Win64;x64)",no_viewport=True)
                context.add_init_script("""Object.defineProperty(navigator,'webdriver',{get: () => undefined});""")
                page=context.new_page()
                speak("yes boss!, Opening youtube")
                page.goto("https://www.youtube.com",wait_until="networkidle")
                command=command.replace("open ",'').replace("and ",'').replace("youtube ",'').strip()
                if 'search' in command or 'search for' in command:
                    command=command.replace('search for','').replace('search','').replace(name+' ','').replace('ok ','').strip()
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    page.wait_for_selector("input[placeholder='Search']",timeout=0)
                    speak(f"searching for {command}")
                    page.fill("input[placeholder='Search']",command)
                    page.click("button[aria-label='Search']")

                while True:
                    command=take_command()
                    if "seek" in command or "forward" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        command=command.replace(name+" ",'').replace('ok ','').strip()
                        if re.search(r'\d',command):
                            num=int(re.search(r'\d+',command).group())
                            digi=num//5
                            for i in range(digi):
                               page.keyboard.press("ArrowRight")
                               time.sleep(0.5)
                        else:
                            page.press("body","ArrowRight")

                    elif "back" in command or "backward" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        command=command.replace(name+" ",'').replace('ok ','').strip()
                        if re.search(r'\d',command):
                            num=int(re.search(r'\d+',command).group())
                            digi=num//5
                            for i in range(digi):
                               page.keyboard.press("ArrowLeft")
                               time.sleep(0.5)
                        else:
                            page.press("body","ArrowRight")

                    elif 'search' in command or 'search for' in command :
                        command=command.replace('search for','').replace('search','').replace(name+' ','').replace('ok ','').strip()
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("input[placeholder='Search']",timeout=0)
                        speak(f"searching for {command}")
                        page.fill("input[placeholder='Search']",command)
                        page.click("button[aria-label='Search']")

                    elif "minimize" in command and "window" in command or "minimise" in command and "window"in command:
                        speak("yes sir!")
                        gui.hotkey('win','d')
                        
                    elif "maximize" in command and "window" in command or "maximise" in command and "window" in command:
                        speak("yes sir!")
                        gui.hotkey('win','d')

                    elif 'first' in command or "1st" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok boss!")
                        videos.nth(0).locator("a#video-title").click()

                    elif 'second' in command or "2nd" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok sir!")
                        videos.nth(1).locator("a#video-title").click()

                    elif 'third' in command or "3rd" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("yes boss!")
                        videos.nth(2).locator("a#video-title").click()

                    elif 'fourth' in command or "4th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok boss!")
                        videos.nth(3).locator("a#video-title").click()

                    elif 'fifth' in command or "5th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("yes boss!")
                        videos.nth(4).locator("a#video-title").click()

                    elif 'sixth' in command or "6th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok boss!")
                        videos.nth(5).locator("a#video-title").click()

                    elif 'seventh' in command or "7th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok sir!")
                        videos.nth(6).locator("a#video-title").click()

                    elif 'eighth' in command or "8th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("yes boss!")
                        videos.nth(7).locator("a#video-title").click()
                    
                    elif 'nineth' in command or "9th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("yes sir!")
                        videos.nth(8).locator("a#video-title").click()
                    
                    elif 'tenth' in command or "10th" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.wait_for_selector("ytd-video-renderer",timeout=0)
                        videos=page.locator("ytd-video-renderer")
                        speak("ok sir!")
                        videos.nth(9).locator("a#video-title").click()

                    elif 'skip' in command or 'ad' in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        skip_ad()
                        
                    elif "play" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.press("body","k")

                    elif "pause" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        page.press("body","k")
                   
                    elif "close" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        browser.close()
                        play.stop()
                        page=None
                        play=None
                        browser=None
                        return " "
                    
                    elif 'share' in command or "link" in command or 'copy' in command:
                        page.get_by_role("button",name='Share').click(force=True)
                        time.sleep(1)
                        page.get_by_role("button",name='Copy').click(force=True)
                        speak("Link is copied sir!")
                        for i in range(3):
                            page.keyboard.press("Escape")
                            time.sleep(0.2)

                    elif "maximize" in command or "maximise" in command or "big" in command :
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        speak("yes boss!")
                        page.press("body",'f')
                        time.sleep(1)
                        page.press("body","k")
                        speak("Sir!, please keep your mic in mute mode")
                        page.keyboard.press("k")

                    elif 'minimize' in command or "minimise" in command or "small" in command :
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        speak("yes boss!")
                        page.press("body",'f')
                        time.sleep(1)
                        page.press("body","k")
                        speak("Sir!, please keep your mic in mute mode")
                        page.keyboard.press("k")
                        
                    elif "volume up" in command or "increase" in command or "raise" in command:
                        if re.search(r'\d+',command):
                            num=int(re.search(r'\d+',command).group())
                            digi=num//2
                            for i in range(digi):
                                gui.hotkey('volumeup')
                                time.sleep(0.3)
                        else:
                            gui.hotkey("volumeup")

                    elif "volume down" in command or "decrease" in command or "reduce" in command:
                        if re.search(r'\d+',command):
                            num=int(re.search(r'\d+',command).group())
                            digi=num//2
                            for i in range(digi):
                                gui.hotkey('volumedown')
                                time.sleep(0.3)
                        else:
                            gui.hotkey("volumedown")

                    elif "scroll up" in command or "up" in command:
                        page.keyboard.press("PageUp")

                    elif "scroll down" in command or "down" in command:
                        page.keyboard.press("PageDown")
                    
                    elif "open" in command or "launch" in command:
                        page.mouse.move(135,856)
                        page.mouse.move(856,200)
                        browser.close()
                        play.stop()
                        page=None
                        play=None
                        browser=None
                        return command

                    else:
                        speak("sorry sir!, please say it again!")

        elif "whatsapp" in command :
            os.system("taskkill /F /IM msedge.exe")
            play=sync_playwright().start()
            browser=play.chromium.launch_persistent_context(channel="msedge",user_data_dir="C:\\Users\\Venkata Siva Prasad\\AppData\\Local\\Microsoft\\Edge\\User Data",
                                                            headless=False,
                                                            args=["--start-maximized"],
                                                            no_viewport=True)
            page=browser.new_page()
            speak("yes boss!, Opening whatsapp")
            page.goto("https://web.whatsapp.com/",wait_until="networkidle")
            time.sleep(2)
            command=command.replace("open whatsapp",'').strip()
            try:
                obj=page.wait_for_selector("canvas[aria-label='Scan this QR code to link a device!']",timeout=10000)
                if obj:
                    speak("Sir!, please login your whatsapp account")
            except:
                pass
                if "send" in command or "message" in command or "search" in command:
                    comand=command
                    st=comand.rfind("to")
                    print(st)
                    ch=comand[st+3:]
                    remove=["and","send","message","to",ch]
                    words=command.split()
                    message=[w for w in words if w not in remove]
                    word=" ".join(message)
                    print(word)
                    page.wait_for_selector("div[aria-label='Search input textbox']",timeout=0)
                    speak(f"searching for {ch}")
                    page.fill("div[aria-label='Search input textbox']",'')
                    page.fill("div[aria-label='Search input textbox']",ch)
                    page.keyboard.press("Enter")
                    page.wait_for_selector("div[aria-placeholder='Type a message']",timeout=0)
                    page.fill("div[aria-placeholder='Type a message']",word)
                    page.keyboard.press("Enter")
                    speak("Message is successfully send sir!")
                    
            
            while True:
                command=take_command()
                if "search" in command or "search for" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    command=command.replace('search for','').replace('search','').replace(name+' ','').replace('ok ','').replace(" ",'').strip()
                    page.wait_for_selector("div[aria-label='Search input textbox']",timeout=0)
                    speak(f"ok sir!, searching for {command}")
                    page.fill("div[aria-label='Search input textbox']",'')
                    page.fill("div[aria-label='Search input textbox']",command)
                    page.keyboard.press("Enter")
                    speak("sir!, if you didn't get, desired contact, please say first 2 or 4 letters in a contact name")
                
                elif "first" in command or "1st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(0).click(force=True)

                elif "second" in command or "2st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(1).click(force=True)

                elif "third" in command or "3st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(2).click(force=True)

                elif "fourth" in command or "4st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(3).click(force=True)
                
                elif "fifth" in command or "5st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(4).click(force=True)
                
                elif "sixth" in command or "6st" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    contact=page.locator("div[role='row']")
                    contact.nth(5).click(force=True)
                    
                elif "picture" in command or "image" in command or "video" in command or "audio" in command:
                    speak("sorry sir!, I can't send images or audios or videos")

                elif "send" in command or "message" in command:
                   page.mouse.move(135,856)
                   page.mouse.move(856,200)
                   command=command.replace('send ','').replace('message ','').replace('for ','').replace('a ','').strip()
                   page.wait_for_selector("div[aria-placeholder='Type a message']",timeout=0)
                   page.fill("div[aria-placeholder='Type a message']",command)
                   page.keyboard.press("Enter")
                   speak("Message is successfully send sir!")

                elif "logout" in command:
                    speak("ok boss!")
                    page.locator("button[aria-label='Menu']").first.click(force=True)
                    page.get_by_text("Log out").click(force=True)
                    page.locator("//button//span[text()='Log out']").click(force=True)
                    
                elif "open" in command or "launch" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    browser.close()
                    play.stop()
                    page=None
                    play=None
                    browser=None
                    return command
                
                elif "close" in command or "exit" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    speak("ok sir!")
                    browser.close()
                    play.stop()
                    page=None
                    play=None
                    browser=None
                    
                    return " "
                
                elif "call" in command:
                    speak("Sir!, it is impossiable to call through whatsapp web")
        
        elif "notepad" in command:
            os.system('notepad.exe')
            time.sleep(2)
            gui.hotkey('ctrl','shift','n')
            if "code" in command or "program " in command or "write" in command:
                command=command.replace("open ",'').replace("notepad ",'').replace("and ",'').replace("write ",'').strip()
                assistant(command)
                
            while True:
                command=take_command()
                if "save" in command:
                    gui.hotkey('ctrl','s')

                elif "open" in command or "launch" in command:
                    os.system("taskkill /im notepad.exe /f")
                    return command
                
                elif "close" in command:
                    os.system("taskkill /im notepad.exe /f")
                    return " "

        elif "google" in command or "edge" in command:
            os.system("taskkill /F /IM msedge.exe")
            play=sync_playwright().start()
            browser=play.chromium.launch_persistent_context(channel="msedge",user_data_dir="C:\\Users\\Venkata Siva Prasad\\AppData\\Local\\Microsoft\\Edge\\User Data",
                                                            headless=False,
                                                            args=["--start-maximized"],
                                                            no_viewport=True)
            page=browser.new_page()
            speak("yes boss!, Opening bowser")
            page.goto("https://www.google.com/",wait_until="networkidle")
            command=command.replace('google ','').replace('edge','').replace('microsoft','').replace('msedge','').replace('and ','').replace('chrome','').replace('open','').replace('launch','').strip()
            if "search for" in command or "search " in command:
                command=command.replace('search','').replace('for','').replace(name+' ','').strip()
                page.wait_for_selector("textarea[aria-label='Search']",timeout=0)
                page.fill("textarea[aria-label='Search']",command)
                page.keyboard.press("Enter")
            while True:
                command=take_command()
                if "search for" in command or "search " in command:
                    page.mouse.move(329,512)
                    page.mouse.move(512,465)
                    command=command.replace('search','').replace('for','').replace(name+' ','').strip()
                    page.wait_for_selector("textarea[aria-label='Search']",timeout=0)
                    page.fill("textarea[aria-label='Search']",command)
                    page.keyboard.press("Enter")

                elif "open" in command or "launch" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    browser.close()
                    play.stop()
                    page=None
                    play=None
                    browser=None
                    return command
                
                elif "close" in command or "exit" in command:
                    page.mouse.move(135,856)
                    page.mouse.move(856,200)
                    speak("ok sir!")
                    browser.close()
                    play.stop()
                    page=None
                    play=None
                    browser=None
                    return " "
                
                else:
                    speak(" sorry sir!, due to bot detection, I cannot perfrom specific task")

        else:
            speak("sir!, i cannnot access that perticular application")
            return ' '

    except:
        speak("sir !, I think your network is slow")
        browser.close()
        play.stop()
        page=None
        play=None
        browser=None 
        return " "       
@eel.expose                   
def main():
 
  speak(f"hi sir , I am your {name} ")
  while True:
    command=take_command()
    command=command.replace(name+"",'').strip()
    if 'hello'==command or 'hey'==command or 'hi'==command:
        speak(f"hi sir !, how can i assist you ?")
    elif name in command or name not in command:
        if 'open' in command or 'launch' in command:
            while command!=" ":
               command=command_exe(command)
        elif "who" in command and "create" in command or "creator" in command:
            speak("I'm created by, my boss Siva")
        elif "your name" in command:
            speak(f"my name is {name} and I'm an personal assistant")
        elif "who are you" in command:
            speak("I'm mister siva prasad's personal assistant")
        elif "bye" in command or "exit" in command or "see you" in command:
            speak("ok bye sir!, see u later")
            return
        elif "shut down" in command:
            os.system("shutdown /s /t 0")
        elif "restart" in command:
            os.system("shutdown /r /t 0")
        else:
            assistant(command)

if __name__=="__main__":
    eel.start("jarvis.html",size=(1920 ,1080))
    main()

