Travelly

## Overview
The Travelly is a comprehensive AI-based travel recommendation system designed to assist users in planning their trips effectively. This system provides tailored recommendations for destinations, hotels, restaurants, and activities based on individual and group preferences. It also incorporates budget calculations and mapping features to enhance user experience.

## Key Features
- **Personalized Recommendations**: Suggests destinations, accommodations, and restaurants based on user preferences and travel types (solo, family, or couple).
- **Budget Estimation**: Calculates trip budgets considering travel type, number of days, and group size (adults and children).
- **Dynamic Filtering**: Filters recommendations based on user-defined budget ranges.
- **Interactive Maps**: Integrates Google Maps for location visualization.
- **User-Friendly Interface**: Easy-to-use frontend with seamless navigation.

## File Structure
### Backend
- **`cities1.csv`**: Contains city IDs and names.
- **`country.csv`**: Maps countries to their respective cities.
- **`hotels.csv`**: Lists hotels categorized by travel type (solo, family, couple).
- **`places.csv`**: Contains categorized places such as cultural, historical, and adventure spots.
- **`restoran.csv`**: Lists restaurants categorized by travel type.
- **`budget.csv`**: Defines budget estimates for solo, couple, and child travelers per city.
- **`user_preferences1.csv`**: Tracks user preferences for various travel aspects like monuments, museums, and restaurants.

### Frontend
- **`index.html`**: Main landing page for inputting travel preferences.
- **`result.html`**: Displays travel recommendations.
- **CSS & JS Files**: Provide styling and interactivity for the web application.

## Installation
### Prerequisites
- Python 3.9+
- Git
- A code editor (e.g., Visual Studio Code)
- Virtual environment setup

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/055677/TRAVELLY_PROJECT.git
   ```

2. **Navigate to the Project Folder**:
   ```bash
   cd trip-planner-monorepo
   ```

3. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open `http://localhost:5000` in your web browser.

## Usage
1. Select your travel type (solo, family, couple).
2. Specify the number of days and budget range.
3. Input your ratings for specific preferences (e.g., restaurants, museums).
4. View personalized recommendations on the results page.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask framework)
- **Database**: CSV files (for prototype phase; can be replaced with SQL/NoSQL databases)
- **API Integration**: Google Maps API
- **Version Control**: Git and GitHub

## Future Enhancements
- Integration of live data from APIs for real-time updates.
- Advanced AI algorithms for improved recommendation accuracy.
- Mobile application version.
- Multi-language support for a global audience.

## Contributors
- Ani Matkosyan(Owner)
- Razmik Badalyan.



