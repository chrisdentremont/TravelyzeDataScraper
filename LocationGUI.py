import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import os
import openai
import threading
from threading import Event

openai.api_key = ""

cancelEvent = Event()

def submitLocation():
    cancelEvent = Event()

    URLbutton.config(text="Cancel", command=cancelGeneration)

    threading.Thread(target=generateSummaries, args=(cancelEvent,)).start()  
    
def cancelGeneration():
    cancelEvent.set()
    global progressLabel
    progressLabel['text'] = ""
    progressBar.stop()
    URLbutton.config(text="Submit", command=submitLocation)

def generateSummaries(cancelEvent):
    global progressLabel
    progressLabel['text'] = "Generating summaries..."
    locationURL = URLentry.get()
    page = requests.get(locationURL)
    soup = BeautifulSoup(page.content, "html.parser")

    pTexts = soup.find_all("p")
    count = 0

    summaryGroup = ""

    for element in pTexts:
        if cancelEvent.is_set():
            break

        # Skip the first iteration (the first index is empty for some reason)
        if count == 0:
            count += 1
            continue

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
        {"role": "system", "content" : "Make a short summary of this text: " + element.text}
        ])

        progressBar['value'] += 10

        summaryGroup += f"Before GPT: =======================================================\n\n {element.text} \n\n After GPT: =======================================================\n\n {completion.choices[0].message.content} \n\n"
        count += 1
        if count > 10: break 
    
    outputSummary.insert(tk.END, summaryGroup)
    progressBar.stop()

window = tk.Tk(className="Location Data Entry")
window.geometry("800x600")

URLframe = tk.Frame(master=window)
URLframe.pack()
URLlabel = tk.Label(master=URLframe, text="Enter Wikipedia URL:", font=("Arial", 16))
URLlabel.pack(pady=(30, 0))
URLentry = tk.Entry(master=URLframe, width="300")
URLentry.pack(padx=50, pady=(0, 10))
URLbutton = tk.Button(text="Submit", font=("Arial", 12), command=submitLocation)
URLbutton.pack(pady=(0, 30))

progressFrame = tk.Frame(master=window)
progressFrame.pack()
progressLabel = tk.Label(master=progressFrame, font="Arial")
progressLabel.pack(pady=10)
progressBar = ttk.Progressbar(progressFrame, mode='determinate', length=280)
progressBar.pack()

outputFrame = tk.Frame(master=window)
outputFrame.pack()
outputSummary = tk.Text(master=outputFrame, font="Arial", height=500)
outputSummary.pack(fill=tk.X, padx=30, pady=30)

window.mainloop()