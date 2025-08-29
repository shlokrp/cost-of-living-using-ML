import json  
import pandas as pd
from flask import Flask, jsonify, render_template, request, session

from data_loader import calculate_total_cost, backtrack_values
from statsmodels.tsa.holtwinters import ExponentialSmoothing

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Set a secret key for session management

def get_inflation_rates(json_file, country):
    try:
        with open(json_file, 'r') as file:
            inflation_data = json.load(file)
            for data_entry in inflation_data:
                if data_entry['country'] == country:
                    return data_entry
            # If country is not found in the inflation data
            print(f'Inflation rates not found for {country}')
            return {}
    except Exception as e:
        print("Error loading inflation data:", str(e))
        return {}

# Load inflation rates for all countries from the JSON file
def load_inflation_data(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print("Error loading inflation data:", str(e))
        return None

inflation_data = load_inflation_data("static/inflation_data.json")

# Function to calculate inflation rate for a given country and year
def get_inflation_rate(country, year):
    try:
        return inflation_data[country][str(year)]
    except KeyError:
        print(f"Inflation data not available for {country} in {year}")
        return None


def load_city_data(city_name, json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            city_data = next((entry for entry in data if entry['city'] == city_name), None)
            if city_data is None:
                print(f"City data not found for {city_name}")
            return city_data
    except Exception as e:
        print("Error loading city data:", str(e))
        return None


def predict_cost_of_living_ets(city_data, city_name, prediction_year):
    # Extract the cost of living values as a one-dimensional array
    cost_of_living_values = city_data.values.flatten()[::-1]
    
    model = ExponentialSmoothing(cost_of_living_values, trend='add')
    model_fit = model.fit()
    
    base_year = 2022  # Change the base year as needed
    start_year = base_year + 1  # Start from the year after the base year
    steps = prediction_year - start_year + 1  # Include the prediction year itself
    
    forecast = model_fit.forecast(steps=steps)

    return list(forecast)  # Return a list of forecasted values for each year

# Function to convert dictionary to DataFrame and transpose it
def dict_to_transposed_dataframe(data_dict):
    df = pd.DataFrame(data_dict.items(), columns=['Year', 'Cost of Living'])
    return df.set_index('Year').T

    
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except Exception as e:
        print("Error loading data:", str(e))
        return None
# Define a route for the homepage
@app.route('/')
def home():
    return render_template('Home.html')  # Render the home.html template

@app.route('/about-us')
def about_us():
    return render_template('AboutUs.html')  # Render the AboutUs.html template

@app.route('/our-team')
def our_team():
    return render_template('OurTeam.html')  # Render the OurTeam.html template

@app.route('/contact-us')
def contact_us():
    return render_template('ContactUs.html')  # Render the ContactUs.html template

# Define a route for the index page
@app.route('/get-started')
def get_started():
    # Fetch countries data and render city selection form
    try:
        countries_data = load_data('static/countries.json')
        return render_template('index.html', countries=countries_data)
    except Exception as e:
        print("Error:", str(e))
        return render_template('error.html', error_message='Failed to fetch countries data')

# Route to fetch countries data
@app.route('/countries')
def get_countries():
    try:
        countries_data = load_data('static/countries.json')
        if countries_data:
            return jsonify(countries_data)
        else:
            return jsonify({'error': 'Failed to fetch countries data'})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'An error occurred while fetching countries data'})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        city = request.form.get('selectedCity')
        country = request.form.get('selectedCountry')
        prediction_year = int(request.form.get('prediction_year'))
        no_of_adult = int(request.form.get('no_of_adult'))
        universities = int(request.form.get('universities'))
        schoolers = int(request.form.get('schoolers'))
        preschoolers = int(request.form.get('preschoolers'))
        no_of_infant = int(request.form.get('no_of_infant'))
        res_level = request.form.get('res_level')
        eat_out = int(request.form.get('eat_out'))
        alcohol = request.form.get('alcohol')
        alcohol_consumers = int(request.form.get('alcohol_consumers', 0))
        alcohol_consumption = int(request.form.get('alcohol_consumption', 0))
        cafe = int(request.form.get('cafe'))
        smoke = request.form.get('smoke')
        smoke_freq = request.form.get('smoke_freq')
        smoke_family_count = int(request.form.get('smoke_family_count', 0))
        travel_distance_car = float(request.form.get('travel_distance_car'))
        travel_distance_bike = float(request.form.get('travel_distance_bike'))
        taxi = int(request.form.get('taxi'))
        gym = int(request.form.get('gym'))
        movie = int(request.form.get('movie'))
        save_house = request.form.get('save_house')
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        save_house_years = int(request.form.get('save_house_years'))
        buy_car = request.form.get('buy_car')
        buy_car_years = int(request.form.get('buy_car_years'))
        car_type = request.form.get('car_type')
        cuisine = request.form.get('cuisine')
        food_pref = request.form.get('food_pref')
        no_of_cars = int(request.form.get('no_of_cars', 0))
        no_of_bikes = int(request.form.get('no_of_bikes', 0))

        data = {
            'city': city,
            'country': country,
            'prediction_year': prediction_year,
            'no_of_adult': no_of_adult,
            'universities': universities,
            'schoolers': schoolers,
            'preschoolers': preschoolers,
            'no_of_infant': no_of_infant,
            'res_level': res_level,
            'eat_out': eat_out,
            'alcohol': alcohol,
            'alcohol_consumers': alcohol_consumers,
            'alcohol_consumption': alcohol_consumption,
            'cafe': cafe,
            'smoke': smoke,
            'smoke_freq': smoke_freq,
            'smoke_family_count': smoke_family_count,
            'travel_distance_car': travel_distance_car,
            'travel_distance_bike': travel_distance_bike,
            'taxi': taxi,
            'gym': gym,
            'movie': movie,
            'save_house': save_house,
            'location': location,
            'bhk': bhk,
            'save_house_years': save_house_years,
            'buy_car': buy_car,
            'buy_car_years': buy_car_years,
            'car_type': car_type,
            'cuisine': cuisine,
            'food_pref': food_pref,
            'no_of_cars': no_of_cars,
            'no_of_bikes': no_of_bikes
        }

        # Further processing and calculations...
        # Calculate total cost of living for 2022
        original_value_2022_tuple = calculate_total_cost(data)
        print("Original values for 2022:", original_value_2022_tuple)  # Debugging statement


        total_eat_out_cost, total_alcohol_cost, total_coffee_cost, total_smoke_cost, total_travel_cost, total_leisure_cost, total_education_cost, total_save_house_amount, total_rent, total_amenities_cost, total_save_car_amount, total_internet_cost, total_call_cost, total_food_cost, total_cost = original_value_2022_tuple

        #Calculated Values for pie chart
        food_cost = total_eat_out_cost + total_coffee_cost + total_food_cost
        toxic_cost = total_alcohol_cost + total_smoke_cost
        miscellaneous = total_call_cost + total_internet_cost + total_leisure_cost
        housing_rent = total_rent + total_amenities_cost
        education_cost = total_education_cost
        save_house1 = total_save_house_amount
        save_car = total_save_car_amount
        travel_cost = total_travel_cost

        print("Food Cost:", food_cost)
        print("Toxic Cost:", toxic_cost)
        print("Miscellaneous Cost:", miscellaneous)
        print("Housing and Rent Cost:", housing_rent)
        print("Education Cost:", education_cost)
        print("Save House Amount:", save_house1)
        print("Save Car Amount:", save_car)
        print("Travel Cost:", travel_cost)


        
        # Calculate backtracked values
        backtracked_values_data = backtrack_values(total_cost, "static/inflation_data.json", country)
        if backtracked_values_data is None:
            return render_template('error.html', error_message='Error calculating backtracked values')
        # print("Backtracked values:", backtracked_values_data)  # Debugging statement


        # Create a transposed DataFrame from the backtracked values
        df_backtracked_values_transposed = dict_to_transposed_dataframe(backtracked_values_data)
        
        # Use the function to predict the cost of living for the prediction year
        forecast_ets_orignal= predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)
      #  print("Forecast using ETS:", forecast_ets)  # Debugging statement

        # Use the function to predict the cost of living for each year from 2023 to the prediction year
        forecast_ets_values = predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)

        # Print the forecasted values
        print("Forecasted Cost of Living for Each Year:")
        for year, forecast_value in zip(range(2023, prediction_year + 1), forecast_ets_values):
            print(f"Year {year}: ${forecast_value}")   

        data['city']='Mumbai'
        data['country']='India'
        mumbai_value= calculate_total_cost(data)
        print("Original values for Mumbai 2022:", mumbai_value)  # Debugging statement

        # Calculate backtracked values for Mumbai
        total_eat_out_cost, total_alcohol_cost, total_coffee_cost, total_smoke_cost, total_travel_cost, total_leisure_cost, total_education_cost, total_save_house_amount, total_rent, total_amenities_cost, total_save_car_amount, total_internet_cost, total_call_cost, total_food_cost, total_cost = mumbai_value
        backtracked_values_data = backtrack_values(total_cost, "static/inflation_data.json", country)
        if backtracked_values_data is None:
            return render_template('error.html', error_message='Error calculating backtracked values')
        # print("Backtracked values:", backtracked_values_data)  # Debugging statement


        # Create a transposed DataFrame from the backtracked values
        df_backtracked_values_transposed = dict_to_transposed_dataframe(backtracked_values_data)
        
        # Use the function to predict the cost of living for the prediction year
        forecast_ets_mumbai = predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)
        print("Forecast using ETS of Mumbai:", forecast_ets_mumbai[-1])  # Debugging statement
        
        data['city']='Sydney'
        data['country']='Australia'
        sydney_value= calculate_total_cost(data)
        print("Original values for Sydney 2022:", sydney_value)  # Debugging statement

        # Calculate backtracked values For Sydney
        total_eat_out_cost, total_alcohol_cost, total_coffee_cost, total_smoke_cost, total_travel_cost, total_leisure_cost, total_education_cost, total_save_house_amount, total_rent, total_amenities_cost, total_save_car_amount, total_internet_cost, total_call_cost, total_food_cost, total_cost = sydney_value
        backtracked_values_data = backtrack_values(total_cost, "static/inflation_data.json", country)
        if backtracked_values_data is None:
            return render_template('error.html', error_message='Error calculating backtracked values')
        # print("Backtracked values:", backtracked_values_data)  # Debugging statement


        # Create a transposed DataFrame from the backtracked values
        df_backtracked_values_transposed = dict_to_transposed_dataframe(backtracked_values_data)
        
        # Use the function to predict the cost of living for the prediction year
        forecast_ets_sydney = predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)
        print("Forecast using ETS of Sydney:", forecast_ets_sydney[-1])  # Debugging statement

        data['city']='New York'
        data['country']='United States'
        newyork_value= calculate_total_cost(data)
        print("Original values for New York 2022:", newyork_value)  # Debugging statement

        # Calculate backtracked values New York
        total_eat_out_cost, total_alcohol_cost, total_coffee_cost, total_smoke_cost, total_travel_cost, total_leisure_cost, total_education_cost, total_save_house_amount, total_rent, total_amenities_cost, total_save_car_amount, total_internet_cost, total_call_cost, total_food_cost, total_cost = newyork_value
        backtracked_values_data = backtrack_values(total_cost, "static/inflation_data.json", country)
        if backtracked_values_data is None:
            return render_template('error.html', error_message='Error calculating backtracked values')
        # print("Backtracked values:", backtracked_values_data)  # Debugging statement


        # Create a transposed DataFrame from the backtracked values
        df_backtracked_values_transposed = dict_to_transposed_dataframe(backtracked_values_data)
        
        # Use the function to predict the cost of living for the prediction year
        forecast_ets_newyork = predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)
        print("Forecast using ETS of New York:", forecast_ets_newyork[-1])  # Debugging statement

        data['city']='London'
        data['country']='United Kingdom'
        london_value= calculate_total_cost(data)
        print("Original values for London 2022:", london_value)  # Debugging statement

         # Calculate backtracked values London
        total_eat_out_cost, total_alcohol_cost, total_coffee_cost, total_smoke_cost, total_travel_cost, total_leisure_cost, total_education_cost, total_save_house_amount, total_rent, total_amenities_cost, total_save_car_amount, total_internet_cost, total_call_cost, total_food_cost, total_cost = london_value
        backtracked_values_data = backtrack_values(total_cost, "static/inflation_data.json", country)
        if backtracked_values_data is None:
            return render_template('error.html', error_message='Error calculating backtracked values')
        # print("Backtracked values:", backtracked_values_data)  # Debugging statement


        # Create a transposed DataFrame from the backtracked values
        df_backtracked_values_transposed = dict_to_transposed_dataframe(backtracked_values_data)
        
        # Use the function to predict the cost of living for the prediction year
        forecast_ets_london = predict_cost_of_living_ets(df_backtracked_values_transposed, city, prediction_year)
        print("Forecast using ETS of London:", forecast_ets_london[-1])  # Debugging statement     

        return render_template('result.html', 
                               city=city,
                               prediction_year=prediction_year,
                               forecast_ets_orignal=int(forecast_ets_orignal[-1]),
                               forecast_ets_values=forecast_ets_values,
                               forecast_ets_mumbai=int(forecast_ets_mumbai[-1]),
                               forecast_ets_sydney=int(forecast_ets_sydney[-1]),
                               forecast_ets_newyork=int(forecast_ets_newyork[-1]),
                               forecast_ets_london=int(forecast_ets_london[-1]),
                               food_cost=int(food_cost),
                               toxic_cost=int(toxic_cost),
                               miscellaneous_cost=int(miscellaneous),
                               housing_rent_cost=int(housing_rent),
                               education_cost=int(education_cost),
                               save_house_cost=int(save_house1),
                               save_car_cost=int(save_car),
                               travel_cost=int(travel_cost))
    except KeyError as e:
        error_message = f"Error: Missing field {e.args[0]}"
        return render_template('error.html', error_message=error_message)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print("Error:", error_message)  # Debugging statement
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)