import requests
from bs4 import BeautifulSoup
import openai
import threading

openai.api_key = "" 

def generateSummaries():
    # Retrieve the entered URL, send a GET request to get HTML content and pass it to BeautifulSoup to parse through the HTML
    countryListURL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    page = requests.get(countryListURL)
    soup = BeautifulSoup(page.content, "html.parser")


    # Create dictionary with country names linked to their respective Wikipedia URL
    countryURLS = {}

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