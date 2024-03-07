import speech_recognition as sr
import pyttsx3
import dialogflow_v2 as dialogflow
import os
import requests
import datetime
from googlesearch import search

# Set up credentials for Dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print("Sorry, an error occurred. Please try again later.")

def detect_intent(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("your-project-id", "your-session-id")
    text_input = dialogflow.types.TextInput(text=text, language_code="en-US")
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}."

def get_current_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%B %d, %Y")
    return f"Today's date is {current_date}."

def get_weather():
    api_key = "your-weather-api-key"
    city = "your-city"
    url = f"http://api.weatherapi.com/v1/current.json?key={"4163215dcdd443aaa7dcfe5e99d0eca0"}&q={city}"
    response = requests.get(url).json()
    temperature = response["current"]["temp_c"]
    condition = response["current"]["condition"]["text"]
    return f"The weather in {city} is currently {condition} with a temperature of {temperature} degrees Celsius."

def get_news():
    api_key = "your-news-api-key"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={"4163215dcdd443aaa7dcfe5e99d0eca0"}"
    response = requests.get(url).json()
    articles = response["articles"]
    headlines = [article["title"] for article in articles[:5]]
    news = "Here are the latest news headlines: " + ", ".join(headlines)
    return news

def search_google(query):
    try:
        speak("I'm not sure about that. Let me look it up for you.")
        search_results = list(search(query, num=1, stop=1, pause=2))
        if search_results:
            speak(f"According to my search results, {search_results[0]}")
        else:
            speak("I couldn't find any relevant information.")
    except Exception as e:
        speak("Sorry, there was an error while searching. Please try again later.")

def start_jarvis():
    while True:
        user_input = listen()
        if user_input:
            if user_input.lower() == "jarvis":
                speak("Hello! How can I assist you today?")
                while True:
                    user_input = listen()
                    if user_input:
                        response = detect_intent(user_input)
                        if response:
                            if response == "getCurrentTime":
                                speak(get_current_time())
                            elif response == "getCurrentDate":
                                speak(get_current_date())
                            elif response == "getWeather":
                                speak(get_weather())
                            elif response == "getNews":
                                speak(get_news())
                            elif response.lower() == "goodbye":
                                speak("Goodbye! Have a great day!")
                                return
                            else:
                                search_google(user_input)
                        else:
                            speak("I'm sorry, I cannot assist with that.")

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Start Jarvis
start_jarvis()
