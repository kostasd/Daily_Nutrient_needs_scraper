"""
Created on 02May20

Script: human_nutrient_needs_scraper.py

Description: A scraper for data gathering from nutritiondata.self.com for the minimum daily nutrient needs,
based of the Dietary Reference Intakes (DRI)

Usage: python human_nutrient_needs_scraper.py

@author: Kostas
"""

# import the necessary packages
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import progressbar as pb
import argparse
import pandas as pd
import os

# Define the arguments for this script
# TO-DO: Add more arguments if necessary
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Modify output verbosity', action='store_true')
args = vars(parser.parse_args())
verbose = args['verbose']


# Define progress timer class
class ProgressTimer:

    def __init__(self, n_iter, description="Nutrient recommendation scraper"):
        self.n_iter = n_iter
        self.iter = 0
        self.description = description + ':'
        self.timer = None
        self.initialize()

    def initialize(self):
        # Initialize Timer
        widgets = [self.description, pb.Percentage(), '', pb.Bar(marker=pb.RotatingMarker()), '', pb.ETA()]
        self.timer = pb.ProgressBar(widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        # Update Timer
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        # End Timer
        self.timer.finish()


# Define the url
url = 'https://nutritiondata.self.com/'

# Initializing the webdriver
options = webdriver.ChromeOptions()

# Initialize the Chrome webdriver and open the URL in a new window
driver = webdriver.Chrome(options=options)
driver.set_window_size(1120, 1000)
driver.get(url)

# Initialize the list that will contain the dictionary that will be used to generate the dataset
human_nutrients = []

# Let the page load.
# # TO-DO: Change this number based on your internet speed.
time.sleep(5)

# TO-DO: Setup the range and step for the weight
weight_start = 20
weight_end = 120
weight_step = 0.5
initial_weights = [x * weight_step for x in
                   range((weight_start * int(1 / weight_step)), (weight_end * int(1 / weight_step))
                         + 1)]
weights = ['%.1f' % elem for elem in initial_weights]

# TO-DO: Setup the range for the age
age_start = 6
age_end = 70
ages = list(range(age_start, age_end + 1))

# Create a list of the available genders, heights, lifestyles
genders = []
genders_select = driver.find_element_by_name("sex")
genders_buttons = genders_select.find_elements_by_tag_name("option")
for gender in genders_buttons:
    genders.append(gender.text)

heights = []
heights_select = driver.find_element_by_name("height")
heights_button = heights_select.find_elements_by_tag_name("option")
for height in heights_button:
    heights.append(height.text)

lifestyles = []
lifestyles_select = driver.find_element_by_name("lifestyleIndex")
lifestyles_button = lifestyles_select.find_elements_by_tag_name("option")
for lifestyle in lifestyles_button:
    lifestyles.append(lifestyle.text)

# Calculate the number of iterations
iterations = len(weights) * len(ages) * len(genders) * len(heights) * len(lifestyles)
print('\n')
print("Total unique weights that will be processed: " + str(len(weights)))
print("Total unique ages that will be processed: " + str(len(ages)))
print("Total unique genders that will be processed: " + str(len(genders)))
print("Total unique heights that will be processed: " + str(len(heights)))
print("Total unique lifestyles that will be processed: " + str(len(lifestyles)))
print("Total number of iterations: " + str(iterations))

# Initialize Timer
pt = ProgressTimer(description='Nutrient recommendation scraper progress', n_iter=iterations)

for age in ages:
    for gender in genders:
        for height in heights:
            for lifestyle in lifestyles:
                for weight in weights:

                    # Update Timer
                    pt.update()

                    # Output the values of the current iteration
                    print('\n')
                    print("Age set to:" + str(age))
                    print("Gender set to:" + gender)
                    print("Height set to:" + height)
                    print("Lifestyle set to:" + lifestyle)
                    print("Weight set to:" + str(weight))

                    # Click on the dropdown menus and select the corresponding value
                    select_gender = Select(driver.find_element_by_name("sex"))
                    select_height = Select(driver.find_element_by_name("height"))
                    select_lifestyle = Select(driver.find_element_by_name("lifestyleIndex"))

                    select_gender.select_by_visible_text(gender)
                    select_height.select_by_visible_text(height)
                    select_lifestyle.select_by_visible_text(lifestyle)

                    # Set the weight metric to Kilograms
                    select_weight = Select(driver.find_element_by_name("weightUnit"))
                    select_weight.select_by_value("kg")

                    # Set age and weight in the corresponding boxes
                    input_age = driver.find_element_by_name("age")
                    input_age.send_keys(age)

                    input_weight = driver.find_element_by_name("weight")
                    input_weight.send_keys(weight)

                    # Click on Calculate
                    button = driver.find_element_by_xpath("//input[@value='Calculate']")
                    driver.execute_script("arguments[0].click();", button)

                    # TO-DO: Setup the time to wait based on your internet speed
                    time.sleep(3)

                    # On the next page get the information of interest
                    try:
                        total_carbo = driver.find_element_by_name("dailyValueCommand.nutrients['Total Carbohydrate']")\
                            .get_attribute('value')
                    except NoSuchElementException:
                        total_carbo = -1
                        if verbose:
                            print("[WARN] Total Carbohydrate was not found. Value set to default: -1")

                    try:
                        dietary_fiber = driver.find_element_by_name("dailyValueCommand.nutrients['Dietary Fiber']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        dietary_fiber = -1
                        if verbose:
                            print("[WARN] Dietary Fiber was not found. Value set to default: -1")

                    try:
                        lino_acid = driver.find_element_by_name("dailyValueCommand.nutrients['Linoleic Acid']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        lino_acid = -1
                        if verbose:
                            print("[WARN] Linoleic Acid was not found. Value set to default: -1")

                    try:
                        alpha_lino_acid = driver.find_element_by_name("dailyValueCommand.nutrients["
                                                                      "'Alpha-Linolenic Acid']").get_attribute('value')
                    except NoSuchElementException:
                        alpha_lino_acid = -1
                        if verbose:
                            print("[WARN] Alpha-Linolenic Acid was not found. Value set to default: -1")

                    try:
                        protein = driver.find_element_by_name("dailyValueCommand.nutrients['Protein']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        protein = -1
                        if verbose:
                            print("[WARN] Protein was not found. Value set to default: -1")

                    try:
                        vit_a = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin A']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_a = -1
                        if verbose:
                            print("[WARN] Vitamin A was not found. Value set to default: -1")

                    try:
                        vit_c = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin C']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_c = -1
                        if verbose:
                            print("[WARN] Vitamin C was not found. Value set to default: -1")

                    try:
                        vit_d = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin D']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_d = -1
                        if verbose:
                            print("[WARN] Vitamin D was not found. Value set to default: -1")

                    try:
                        vit_e = driver.find_element_by_name("dailyValueCommand.nutrients["
                                                            "'Vitamin E (Alpha Tocopherol)']").get_attribute('value')
                    except NoSuchElementException:
                        vit_e = -1
                        if verbose:
                            print("[WARN] Vitamin E was not found. Value set to default: -1")

                    try:
                        vit_k = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin K']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_k = -1
                        if verbose:
                            print("[WARN] Vitamin K was not found. Value set to default: -1")

                    try:
                        thiamin = driver.find_element_by_name("dailyValueCommand.nutrients['Thiamin']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        thiamin = -1
                        if verbose:
                            print("[WARN] Thiamin was not found. Value set to default: -1")

                    try:
                        riboflavin = driver.find_element_by_name("dailyValueCommand.nutrients['Riboflavin']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        riboflavin = -1
                        if verbose:
                            print("[WARN] Riboflavin was not found. Value set to default: -1")

                    try:
                        niacin = driver.find_element_by_name("dailyValueCommand.nutrients['Niacin']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        niacin = -1
                        if verbose:
                            print("[WARN] Niacin was not found. Value set to default: -1")

                    try:
                        vit_b6 = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin B6']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_b6 = -1
                        if verbose:
                            print("[WARN] Vitamin B6 was not found. Value set to default: -1")

                    try:
                        folate = driver.find_element_by_name("dailyValueCommand.nutrients['Folate']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        folate = -1
                        if verbose:
                            print("[WARN] Folate was not found. Value set to default: -1")

                    try:
                        vit_b12 = driver.find_element_by_name("dailyValueCommand.nutrients['Vitamin B12']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        vit_b12 = -1
                        if verbose:
                            print("[WARN] Vitamin B12 was not found. Value set to default: -1")

                    try:
                        pan_acid = driver.find_element_by_name("dailyValueCommand.nutrients['Pantothenic Acid']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        pan_acid = -1
                        if verbose:
                            print("[WARN] Pantothenic Acid was not found. Value set to default: -1")

                    try:
                        biotin = driver.find_element_by_name("dailyValueCommand.nutrients['Biotin']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        biotin = -1
                        if verbose:
                            print("[WARN] Biotin was not found. Value set to default: -1")

                    try:
                        choline = driver.find_element_by_name("dailyValueCommand.nutrients['Choline']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        choline = -1
                        if verbose:
                            print("[WARN] Choline was not found. Value set to default: -1")

                    try:
                        calcium = driver.find_element_by_name("dailyValueCommand.nutrients['Calcium']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        calcium = -1
                        if verbose:
                            print("[WARN] Calcium was not found. Value set to default: -1")

                    try:
                        chromium = driver.find_element_by_name("dailyValueCommand.nutrients['Chromium']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        chromium = -1
                        if verbose:
                            print("[WARN] Chromium was not found. Value set to default: -1")

                    try:
                        copper = driver.find_element_by_name("dailyValueCommand.nutrients['Copper']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        copper = -1
                        if verbose:
                            print("[WARN] Copper was not found. Value set to default: -1")

                    try:
                        flouride = driver.find_element_by_name("dailyValueCommand.nutrients['Flouride']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        flouride = -1
                        if verbose:
                            print("[WARN] Flouride was not found. Value set to default: -1")

                    try:
                        iodine = driver.find_element_by_name("dailyValueCommand.nutrients['Iodine']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        iodine = -1
                        if verbose:
                            print("[WARN] Iodine was not found. Value set to default: -1")

                    try:
                        iron = driver.find_element_by_name("dailyValueCommand.nutrients['Iron']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        iron = -1
                        if verbose:
                            print("[WARN] Iron was not found. Value set to default: -1")

                    try:
                        magnesium = driver.find_element_by_name("dailyValueCommand.nutrients['Magnesium']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        magnesium = -1
                        if verbose:
                            print("[WARN] Magnesium was not found. Value set to default: -1")

                    try:
                        manganese = driver.find_element_by_name("dailyValueCommand.nutrients['Manganese']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        manganese = -1
                        if verbose:
                            print("[WARN] Manganese was not found. Value set to default: -1")

                    try:
                        moly = driver.find_element_by_name("dailyValueCommand.nutrients['Molybdenum']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        moly = -1
                        if verbose:
                            print("[WARN] Molybdenum was not found. Value set to default: -1")

                    try:
                        phosphorus = driver.find_element_by_name("dailyValueCommand.nutrients['Phosphorus']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        phosphorus = -1
                        if verbose:
                            print("[WARN] Phosphorus was not found. Value set to default: -1")

                    try:
                        selen = driver.find_element_by_name("dailyValueCommand.nutrients['Selenium']"). \
                            get_attribute('value')
                    except NoSuchElementException:
                        selen = -1
                        if verbose:
                            print("[WARN] Selenium was not found. Value set to default: -1")

                    try:
                        zinc = driver.find_element_by_name("dailyValueCommand.nutrients['Zinc']").get_attribute('value')
                    except NoSuchElementException:
                        zinc = -1
                        if verbose:
                            print("[WARN] Zinc was not found. Value set to default: -1")

                    # Printing for debugging
                    if verbose:
                        print("[INFO] Total Carbohydrate: {}".format(total_carbo))
                        print("[INFO] Dietary Fiber: {}".format(dietary_fiber))
                        print("[INFO] Linoleic Acid: {}".format(lino_acid))
                        print("[INFO] Alpha-Linolenic Acid: {}".format(alpha_lino_acid))
                        print("[INFO] Protein: {}".format(protein))
                        print("[INFO] Vitamin A: {}".format(vit_a))
                        print("[INFO] Vitamin C: {}".format(vit_c))
                        print("[INFO] Vitamin D: {}".format(vit_d))
                        print("[INFO] Vitamin E: {}".format(vit_e))
                        print("[INFO] Vitamin K: {}".format(vit_k))
                        print("[INFO] Thiamin: {}".format(thiamin))
                        print("[INFO] Riboflavin: {}".format(riboflavin))
                        print("[INFO] Niacin: {}".format(niacin))
                        print("[INFO] Vitamin B6: {}".format(vit_b6))
                        print("[INFO] Folate: {}".format(folate))
                        print("[INFO] Vitamin B12: {}".format(vit_b12))
                        print("[INFO] Pantothenic Acid: {}".format(pan_acid))
                        print("[INFO] Biotin: {}".format(biotin))
                        print("[INFO] Choline: {}".format(choline))
                        print("[INFO] Calcium: {}".format(calcium))
                        print("[INFO] Chromium: {}".format(chromium))
                        print("[INFO] Copper: {}".format(copper))
                        print("[INFO] Flouride: {}".format(flouride))
                        print("[INFO] Iodine: {}".format(iodine))
                        print("[INFO] Iron: {}".format(iron))
                        print("[INFO] Magnesium: {}".format(magnesium))
                        print("[INFO] Manganese: {}".format(manganese))
                        print("[INFO] Molybdenum: {}".format(moly))
                        print("[INFO] Phosphorus: {}".format(phosphorus))
                        print("[INFO] Selenium: {}".format(selen))
                        print("[INFO] Zinc: {}".format(zinc))
                        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                    # Add nutrients need in dictionary
                    human_nutrients.append({"Gender": gender,
                                            "Age": age,
                                            "Height": height,
                                            "Weight": weight,
                                            "Lifestyle": lifestyle,
                                            "Total Carbohydrate": total_carbo,
                                            "Dietary Fiber": dietary_fiber,
                                            "Linoleic Acid": lino_acid,
                                            "Alpha-Lonolenic Acide": alpha_lino_acid,
                                            "Protein": protein,
                                            "Vitamin A": vit_a,
                                            "Vitamin C": vit_c,
                                            "Vitamin D": vit_d,
                                            "Vitamin E": vit_e,
                                            "Vitamin K": vit_k,
                                            "Thiamin": thiamin,
                                            "Riboflavin": riboflavin,
                                            "Niacin": niacin,
                                            "Vitamin B6": vit_b6,
                                            "Folate": folate,
                                            "Vitamin B12": vit_b12,
                                            "Pantothenic Acid": pan_acid,
                                            "Biotin": biotin,
                                            "Choline": choline,
                                            "Calcium": calcium,
                                            "Chromium": chromium,
                                            "Copper": copper,
                                            "Flouride": flouride,
                                            "Iodine": iodine,
                                            "Iron": iron,
                                            "Magnesium": magnesium,
                                            "Manganese": manganese,
                                            "Molybdenum": moly,
                                            "Phosphorus": phosphorus,
                                            "Selenium": selen,
                                            "Zinc": zinc})

                    # Go to the previous page, so the process can be repeated
                    # TO-DO: Setup the wait time based on your internet speed
                    driver.back()
                    time.sleep(3)

                    # Clear previous values for age and weight
                    clear_age = driver.find_element_by_name("age")
                    clear_age.clear()

                    clear_weight = driver.find_element_by_name("weight")
                    clear_weight.clear()

# Finish Timer
pt.finish()

# Close browser
driver.quit()

# Convert the dictionary object into a Pandas DataFrame
df = pd.DataFrame(human_nutrients)

# Create the directory, where the csv file will be saved, after checking if it already exists or not
dir_name = 'Human_nutrients'
if not os.path.exists(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print("[INFO] Creation of the directory {} failed".format(os.path.abspath(dir_name)))
    else:
        print("[INFO] Successfully created the directory {} ".format(os.path.abspath(dir_name)))

# Save the DataFrame as a csv file
filename = "{}/{}.csv".format(dir_name, 'human_daily_nutrient_needs')
df.to_csv(filename, index=False, encoding='utf-8')
print("[INFO] Successfully created the file {}.csv with {} records".format('human_daily_nutrient_needs', iterations))
