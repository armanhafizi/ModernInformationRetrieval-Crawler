# Web Crawler using Selenium in Python
## Introduction
In this project, a web crawler on [Microsoft Academic](https://academic.microsoft.com/home) papers using both Chrome and Firefox drivers is implemented in Python. The starter queue of webpages is saved in *start.txt*. The result database gets saved in *database.json* depending on the driver you use. A Jupyter Notebook version is also implemented to run in Google Colab environment.

## Software Install and Setup
- Python 3
- Selenium (Install this package using ```$ pip install selenium```)
- Firefox and Chrome Web Drivers

## Local Run

**Step 1.** Make sure [Microsoft Academic](https://academic.microsoft.com/home) is accessible.

**Step 2.** Create a folder named *Drivers* and put the web drivers in.

**Step 3.** Run the program using either ```python Crawler-Chrome.py LIMIT``` or ```python Crawler-Chrome.py LIMIT```.

## Google Colab Run

**Step 1.** Upload *Crawler-Google Colab.ipynb* and *start.txt* to your google drive.

**Step 2.** Run the notebook using a GPU. The default limit value is set to 5000. Change it to your desirable value in the last cell.


*Feel free to contact me for more information*
