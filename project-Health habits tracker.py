import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Load food data
food_data = pd.read_csv('FOOD_DES.csv', encoding='utf-8')
nutrient_data = pd.read_csv('NUTR_DEF.csv', encoding='utf-8')
lang_desc_data = pd.read_csv('LANGDESC.csv', encoding='utf-8')
langual_data = pd.read_csv('LANGUAL.csv', encoding='utf-8')
nut_data = pd.read_csv('NUT_DATA.csv', encoding='utf-8', low_memory=False)

# Connect food names and nutrient information
merged_data = pd.merge(langual_data, lang_desc_data, left_on='Factor', right_on='Factor', how='inner')
merged_data = pd.merge(merged_data, food_data, left_on='NDB_No', right_on='NDB_No', how='inner')
merged_data = pd.merge(merged_data, nut_data, left_on='NDB_No', right_on='NDB_No', how='inner')
merged_data = pd.merge(merged_data, nutrient_data, left_on='Nutr_No', right_on='Nutr_No', how='inner')


# Create a HealthTrackerApp class
class HealthTrackerApp:
    def __init__(self, main_window):
        """Initialize the main window and the tabbed sections"""
        self.main_window = main_window
        self.main_window.title("Health Habits Tracker")
        self.main_window.geometry("800x600")

        self.notebook = ttk.Notebook(self.main_window)
        self.notebook.pack(fill="both", expand=1)

        self.create_food_tab()
        self.create_calorie_tab()
        self.create_sleep_tab()
        self.sleep_durations = []
        self.start_entries = []
        self.end_entries = []

    def create_food_tab(self):
        """Create the 'Food Tracking' tab."""
        food_tab = ttk.Frame(self.notebook)
        self.notebook.add(food_tab, text="Food Tracker")

        food_entries = []
        quantity_entries = []

        def add_food_entry():
            """Add a new food entry to the 'Food Tracking' tab."""
            entry_frame = tk.Frame(food_tab)
            entry_frame.pack(padx=10, pady=(10, 0))

            food_label = tk.Label(entry_frame, text="Food:")
            food_label.pack(side='left')

            food_entry = tk.Entry(entry_frame)
            food_entry.pack(side='left', padx=(10, 0))

            quantity_label = tk.Label(entry_frame, text="Quantity(g):")
            quantity_label.pack(side='left', padx=(10, 0))

            quantity_entry = tk.Entry(entry_frame)
            quantity_entry.pack(side='left')

            food_entries.append(food_entry)
            quantity_entries.append(quantity_entry)

        def show_food_nutrition():
            """Display nutrition information for the entered food in the 'Food Tracking' tab."""
            total_nutrition = {}

            for i in range(len(food_entries)):
                food = food_entries[i].get()
                quantity_value = quantity_entries[i].get()

                if quantity_value:
                    try:
                        quantity = float(quantity_value)
                    except ValueError:
                        print("The entered quantity is invalid. ")
                        continue
                else:
                    print("The entered quantity cannot be empty. ")
                    continue

                selected_food = merged_data[merged_data['Description'].str.lower().str.contains(food.lower())]
                selected_nutrients = selected_food[selected_food['Nutr_Val'] > 0]['NutrDesc'].unique()

                # Calculate nutrition information for entered foods and quantities
                nutrition = {}
                for nutrient in selected_nutrients:
                    nutr_data = selected_food[selected_food['NutrDesc'] == nutrient]
                    nutr_value = nutr_data['Nutr_Val'].values[0] * quantity / 100
                    nutrition[nutrient] = nutr_value

                for nutrient, value in nutrition.items():
                    if nutrient in total_nutrition:
                        total_nutrition[nutrient] += value
                    else:
                        total_nutrition[nutrient] = value

            plot_nutrition(total_nutrition)

        # Button to add a food entry and show food nutrition
        food_nutrition_button = tk.Button(food_tab, text="Show Food Nutrition", command=show_food_nutrition)
        food_nutrition_button.pack(side='top', padx=10, pady=10)

        add_food_button = tk.Button(food_tab, text="Add Food", command=add_food_entry)
        add_food_button.pack(side='top', padx=10, pady=10)

        # Define a function to plot nutrition
        def plot_nutrition(nutrition_data):
            """Define a function to plot nutrition."""
            nutrients = list(nutrition_data.keys())
            values = nutrition_data.values()

            plt.figure(figsize=(8, 6))
            plt.bar(nutrients, values)
            plt.xlabel('Nutrient')
            plt.ylabel('Amount (g/mg)')
            plt.title('Nutrition Information')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()

    def create_calorie_tab(self):
        """Create the 'Calorie Tracking' tab."""
        calorie_tab = ttk.Frame(self.notebook)
        self.notebook.add(calorie_tab, text="Calorie Tracker")

        sex_label = tk.Label(calorie_tab, text="Sex (male/female):")
        sex_label.pack()
        sex_entry = tk.Entry(calorie_tab)
        sex_entry.pack()

        weight_label = tk.Label(calorie_tab, text="Weight (kg):")
        weight_label.pack()
        weight_entry = tk.Entry(calorie_tab)
        weight_entry.pack()

        height_label = tk.Label(calorie_tab, text="Height (cm):")
        height_label.pack()
        height_entry = tk.Entry(calorie_tab)
        height_entry.pack()

        age_label = tk.Label(calorie_tab, text="Age:")
        age_label.pack()
        age_entry = tk.Entry(calorie_tab)
        age_entry.pack()

        activity_level_label = tk.Label(
            calorie_tab,
            text=("activity_level (1- Sedentary, 2- Lightly active, 3- Moderately active, "
                  "4- Very active, 5- Super active):")
        )
        activity_level_label.pack()
        activity_level_entry = tk.Entry(calorie_tab)
        activity_level_entry.pack()

        result_label = tk.Label(calorie_tab, text="")
        result_label.pack()

        # Define a function to calculate calories
        def calculate_calories(sex, weight, height, age, activity_level):
            """Define a function to calculate calories."""
            if sex.lower() == "male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            elif sex.lower() == "female":
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            else:
                return "Please enter 'male' or 'female'."

            activity_factors = [1.2, 1.375, 1.55, 1.725, 1.9]
            if 1 <= activity_level <= 5:
                calories = bmr * activity_factors[activity_level - 1]
                return f"Estimated daily calorie consumption: {calories:.2f} kcal"
            else:
                return "Please enter the activity level(1-5)."

        def calculate_calorie_data():
            """Calculate calorie data based on user input"""
            sex = sex_entry.get()
            weight = float(weight_entry.get()) if weight_entry.get() else 0
            height = float(height_entry.get()) if height_entry.get() else 0
            age = float(age_entry.get()) if age_entry.get() else 0
            activity_level = int(activity_level_entry.get()) if activity_level_entry.get() else 0
            result = calculate_calories(sex, weight, height, age, activity_level)
            result_label.config(text=result)

        calculate_button = tk.Button(calorie_tab, text="Count Calories Burned", command=calculate_calorie_data)
        calculate_button.pack()

    def create_sleep_tab(self):
        """Create the 'Sleep Tracker' tab."""
        sleep_tab = ttk.Frame(self.notebook)
        self.notebook.add(sleep_tab, text="Sleep Tracker")

        # Function to calculate average sleep duration
        def calculate_sleep_duration():
            """Calculate and display average sleep duration."""
            total_duration = timedelta()
            num_entries = len(self.start_entries)

            sleep_durations = []

            for i in range(num_entries):
                start_time_str = self.start_entries[i].get()
                end_time_str = self.end_entries[i].get()

                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')

                    if end_time < start_time:
                        end_time += timedelta(days=1)

                    duration = end_time - start_time
                    total_duration += duration
                    sleep_durations.append(duration)
                except ValueError:
                    print(f"Invalid time format in entry {i + 1}")

            if num_entries > 0:
                average_duration = total_duration / num_entries

                # Calculate and display average sleep duration
                average_hours, average_minutes = divmod(int(average_duration.total_seconds() / 60), 60)
                total_duration_label.config(text=f"Average Sleep Duration: {average_hours:02d}:{average_minutes:02d}")

                print("Individual Sleep Durations:")
                for i, duration in enumerate(sleep_durations, start=1):
                    hours, minutes = divmod(int(duration.total_seconds() / 60), 60)
                    print(f"Entry {i}: {hours:02d}:{minutes:02d}")
            else:
                total_duration_label.config(text="No valid entries to calculate the average.")

        # Function to add a new entry for sleep times
        def add_sleep_entry():
            """Add a new entry for sleep times."""
            entry_frame = tk.Frame(sleep_tab)
            entry_frame.pack(padx=10, pady=(10, 0))

            start_label = tk.Label(entry_frame, text="Start Time (YYYY-MM-DD HH:MM):")
            start_label.pack(side='left')

            start_entry = tk.Entry(entry_frame)
            start_entry.pack(side='left', padx=(10, 0))

            end_label = tk.Label(entry_frame, text="End Time (YYYY-MM-DD HH:MM):")
            end_label.pack(side='left', padx=(10, 0))

            end_entry = tk.Entry(entry_frame)
            end_entry.pack(side='left')

            self.start_entries.append(start_entry)
            self.end_entries.append(end_entry)

        # Function to plot sleep durations
        def plot_sleep_durations():
            """Plot sleep durations."""
            sleep_durations = []

            for i in range(len(self.start_entries)):
                start_time_str = self.start_entries[i].get()
                end_time_str = self.end_entries[i].get()

                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
                    duration = end_time - start_time
                    sleep_durations.append(duration.total_seconds() / 3600)
                except ValueError:
                    print(f"Invalid time format in entry {i + 1}")

            if sleep_durations:
                start_times = [entry.get().split(' ')[0] for entry in self.start_entries]

                # Create a plot for sleep durations
                plt.figure(figsize=(8, 6))
                plt.plot(start_times, sleep_durations, marker='o')
                plt.xlabel('Start Time')
                plt.ylabel('Sleep Duration (hours)')
                plt.title('Sleep Duration Over Time')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Add red horizontal lines at y-values 7 and 9
                plt.axhline(y=7, color='red', linestyle='--', label='7 hours')
                plt.axhline(y=9, color='red', linestyle='--', label='9 hours')

                plt.legend()
                plt.show()

        total_duration_label = tk.Label(sleep_tab, text="")
        total_duration_label.pack()

        calculate_duration_button = tk.Button(
            sleep_tab,
            text="Calculate Sleep Duration",
            command=calculate_sleep_duration
        )
        calculate_duration_button.pack()

        # Buttons to add a new sleep entry and plot sleep durations
        add_entry_button = tk.Button(sleep_tab, text="Add Sleep Entry", command=add_sleep_entry)
        add_entry_button.pack()

        plot_button = tk.Button(sleep_tab, text="Plot Sleep Durations", command=plot_sleep_durations)
        plot_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTrackerApp(root)
    root.mainloop()
