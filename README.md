Project Overview

The Health Habit Tracker Program is designed to help users track and manage their dietary intake, calorie consumption, and sleep habits. It provides a comprehensive solution for visualizing and understanding users' health-related data through a user-friendly interface.


Technologies Used

Programming Language: Python

Key Libraries:

Tkinter (GUI Development)
pandas (Data Handling)
matplotlib (Data Visualization)

Data Source

The nutritional data used in this project was sourced from the USDA FoodData Central database:
https://fdc.nal.usda.gov/download-datasets.html

The datasets used include:

FOOD_DES.csv: Contains food description details.
NUT_DATA.csv: Contains nutritional information.
NUTR_DEF.csv: Nutrient definitions.
LANGDESC.csv: Language descriptions.
LANGUAL.csv: Food categories.
These files were processed and combined to create a unified dataset.

Key Functionalities

Food Tracking:

Users input the foods they have consumed along with the weights (in grams).
The program calculates nutritional components and displays a bar chart of nutrient values.

Calorie Tracking:

Users provide their gender, weight, height, age, and activity level.
The program calculates daily calorie expenditure to help users manage their energy balance.

Sleep Tracking:

Users input their sleep and wake times.
The program calculates average sleep duration and visualizes sleep trends.


Development Process

Data Preparation:

Imported raw data files from USDA datasets in CSV and Access formats.
Processed and merged data into a comprehensive dataset for nutritional analysis.

Function Implementation:

Implemented food nutritional calculations, calorie calculations, and sleep duration tracking.
Visualized user data using matplotlib.

Graphical User Interface:

Designed an interactive GUI using Tkinter.
Organized user input fields, buttons, and data visualization components.

Code Editor:

Developed and tested the program using PyCharm Community Edition.


File Structure

├── README.md                         # Project documentation
├── project-Health habits tracker.py  # Python code for the tracker
├── FOOD_DES.csv                      # Food description dataset
├── NUT_DATA.csv                      # Nutritional data
├── NUTR_DEF.csv                      # Nutrient definitions
├── LANGDESC.csv                      # Language descriptions
├── LANGUAL.csv                       # Food category data
├── USDA-sr28.accdb                   # USDA Access database
