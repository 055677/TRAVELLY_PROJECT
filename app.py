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

# Function to generate recommendations for a new user
def generate_recommendations(new_user_ratings):
    new_user_cluster = kmeans.predict([new_user_ratings])[0]
    cluster_city_ids = user_preferences[user_preferences['Cluster'] == new_user_cluster]['City_ID'].unique()
    recommended_cities = cities_df[cities_df['City_ID'].isin(cluster_city_ids)]['City'].tolist()
    return random.choice(recommended_cities)

# Function to calculate average cost
def calculate_average_cost(vacation_type, num_children, num_days, city_id):
    budget_info = budget_data[budget_data['City_ID'] == city_id].iloc[0]
    if vacation_type == 'solo':
        average_cost = budget_info['Solo_Budget'] * num_days
    elif vacation_type == 'couple':
        average_cost = budget_info['Couple_Budget'] * num_days
    elif vacation_type == 'family':
        child_budget = budget_info['Child_Budget'] * num_children
        average_cost = (budget_info['Couple_Budget'] + child_budget) * num_days
    return average_cost

# Function to print city information, including the country
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

    # Restaurant information
    print(f"\nRestaurant in {city_name}:")
    if vacation_type == 'family':
        print(restaurant_data[restaurant_data['City'] == city_name]['fam_rest'].to_string(index=False))

    # Places to visit
    print("\nPlaces to Visit in", city_name)
    for category in ['Cultural_place', 'Historical_place', 'Adventure_place', 'City_place', 'Relax_place', 'Extreme_place']:
        print(f"\n{category.replace('_', ' ').title()}:")
        print(places_to_visit_data[places_to_visit_data['City'] == city_name][category].to_string(index=False))

# Ask user to input vacation type first
vacation_type = input("Enter your vacation type (solo/family/couple): ")
num_days = int(input("How many days are you planning to spend? "))

# Handle family case
num_children = 0
if vacation_type.lower() == 'family':
    num_children = int(input("How many children are traveling with you? "))

# Get user ratings for each category
categories = ['Gyms', 'Local_Services', 'Monuments', 'Museums', 'Parks', 'Restaurants', 'Swimming_Pools', 'Theatres', 'View_Points']
new_user_ratings = []

for category in categories:
    while True:
        try:
            rating = float(input(f"Enter your rating for {category.replace('_', ' ')} (0-5): "))
            if 0 <= rating <= 5:
                new_user_ratings.append(rating)
                break  # Exit the loop if the rating is valid
            else:
                print("Rating must be between 0 and 5. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 5.")

# Recommend a random city based on new user preferences
recommended_city = generate_recommendations(new_user_ratings)

# Get the City ID for further calculations
city_id = cities_df.loc[cities_df['City'] == recommended_city, 'City_ID'].values[0]

# Calculate the average cost
average_cost = calculate_average_cost(vacation_type.lower(), num_children, num_days, city_id)

# Display recommended city name and print its information
print("\nRecommended City:")
print(recommended_city)
print_city_information(recommended_city, vacation_type.lower())

# Print the average cost of the trip
print(f"\nEstimated average cost for your trip: ${average_cost:.2f}")
