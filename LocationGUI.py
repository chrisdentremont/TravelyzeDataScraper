import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import openai
import threading

openai.api_key = ""


def submitLocation():
    """Starts a new thread to """
    threading.Thread(target=generateSummaries).start()  


def generateSummaries():
    # Retrieve the entered URL, send a GET request to get HTML content and pass it to BeautifulSoup to parse through the HTML
    locationURL = URLentry.get()
    page = requests.get(locationURL)
    soup = BeautifulSoup(page.content, "html.parser")

    #Only accept Wikipedia URLs
    pageTitle = soup.find("title")
    if "Wikipedia" not in pageTitle.text:
        messagebox.showerror("Invalid Webpage", "This webpage is not from Wikipedia - please enter a Wikipedia URL.")
        return
        
    # If URL is Wikipedia link, display progress bar/label and clear output text
    outputSummary.delete("1.0", "end")
    progressBar.pack()
    progressBar.start()
    global progressLabel
    progressLabel['text'] = "Generating summaries..."

    summaryGroup = ""

    # Find every <p> element in HTML and have the OpenAI API summarize it to clean and shorten text. (Temporary, will flesh it out)
    pTexts = soup.find_all("p")
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
        {"role": "system", "content" : "Make a short summary of this text: " + pTexts[1].text}
        ])
    
    # Add the resulting text to the output string to display in the output text area
    summaryGroup += f"Before OpenAI =======================================================\n\n {pTexts[1].text} \n\n After OpenAI =======================================================\n\n {completion.choices[0].message.content} \n\n"
    
    # count = 0

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
    
    # Display the final output and clear the progress bar/label
    outputSummary.configure(state="normal")
    outputSummary.insert(tk.END, summaryGroup)
    outputSummary.configure(state="disabled")
    progressBar.stop()
    progressLabel['text'] = ""
    progressBar.pack_forget()


def sendToDatabase():
    #Implement sending data to database
    global progressLabel

# Main window widget
window = tk.Tk()
window.title("Travelyze Data Entry Tool")
window.geometry("800x700")

# Widgets to display text box to enter webpage URL
URLframe = tk.Frame(master=window)
URLframe.pack()
URLlabel = tk.Label(master=URLframe, text="Enter URL:", font=("Arial", 16))
URLlabel.pack(pady=(30, 0))
URLentry = tk.Entry(master=URLframe, width="300")
URLentry.pack(padx=50, pady=(0, 10))
URLbutton = tk.Button(text="Submit", font=("Arial", 12), command=submitLocation)
URLbutton.pack(pady=(0, 30))

# Widgets to display progress bar for submitting URL
progressFrame = tk.Frame(master=window)
progressFrame.pack()
progressLabel = tk.Label(master=progressFrame, font="Arial")
progressLabel.pack(pady=10)
progressBar = ttk.Progressbar(progressFrame, mode='indeterminate', length=280)

# Widgets to display text area to show output of web scraping
outputFrame = tk.Frame(master=window)
outputFrame.pack()
outputSummary = tk.Text(master=outputFrame, font="Arial", height=20)
outputSummary.configure(state="disabled")
outputSummary.pack(pady=(30, 0), padx=30)

bottomFrame = tk.Frame(master=window)
bottomFrame.pack(side=tk.RIGHT)
submitData = tk.Button(master=bottomFrame, text="Send to Database", font=("Arial", 12), command=sendToDatabase)
submitData.pack(pady=30, padx=30)

window.mainloop()