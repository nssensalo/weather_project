from ast import If
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_html_content(city):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE#fetch weather data
    # city = city.replace(" ","+")
    html_content = session.get(f'https://www.wunderground.com/weather/us/{city[1]}/{city[0]}').text
    return html_content

def home(request):

    weather_data = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        city = city.split(', ')
        city[0] = city[0].replace(' ', '-')

        html_content = get_html_content(city)
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data = dict()

        error = soup.find('div', {'class':'columns small-12 city-header ng-star-inserted'})
        if "undefined" in error.text:
            weather_data['temp'] = "Unknown city"
        else:
            
            weather_data['temp'] = soup.find('span', {'class':'test-true wu-unit wu-unit-temperature is-degree-visible ng-star-inserted'}).text
            #weather_data['gust'] = soup.find('p', {'class':'wu-value wu-value-to'}).text
            weather_data['wind'] = soup.find('span', {'class':'test-false wu-unit wu-unit-speed ng-star-inserted'}).text
            
        
        # weather_data['daytime'] = soup.find('div', attrs={'id':'wob_dts'}).text
        # weather_data['status'] = soup.find('span', attrs={'id':'wob_dcp'}).text
        # weather_data['temp'] = soup.find('span', attrs={'id':'wob_tm'}).text
           
    return render(request, 'home.html', {'weather': weather_data})
