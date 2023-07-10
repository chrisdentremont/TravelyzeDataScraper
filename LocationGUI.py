import requests
from bs4 import BeautifulSoup
import openai
import threading
import json
import time

openai.api_key = "" 

# The overall dictionary that will contain all information about a country
dataToSubmit = {}

def getCountryData(country, url):
    # Scrape the URL and get data about the country
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    countryData = {}

    # Check if a specific section exists, and pull the data if it does
    if soup.find(id="Cuisine"):
        cuisine_text = ""
        cuisine = soup.find(id="Cuisine").parent
        for tag in cuisine.next_siblings:
            if tag.name == 'h3':
                break
            elif tag.name == 'p':
                cuisine_text += tag.text + "\n"

        prompt_complete = False
        while not prompt_complete:
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
                {"role": "system", "content" : "Make a short summary of this text: " + cuisine_text}
                ])
                countryData['Cuisine'] = completion.choices[0].message.content
                prompt_complete = True
            except:
                time.sleep(70)

    if soup.find(id="Transportation"):
        transportation_text = ""
        transportation = soup.find(id="Transportation").parent
        for tag in transportation.next_siblings:
            if tag.name == 'h3':
                break
            elif tag.name == 'p':
                transportation_text += tag.text + "\n"

        prompt_complete = False
        while not prompt_complete:
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
                {"role": "system", "content" : "Make a short summary of this text: " + transportation_text}
                ])
                countryData['Transportation'] = completion.choices[0].message.content
                prompt_complete = True
            except:
                time.sleep(70)

    if soup.find(id="Education"):
        education_text = ""
        education = soup.find(id="Education").parent
        for tag in education.next_siblings:
            if tag.name == 'h3':
                break
            elif tag.name == 'p':
                education_text += tag.text + "\n"

        prompt_complete = False
        while not prompt_complete:
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
                {"role": "system", "content" : "Make a short summary of this text: " + education_text}
                ])
                countryData['Education'] = completion.choices[0].message.content
                prompt_complete = True
            except:
                time.sleep(70)

    if soup.find(id="Sports"):
        sports_text = ""
        sports = soup.find(id="Sports").parent
        for tag in sports.next_siblings:
            if tag.name == 'h3':
                break
            elif tag.name == 'p':
                sports_text += tag.text + "\n"

        prompt_complete = False
        while not prompt_complete:
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
                {"role": "system", "content" : "Make a short summary of this text: " + sports_text}
                ])
                countryData['Sports'] = completion.choices[0].message.content
                prompt_complete = True
            except:
                time.sleep(70)

    dataToSubmit[country] = countryData
    print(country + " is done")

def generateSummaries():
    # Retrieve the entered URL, send a GET request to get HTML content and pass it to BeautifulSoup to parse through the HTML
    countryListURL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    page = requests.get(countryListURL)
    soup = BeautifulSoup(page.content, "html.parser")


    # Create dictionary with country names linked to their respective Wikipedia URL
    countryURLS = {}
    country_table = soup.find('table', attrs={'class':'wikitable'})
    country_table_body = country_table.find('tbody')
    country_table_rows = country_table_body.find_all('tr')
    for row in country_table_rows:
        if not row.find('td'):
            continue

        current_country = row.find('td')
        if not current_country.find('a'):
            continue

        current_country_link = current_country.find('a')
        countryURLS[current_country_link.text] = "https://en.wikipedia.org/" + current_country_link['href']

    thread_list = []
    for country in countryURLS.keys():
        thread = threading.Thread(target=getCountryData, args=(country, countryURLS[country],))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()
    
    with open("output.json", "w") as outfile:
        json.dump(dataToSubmit, outfile)

    # In their own threads, parse each URL and store data in their own dictionary
        # Dictionary has key of randomly generated ID, value is another dictionary with key as category + value is text
        #
        # - If the article doesn't have a category, use "N/A" 
        #
        # Categories: 
        # - Country Name
        # - Food & Restaurants
        # - Transportation
        # - Tourism/Landmarks

    # Sample Request
    #
    # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [
    #     {"role": "system", "content" : "Make a short summary of this text: " + pTexts[1].text}
    #     ])

generateSummaries()