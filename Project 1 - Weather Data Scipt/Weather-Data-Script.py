"""
DSC 510
Final Project
Author: Felipe Rodriguez
Date: 11/19/2022

Change Control Log #1
Change 1: Implemented Zipcode Lookup Function
Change 2: Implemented City and State Lookup Function
Change 3: Implemented Weather Lookup Function
Change 4: Implemented Output Zipcode Function
Change 5: Implemented City and State Output Function
Change 6: Implemented Main Function
Date of Change: 11/18/2022
Change to be Approved by: Michael Eller
Date Submitted: 11/19/22
Date Approved: TBD
"""
import requests
import string


def zip_lookup():
    # API to lookup zipcode(lat, lon) and format
    zip_url = 'http://api.openweathermap.org/geo/1.0/zip'
    payload = {}
    headers = {'cache-control': 'no-cache'}
    while True:
        # Establish lat and lon value
        zip_lon = 0
        zip_lat = 0
        # User input for zipcode
        zipcode = input('Please enter zipcode')
        try:
            float(zipcode)
        except ValueError:
            print('A zipcode was not entered')
            continue
        # Parameters for API request
        zip_query_string = {"zip": zipcode, "appid":
                            "c95457742f9936906058d38ad9153a1b"}
        # Try block for Connection and HTTP errors
        try:
            # API GET request for zipcode
            zip_response = requests.request("GET", zip_url, headers=headers,
                                            params=zip_query_string,
                                            data=payload)
        except requests.exceptions.ConnectionError:
            print('A connection could not be established.')
            print('Restarting program...')
            # Returns to beginning
            return
        except requests.exceptions.HTTPError:
            print('A valid zipcode needs to be entered.')
            # Returns to input
            continue
        else:
            # Convert Response into JSON
            zip_response_json = zip_response.json()
            # Try block for accessing lat and lon
            try:
                # Pulling latitude and longitude
                zip_lat = zip_response_json['lat']
                zip_lon = zip_response_json['lon']
            except KeyError:
                print('Please enter a valid zipcode.')
                continue
            break
    return zip_lat, zip_lon, zipcode


def city_state_lookup():
    # API to lookup city(lat, lon) and state and format
    state_url = 'http://api.openweathermap.org/geo/1.0/direct'
    payload = {}
    headers = {'cache-control': 'no-cache'}
    while True:
        # Establish lat and lon value
        city_lon = 0
        city_lat = 0
        # User input for city and state
        city = input('Please enter city')
        state = input('Please enter state')
        country = 'US'
        # Parameters for API request
        city_query_string = {"q": f"{city}, {state}, {country})", "limit": 1,
                             "appid": "c95457742f9936906058d38ad9153a1b"}
        # Try block for Connection and HTTP errors
        try:
            # API GET request for city and state
            state_response = requests.request("GET", state_url,
                                              headers=headers,
                                              params=city_query_string,
                                              data=payload)
        except requests.exceptions.ConnectionError:
            print('A connection could not be established.')
            print('Restarting program...')
            # Returns to beginning
            return
        except requests.exceptions.HTTPError:
            print('Please enter a valid city and state.')
            # Returns to input
            continue
        else:
            # Convert Response into JSON
            state_response_json = state_response.json()
            # Try block for handling dictionary reference
            try:
                coord = state_response_json[0]
            except IndexError:
                print('Please enter a valid city and state.')
                # Returns to input
                continue
            except KeyError:
                print('Please enter a valid city and state.')
                # Returns to input
                continue
            city_lat = coord['lat']
            city_lon = coord['lon']
            break
    return city_lat, city_lon, city, state


def weather_lookup(lat, lon):
    # API to lookup weather with lat and lon
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    payload = {}
    headers = {'cache-control': 'no-cache'}
    while True:
        # Establishes unit for temperature
        units = input('Enter F for Fahrenheit or C for Celsius')
        if units.upper() == 'F':
            units = "imperial"
            measurement = 'Fahrenheit'
            break
        elif units.upper() == 'C':
            units = "metric"
            measurement = 'Celsius'
            break
        # Handles if other values are entered
        else:
            print('Please enter a valid value')
    # Parameters for API request
    weather_query_string = {"lat": lat, "lon": lon, "appid":
                            "c95457742f9936906058d38ad9153a1b", "units": units}
    # Try block for Connection and HTTP errors
    try:
        # API GET request for Weather
        weather_response = requests.request("GET", weather_url,
                                            headers=headers,
                                            params=weather_query_string,
                                            data=payload)
    except requests.exceptions.ConnectionError:
        print('A connection could not be established.')
        print('Restarting program...')
        # Returns to beginning
        return
    except requests.exceptions.HTTPError:
        print('An error has occurred.')
        print('Restarting program...')
        # Returns to beginning
        return
    # Convert Response into JSON
    weather_response_json = weather_response.json()
    # Accesses weather data
    temp_data = weather_response_json['main']
    weather = weather_response_json['weather']
    weather_dict = weather[0]
    # Referencing the weather information
    condition_data = weather_dict['description']
    temp = temp_data['temp']
    temp_max = temp_data['temp_max']
    temp_min = temp_data['temp_min']
    pressure = temp_data['pressure']
    humidity = temp_data['humidity']
    return temp, temp_max, temp_min, pressure, humidity, measurement, \
           condition_data


def output_zipcode(zipcode, temp, temp_max, temp_min, pressure, humidity,
                   measurement, condition_data):
    # Formats percentage
    humidity_percent = "{:.0%}".format(humidity / 100)
    # Prints output
    print('The current weather condition for zipcode', zipcode, 'is',
          condition_data)
    print('Current temperature:', temp, measurement)
    print('High temperature:', temp_max, 'degrees', measurement)
    print('Low temperature:', temp_min, 'degrees', measurement)
    print('Current pressure:', pressure, 'hPa')
    print('Humidity:', humidity_percent)
    return


def output_city_state(city, state, temp, temp_max, temp_min, pressure,
                      humidity, measurement, condition_data):
    # Formats City and State
    city_upper = string.capwords(city)
    state_upper = string.capwords(state)
    # Formats humidity percentage
    humidity_percent = "{:.0%}".format(humidity / 100)
    # Prints output
    print('Current weather condition for', city_upper + ',', state_upper,
          'is', condition_data)
    print('Current temperature:', temp, 'degrees', measurement)
    print('High temperature:', temp_max, 'degrees', measurement)
    print('Low temperature:', temp_min, 'degrees', measurement)
    print('Current pressure:', pressure, 'hPa')
    print('Humidity:', humidity_percent)
    return


def main():
    while True:
        # Welcome message
        print('Welcome to the Weather Program!')
        # User input to see which function to call
        function = input('Would you like to enter Zipcode or City '
                         'information? Enter exit to quit.\n')
        # Handles if zipcode is entered
        if function.upper() == 'ZIPCODE':
            # Try block to handle connection issue
            try:
                # Zipcode lookup function call
                lat, lon, zipcode = zip_lookup()
            except TypeError:
                continue
            # Weather lookup function call
            temp, temp_max, temp_min, pressure, humidity, measurement, \
            condition_data = weather_lookup(lat, lon)
            # Output function call
            output_zipcode(zipcode, temp, temp_max, temp_min, pressure,
                           humidity, measurement, condition_data)
            continue
        # Handles if city is entered
        elif function.upper() == 'CITY':
            # Try block to handle connection issue
            try:
                # City and State lookup function call
                lat, lon, city, state = city_state_lookup()
            except TypeError:
                continue
            # Weather lookup function call
            temp, temp_max, temp_min, pressure, humidity, measurement, \
            condition_data = weather_lookup(lat, lon)
            # Output function call
            output_city_state(city, state, temp, temp_max, temp_min,
                              pressure, humidity, measurement, condition_data)
            continue
        # Handles if exit is entered, ends function
        elif function.upper() == 'EXIT':
            break
        # Handle if other values or entered
        else:
            print('Please enter a valid entry')
            continue


if __name__ == "__main__":
    main()
