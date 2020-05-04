### Scraping NutritionData.com

A hands-on project that gets data for human daily nutrient needs and creates a csv file with all the information extracted.

The script uses Selenium for web scraping.

Source: [NutritionData.com](https://nutritiondata.self.com/)

---------

### Getting Started

These instructions will guide you through the process of setting up and running the script on your local machine for development and testing purposes.

#### Prerequisites

* Selenium Webdriver
* Browser: Chrome
* Python: Anaconda

#### Installing

* How to install Anaconda

   * [Installing Anaconda on Windows](https://docs.anaconda.com/anaconda/install/windows/)
   * [Installing Anaconda on Mac](https://docs.anaconda.com/anaconda/install/mac-os/)
   * [Installing Anaconda on Linux](https://docs.anaconda.com/anaconda/install/linux/)

* How to install Selenium

   Use `pip` to install selenium like this:

     `pip install selenium`

* How to get Selenium Webdriver

   * Visit [ChromeDriver-Webdriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   * Download the Chromedriver for the Chrome version you are using
      * Chrome version can be found through `Help > About Google Chrome`
   * `chromedriver` file should be stored in the location of the python script `human_nutrient_needs_scrapper.py`

**Note**: For this project, Chrome version 81.0.4044.92

----------

### How to use?

From the terminal you can execute the script `human_nutrient_needs_scraper.py`

`python human_nutrient_needs_scraper.py`

**Optional arguments**

```
-h, --help     show this help message and exit
-v, --verbose  Modify output verbosity
```

----------

### Versioning

***Version**: 0.1.0*

----------

### Next Steps

1. Modify the script to include `BeautifulSoup` to test if the script can become faster
2. Find other ways to make the script faster (i.e. parallelization)