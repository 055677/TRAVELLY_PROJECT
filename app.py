import pandas as pd
import random
from sklearn.cluster import KMeans
import sys  # Import sys to use sys.exit()

# Load data from CSV files
cities_df = pd.read_csv('cities1.csv')
country_data = pd.read_csv('country.csv')
restaurant_data = pd.read_csv('restoran.csv')
hotel_data = pd.read_csv('hotels.csv')
places_to_visit_data = pd.read_csv('places.csv')
user_preferences = pd.read_csv('user_preferences1.csv')
budget_data = pd.read_csv('budget.csv')  # Load your budget data

# Perform k-means clustering on the ratings
n_clusters = 20
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
user_ratings = user_preferences.iloc[:, 2:].values
user_preferences['Cluster'] = kmeans.fit_predict(user_ratings)

# Function to calculate average cost
def calculate_average_cost(vacation_type, num_children, num_days, city_id):
    budget_info = budget_data[budget_data['City_ID'] == city_id]

    if budget_info.empty:
        print(f"No budget data found for city ID {city_id}.")
        return 0  # Return 0 if no budget data is found
    
    budget_info = budget_info.iloc[0]  # Get the first row if it exists

    if vacation_type == 'solo':
        average_cost = budget_info['Solo_Budget'] * num_days
    elif vacation_type == 'couple':
        average_cost = budget_info['Couple_Budget'] * num_days
    elif vacation_type == 'family':
        child_budget = budget_info['Child_Budget'] * num_children
        average_cost = (budget_info['Couple_Budget'] + child_budget) * num_days
    else:
        print("Invalid vacation type provided.")
        return 0  # Handle unexpected vacation type

    return average_cost

# Function to print city information, including the country, hotel, restaurant, and places to visit
def print_city_information(city_name, vacation_type):
    print("\nCity:", city_name)

    # Get country name
    city_id = cities_df.loc[cities_df['City'] == city_name, 'City_ID'].values[0]
    country_name = country_data.loc[country_data['City_ID'] == city_id, 'Country_Name'].values[0] if not country_data[country_data['City_ID'] == city_id].empty else "Unknown"
    print("Country:", country_name)

    # Hotel information based on vacation type
    print(f"\nHotel in {city_name}:")
    if vacation_type == 'family':
        print(hotel_data[hotel_data['City'] == city_name]['family_hotel'].to_string(index=False))
    elif vacation_type == 'couple':
        print(hotel_data[hotel_data['City'] == city_name]['couple_hotel'].to_string(index=False))
    elif vacation_type == 'solo':
        print(hotel_data[hotel_data['City'] == city_name]['solo_hotel'].to_string(index=False))

    # Restaurant information
    print(f"\nRestaurant in {city_name}:")
    if vacation_type == 'family':
        print(restaurant_data[restaurant_data['City'] == city_name]['fam_rest'].to_string(index=False))
    elif vacation_type == 'couple':
        print(restaurant_data[restaurant_data['City'] == city_name]['couple_rest'].to_string(index=False))
    elif vacation_type == 'solo':
        print(restaurant_data[restaurant_data['City'] == city_name]['solo_rest'].to_string(index=False))

    # Places to visit
    print("\nPlaces to Visit in", city_name)
    for category in ['Cultural_place', 'Historical_place', 'Adventure_place', 'City_place', 'Relax_place', 'Extreme_place']:
        print(f"\n{category.replace('_', ' ').title()}:")
        print(places_to_visit_data[places_to_visit_data['City'] == city_name][category].to_string(index=False))

# Function to find the most similar city based on visited cities' ratings
def find_most_similar_city(visited_cities):
    # Get city IDs for the visited cities
    visited_city_ids = [cities_df.loc[cities_df['City'] == city, 'City_ID'].values[0] for city in visited_cities if city in cities_df['City'].values]

    if not visited_city_ids:
        print("No valid cities found in our dataset.")
        sys.exit()

    # Get the ratings for the visited cities
    visited_city_ratings = user_preferences[user_preferences['City_ID'].isin(visited_city_ids)]

    if visited_city_ratings.empty:
        print("No rating data found for the selected cities.")
        sys.exit()

    # Calculate the average rating profile for the visited cities
    average_ratings = visited_city_ratings.iloc[:, 2:].mean().values

    # Find the most similar city based on the average ratings
    best_match = None
    best_similarity_score = float('inf')

    for _, row in user_preferences.iterrows():
        city_id = row['City_ID']
        if city_id in visited_city_ids:
            continue  # Skip cities that the user has already visited

        city_ratings = row[2:].values
        similarity_score = sum((average_ratings - city_ratings) ** 2)

        if similarity_score < best_similarity_score:
            best_match = city_id
            best_similarity_score = similarity_score

    if best_match is not None:
        recommended_city = cities_df[cities_df['City_ID'] == best_match]['City'].values[0]
        return recommended_city
    else:
        return None

# Main user interaction
has_traveled = input("Have you ever traveled to any city? (yes/no): ").lower()

if has_traveled == 'yes':
    recommend_based_on_travel = input("Do you want me to recommend you a city based on where you have been already? (yes/no): ").lower()

    if recommend_based_on_travel == 'yes':
        visited_cities = input("Enter the cities you have visited, separated by commas: ").split(',')
        visited_cities = [city.strip() for city in visited_cities]

        vacation_type = input("Enter your vacation type (solo/family/couple): ")
        num_days = int(input("How many days are you planning to spend? "))

        num_children = 0
        if vacation_type.lower() == 'family':
            num_children = int(input("How many children are traveling with you? "))

        similar_city = find_most_similar_city(visited_cities)
        if similar_city:
            city_id = cities_df.loc[cities_df['City'] == similar_city, 'City_ID'].values[0]
            average_cost = calculate_average_cost(vacation_type.lower(), num_children, num_days, city_id)

            # Print city details
            print("\nRecommended City Details:")
            print_city_information(similar_city, vacation_type)

            if average_cost > 0:
                print(f"\nEstimated average cost for your trip: ${average_cost:.2f}")
        else:
            print("\nNo similar city found in our dataset.")
    
    else:
        # Proceed to collect ratings if the user does not want a recommendation based on past travels
        print("\nWe will help you find a city based on your preferences.")
        vacation_type = input("Enter your vacation type (solo/family/couple): ")
        num_days = int(input("How many days are you planning to spend? "))

        num_children = 0
        if vacation_type.lower() == 'family':
            num_children = int(input("How many children are traveling with you? "))

        categories = ['Gyms', 'Local_Services', 'Monuments', 'Museums', 'Parks', 'Restaurants', 'Swimming_Pools', 'Theatres', 'View_Points']
        new_user_ratings = []

        for category in categories:
            while True:
                try:
                    rating = float(input(f"Enter your rating for {category.replace('_', ' ')} (0-5): "))
                    if 0 <= rating <= 5:
                        new_user_ratings.append(rating)
                        break
                    else:
                        print("Rating must be between 0 and 5. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 5.")

        recommended_city = find_most_similar_city(visited_cities)  # Fix: You should find a city even when entering ratings directly
        city_id = cities_df.loc[cities_df['City'] == recommended_city, 'City_ID'].values[0]

        # Print city details
        print("\nRecommended City Details:")
        print_city_information(recommended_city, vacation_type)

        # Calculate and print the average cost
        average_cost = calculate_average_cost(vacation_type.lower(), num_children, num_days, city_id)

        if average_cost > 0:
            print(f"\nEstimated average cost for your trip: ${average_cost:.2f}")
