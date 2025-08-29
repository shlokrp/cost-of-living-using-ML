import pandas as pd
import json

def load_city_data(city_name, json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            city_data = next((entry for entry in data if entry['city'] == city_name), None)
            if city_data:
                return city_data
            else:
                return None
    except Exception as e:
        print("Error loading city data:", str(e))
        return None
    

def calculate_total_cost(data):
     # Validate city and country names
    city_data = load_city_data(data['city'], "static/countries.json")
    if not city_data:
        raise ValueError("City data not found")

    # Perform calculations using validated city and country names
    # city_data = df[(df['city'] == data['city']) & (df['country'] == data['country'])].iloc[0]

    total_members = data['no_of_adult'] + data['universities'] + 0.75 * data['schoolers'] + 0.5 * data['preschoolers'] + 0.5 * data['no_of_infant']
    
    total_cost = 0
    city = city_data['city']
    
    res_cost = 0  
    if data['res_level'] == 'inexpensive':
        res_cost = city_data['x1'] + city_data['x3']
    elif data['res_level'] == 'mid-range':
        res_cost = (city_data['x2']) / 2 + city_data['x3']

    eat_out_cost = (data['eat_out'] / 2) * res_cost
    total_eat_out_cost = eat_out_cost * total_members

    total_alcohol_cost = 0  
    if data['alcohol'] != 'none alcohol':
        alcohol_consumption = data['alcohol_consumption']
        if data['alcohol'] == 'local beer':
            alcohol_cost = data['eat_out'] * city_data['x4'] + alcohol_consumption * city_data['x25']
        elif data['alcohol'] == 'imported beer':
            alcohol_cost = data['eat_out'] * city_data['x5'] + alcohol_consumption * city_data['x26']
        elif data['alcohol'] == 'wine':
            alcohol_cost = (data['eat_out'] + alcohol_consumption) * city_data['x24']

        total_alcohol_cost = alcohol_cost * data['alcohol_consumers']
    else:
        total_alcohol_cost = 0

    total_coffee_cost = total_members * (data['cafe'] * city_data['x6'])

    total_smoke_cost = 0  
    if data['smoke'] == 'yes':
        smoke_freq = data.get('smoke_freq', None)
        if smoke_freq == "Once daily":
            total_smoke_cost = data['smoke_family_count'] * (city_data['x27'] * 1.5) 
        elif smoke_freq == "Once a week":
            total_smoke_cost = data['smoke_family_count'] * (city_data['x27'] / 5) 
        elif smoke_freq == "2-3 times a week":
            total_smoke_cost = data['smoke_family_count'] * (city_data['x27'] / 2) 
        elif smoke_freq == "Once a month":
            total_smoke_cost = data['smoke_family_count'] * (city_data['x27'] / 20) 
        elif smoke_freq == "More than once a day":
            total_smoke_cost = data['smoke_family_count'] * (city_data['x27'] * 3) 

    total_petrol_car = data['travel_distance_car'] / 12.5
    total_petrol_bike = data['travel_distance_bike'] / 40
    total_petrol = total_petrol_car + total_petrol_bike
    total_petrol_cost = total_petrol * city_data['x33']

    total_taxi_cost = data['taxi'] * city_data['x31'] * 5
    total_travel_cost = total_petrol_cost + total_taxi_cost

    total_gym_cost = data['gym'] * city_data['x39']
    total_movie_cost = total_members * (data['movie'] * city_data['x41'])
    total_leisure_cost = total_gym_cost + total_movie_cost

    total_preschool_cost = data['preschoolers'] * city_data['x42']
    total_school_cost = data['schoolers'] * (city_data['x43'] / 12)
    total_university_cost = data['universities'] * (city_data['x43'] * 1.5 / 12)
    total_education_cost = total_preschool_cost + total_school_cost + total_university_cost
    
    total_save_house_amount = 0

    if data['save_house'] == 'yes':
        if data['bhk'] == 1:
            if data['location'] == 'city center':
                total_price = city_data['x52'] * 30
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
            elif data['location'] == 'outskirts':
                total_price = city_data['x53'] * 30
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
        elif data['bhk'] == 2:
            if data['location'] == 'city center':
                total_price = city_data['x52'] * 60
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
            elif data['location'] == 'outskirts':
                total_price = city_data['x53'] * 60
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
        elif data['bhk'] == 3:
            if data['location'] == 'city center':
                total_price = city_data['x52'] * 90
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
            elif data['location'] == 'outskirts':
                total_price = city_data['x53'] * 90
                total_save_house_amount = total_price / (data['save_house_years'] * 12)
    
    total_save_car_amount = 0
    if data['buy_car'] == 'yes':
        car_type = data.get('car_type', '')
        if car_type == 'hatchback':
            total_car_price = city_data['x34']
            total_save_car_amount = total_car_price / (data['buy_car_years'] * 12)
        elif car_type == 'sedan':
            total_car_price = city_data['x35']
            total_save_car_amount = total_car_price / (data['buy_car_years'] * 12)
        elif car_type == 'suv':
            price_diff_ratio = (city_data['x35'] - city_data['x34']) / city_data['x34']
            total_car_price = city_data['x35'] + (price_diff_ratio * city_data['x35'])
            total_save_car_amount = total_car_price / (data['buy_car_years'] * 12)

    total_rent=0
    if data['location'] == 'city center':
        if data['bhk']==1:
            total_rent = city_data['x48']
        elif data['bhk']==3:
            total_rent = city_data['x50']
        elif data['bhk']==2:
            total_rent = (city_data['x48']+city_data['x50'])/2
    elif data['location'] =='outskirts':
        if data['bhk']==1:
            total_rent = city_data['x49']
        elif data['bhk']==3:
            total_rent = city_data['x51']
        elif data['bhk']==2:
            total_rent = (city_data['x49']+city_data['x51'])/2

    total_amenities_cost = city_data['x36'] * data['bhk'] / 3

    total_internet_cost = city_data['x38'] + total_members * city_data['x38']

    total_call_cost = city_data['x37'] * 200 * (data['no_of_adult'] + data['universities'])

    total_food_cost = 0
    row = city_data

    if data['cuisine'] == 'Indian':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 6
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13']
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 3
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 6
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13']
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 3
            egg_cost = row['x12'] * 3
            meat_cost = row['x14'] * 6 + row['x15'] * 6  
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Arabic':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13']
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 3
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost  
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13']
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 3
            egg_cost = row['x12'] * 5
            meat_cost = row['x14'] * 7 + row['x15'] * 7
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'American':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 3
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 3
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            egg_cost = row['x12'] * 5
            meat_cost = row['x14'] * 8 + row['x15'] * 8
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'English':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 5
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 5 + row['x17'] * 5 + row['x18'] * 5 + row['x19'] * 6 + row['x20'] * 6 + row['x21'] * 4 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 5
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            egg_cost = row['x12'] * 5
            meat_cost = row['x14'] * 8 + row['x15'] * 8
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Italian':
        if data['food_pref'] == 'veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 4+ row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 4 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4   
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 2
            meat_cost = row['x14'] * 6 + row['x15'] * 6    
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Japanese':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 5
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            total_food_cost = rice_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 5
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 2
            meat_cost = row['x14'] * 7 + row['x15'] * 7
            total_food_cost = rice_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Mexican':
        if data['food_pref'] == 'veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 5 + row['x17'] * 5 + row['x18'] * 5 + row['x19'] * 6 + row['x20'] * 6 + row['x21'] * 4 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 3
            meat_cost = row['x14'] * 6 + row['x15'] * 6
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'French':
        if data['food_pref'] == 'veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            bread_cost = row['x10'] * 20
            cheese_cost = row['x13'] * 1.5
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 3
            meat_cost = row['x14'] * 7 + row['x15'] * 7
            total_food_cost = bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Thai':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 6
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            total_food_cost = rice_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 6
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 2
            meat_cost = row['x14'] * 6 + row['x15'] * 6  
            total_food_cost = rice_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Chinese':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 10
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 10
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 10
            softdrink_cost = row['x7'] * 6
            egg_cost = row['x12'] * 5
            meat_cost = row['x14'] * 7 + row['x15'] * 7
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    elif data['cuisine'] == 'Spanish':
        if data['food_pref'] == 'veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 4 + row['x17'] * 4 + row['x18'] * 4 + row['x19'] * 5 + row['x20'] * 5 + row['x21'] * 3 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost 
        elif data['food_pref'] == 'non-veg':
            rice_cost = row['x11'] * 7
            bread_cost = row['x10'] * 15
            cheese_cost = row['x13'] * 1
            fruit_vegetable_cost = row['x16'] * 3 + row['x17'] * 3 + row['x18'] * 3 + row['x19'] * 4 + row['x20'] * 4 + row['x21'] * 2.5 + row['x22']
            milk_cost = row['x9'] * 8
            softdrink_cost = row['x7'] * 4
            egg_cost = row['x12'] * 3
            meat_cost = row['x14'] * 7 + row['x15'] * 7
            total_food_cost = rice_cost + bread_cost + cheese_cost + fruit_vegetable_cost + milk_cost + softdrink_cost + egg_cost + meat_cost

    total_food_cost = total_members * total_food_cost
    # total_cost = total_members * (eat_out_cost) +  total_alcohol_cost + total_members * (coffee_cost) + smoke_cost + travel_cost + leisure_cost + education_cost + save_house_amount + rent + amenities_cost + save_car_amount + internet_cost + call_cost + total_members * (total_food_cost)

    total_cost = total_eat_out_cost +  total_alcohol_cost + total_coffee_cost + total_smoke_cost + total_travel_cost + total_leisure_cost + total_education_cost + total_save_house_amount + total_rent + total_amenities_cost + total_save_car_amount + total_internet_cost + total_call_cost + total_food_cost
    # Print all calculated values individually
    # print("Total Eat Out Cost:", total_eat_out_cost)
    # print("Total Alcohol Cost:", total_alcohol_cost)
    # print("Total Coffee Cost:", total_coffee_cost)
    # print("Total Smoke Cost:", total_smoke_cost)
    # print("Total Travel Cost:", total_travel_cost)
    # print("Total Leisure Cost:", total_leisure_cost)
    # print("Total Education Cost:", total_education_cost)
    # print("Total Save House Amount:", total_save_house_amount)
    # print("Total Rent:", total_rent)
    # print("Total Amenities Cost:", total_amenities_cost)
    # print("Total Save Car Amount:", total_save_car_amount)
    # print("Total Internet Cost:", total_internet_cost)
    # print("Total Call Cost:", total_call_cost)
    # print("Total Food Cost:", total_food_cost)
        # Return all calculated values as a tuple
    return (
        total_eat_out_cost,
        total_alcohol_cost,
        total_coffee_cost,
        total_smoke_cost,
        total_travel_cost,
        total_leisure_cost,
        total_education_cost,
        total_save_house_amount,
        total_rent,
        total_amenities_cost,
        total_save_car_amount,
        total_internet_cost,
        total_call_cost,
        total_food_cost,
        total_cost,
    )
    # return total_cost



    
def backtrack_values(original_value_2022, json_file, country):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            inflation_data = None
            for entry in data:
                if entry['country'] == country:
                    inflation_data = entry
                    break
            
            if not inflation_data:
                raise ValueError(f"Inflation rates data not found for {country} in the JSON file")

        backtracked_values = [original_value_2022]

        for i in range(2022, 2000, -1):
            backtracked_values.append(backtracked_values[-1] / (1 + inflation_data[str(i)] / 100))

        return {year: value for year, value in zip(range(2022, 1999, -1), backtracked_values)}

    except Exception as e:
        print("Error calculating backtracked values:", str(e))
        return None
