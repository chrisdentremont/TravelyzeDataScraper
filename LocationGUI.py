import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os
import openai
import threading

openai.api_key = ""

def submitLocation():
    threading.Thread(target=generateSummaries).start()  


def generateSummaries():
    locationURL = URLentry.get()
    page = requests.get(locationURL)
    soup = BeautifulSoup(page.content, "html.parser")

    #Only accept Wikipedia URLs
    pageTitle = soup.find("title")
    if "Wikipedia" not in pageTitle.text:
        messagebox.showerror("Invalid Webpage", "This webpage is not from Wikipedia - please enter a Wikipedia URL.")
        return
        

    outputSummary.delete("1.0", "end")
    progressBar.pack()
    progressBar.start()
    global progressLabel
    progressLabel['text'] = "Generating summaries..."

    summaryGroup = ""


    pTexts = soup.find_all("p")
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
        {"role": "system", "content" : "Make a short summary of this text: " + pTexts[1].text}
        ])
    summaryGroup += f"Before GPT =======================================================\n\n {pTexts[1].text} \n\n After GPT =======================================================\n\n {completion.choices[0].message.content} \n\n"
    count = 0

    # for element in pTexts:
    #     if cancelEvent.is_set():
    #         break

    #     # Skip the first iteration (the first index is empty for some reason)
    #     # if count == 0:
    #     #     count += 1
    #     #     continue

    #     completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
    #     {"role": "system", "content" : "Make a short summary of this text: " + element.text}
    #     ])

    #     progressBar['value'] += 10

    #     summaryGroup += f"Before GPT: =======================================================\n\n {element.text} \n\n After GPT: =======================================================\n\n {completion.choices[0].message.content} \n\n"
    #     # count += 1
    #     # if count > 10: break 
    
    outputSummary.insert(tk.END, summaryGroup)
    progressBar.stop()
    progressLabel['text'] = ""
    progressBar.pack_forget()

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
progressBar = ttk.Progressbar(progressFrame, mode='indeterminate', length=280)

outputFrame = tk.Frame(master=window)
outputFrame.pack()
outputSummary = tk.Text(master=outputFrame, font="Arial", height=500)
outputSummary.pack(fill=tk.X, padx=30, pady=30)

window.mainloop()