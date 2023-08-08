# Project Description

## blipfuzzytest

blipfuzzytest is a tool for making Take’s Fuzzy Match API easier to use when testing. It can be used to process inputs using both endpoints of the Fuzzy Match API (“menu” and “map”, detailed below), returning the response’s parameters associated with entry data. blipfuzzytest can deal with single inputs (string), iterables (list, pd.Series, etc) and a specific form of .csv input file (detailed below).

## Fuzzy Match API Endpoints

There are two endpoints available in Fuzzy Match API, which use different formats for defining what the text input will be compared to. Both endpoints can be used in blipfuzzytest, and they are:

* **Menu:** Receives a list of menu options with or without number markings and compares a given input to the text of these options.

For example:

Both “1. Option A, 2. Option B, (...), N. Option N” and “Option A, Option B, (...), Option N” are valid and will both make it so text inputs are compared to “Option A”, then “Option B” all the way to “Option N”, as the number markings are omitted before comparison.

* **Map:** Receives a dictionary-like structure comprising Categories and their respective Elements, and compares a given input to each Categories’ Elements.

For example:

```
{
“category1” : [“element1_1”, “element1_2”, (...), “element1_N”],
“category2” : [“element2_1”, “element2_2”],
(...),
“categoryN” : [“elementN_1”, “elementN_2”, “elementN_3”]
}
```

This is a valid map and will make it so text inputs are compared to all of the Elements of each Category

## Fuzzy Methods

Some of the functions described below require a Fuzzy Method to be informed, which determines the type of comparison Fuzzy Match API makes between the input and the menus/maps given. The methods are:



* default
* ratio
* partialRatio
* tokenSet
* partialTokenSet
* tokenSort
* partialTokenSort
* tokenAbbreviation
* partialTokenAbbreviation

A full explanation of some of these methods is available [here](https://towardsdatascience.com/string-matching-with-fuzzywuzzy-e982c61f8a84).

## Testing File

Some of the functions described below require a test file to be given. This test file must be saved in the .csv extension and have the following format:


|input|expectedCategory|categories|elementsCat1|elementsCat2|...|elementsCatN|
|--|--|--|--|--|--|--|
|  |  |  |  |  |  |  |


The expected content of the file’s columns is:

* **input:** The text inputs that will be processed
<br>
* **expectedCategory:** What is the expected/correct outcome of the fuzzy matching process. This field enables blipfuzzytest to automatically check if the expected outcome was achieved, and give this information to the user.
* * When using the “menu” endpoint, this field can be either the text of the menu option (without number markings) or the number of the option, if number markings are present in the list of menu options. (e.g. “Option B” or “2”)
* * When using the “map” endpoint, this field can be either the name of a category or the name of a specific element. (e.g. “categoryN” or “elementN_1”) Note that expecting a specific element will make it so that the identification of another element of the same category is registered as a failure.
<br>
* **categories:**
* * When using the “menu” endpoint, this field contains the menu options used for matching, separated by “, ” or “,”. (e.g. “1. Option A, 2. Option B, (...), N. Option N”)
* * When using the “map” endpoint, this field contains the categories that compose your full map, separated by “, ” or “,”. (e.g. “category1, category2, (...), categoryN”)
<br>
* **elementsCat1, (...), elementsCatN:**
* * When using the “map” endpoint, each of these columns contains the elements of one of the map’s categories, in order, separated by “, ” or “,”. (e.g. “element1_1, element1_2, (...), element1_N” in the column elementsCat1, “element2_1, element2_2”  in the column elementsCat2 and so on)
* * When using the “menu” endpoint, you must leave these fields empty.

**Note 1:** The order of the columns is important for blipfuzzytest to function, although the names are not.
**Note 2:** You can have rows configured for both the “menu” and “map” endpoints in the same testing file.

## Instancing the Class:

In order to use blipfuzzytest, you will have to instance the class, providing a Blip Botkey and an Organization ID (both str):

```
FT = blipfuzzytest("authorization key", "organization id")
```

## Functions:

**blipfuzzytest.run_onemethod_file(file_df, method, score_threshold):** using a single chosen Fuzzy Method, returns results for all inputs in a given testing file

* file_df: pd.core.frame.DataFrame
file_df is the pandas DataFrame that needs to be processed, created from the Testing File described above

* method: str
method is the Fuzzy Method to be used for processing

* score_threshold: int
score_threshold is the minimum score value that an identification must have to be considered reliable

**blipfuzzytest.run_allmethods_file(file_df, score_threshold):** using all Fuzzy Methods, returns results for all inputs in a given testing file

* file_df: pd.core.frame.DataFrame
file_df is the pandas DataFrame that needs to be processed, created from the Testing File described above

* score_threshold: int
score_threshold is the minimum score value that an identification must have to be considered reliable

**blipfuzzytest.run_onemethod_map(inputs, method, score_threshold, map):** using a single chosen Fuzzy Method, returns results for all inputs in a given iterable (using the “map” endpoint)

* inputs: list or pd.core.series.Series
inputs is the iterable containing the text inputs that need to be processed

* method: str
method is the Fuzzy Method to be used for processing

* score_threshold: int
score_threshold is the minimum score value that an identification must have to be considered reliable

* map: dict
map is the dictionary containing the categories and elements to be used for processing

**blipfuzzytest.run_allmethods_map(inputs, score_threshold, map):** using all Fuzzy Methods, returns results for all inputs in a given iterable (using the “map” endpoint)

* inputs: list or pd.core.series.Series
inputs is the iterable containing the text inputs that need to be processed

* score_threshold: int
score_threshold is the minimum score value that an identification must have to be considered reliable

* map: dict
map is the dictionary containing the categories and elements to be used for processing

**blipfuzzytest.test_onemethod_menu(menu, userInput, score, method):** using a single chosen Fuzzy Method, returns the result for a single input (using the “menu” endpoint)

* menu: list
menu is the list containing the menu options to be used for processing

* userInput: str
userInput is the input to be used for processing

* score: int
score is the minimum score value that an identification must have to be considered reliable

* method: str
method is the Fuzzy Method to be used for processing

**blipfuzzytest.test_allmethods_menu(menu, userInput, score):** using all Fuzzy Methods, returns the results for a single input (using the “menu” endpoint)

* menu: list
menu is the list containing the menu options to be used for processing

* userInput: str
userInput is the input to be used for processing

* score: int
score is the minimum score value that an identification must have to be considered reliable

**blipfuzzytest.run_onemethod_menu(menu, inputs, score, method):** using a single chosen Fuzzy Method, returns results for all inputs in a given iterable (using the “menu” endpoint)

* menu: list
menu is the list containing the menu options to be used for processing

* inputs: list or pd.core.series.Series
inputs is the iterable containing the text inputs that need to be processed

* score: int
score_threshold is the minimum score value that an identification must have to be considered reliable

* method: str
method is the Fuzzy Method to be used for processing


**blipfuzzytest.run_allmethods_menu(menu, inputs, score):** using all Fuzzy Methods, returns results for all inputs in a given iterable (using the “menu” endpoint)

* menu: list
menu is the list containing the menu options to be used for processing

* inputs: list or pd.core.series.Series
inputs is the iterable containing the text inputs that need to be processed

* score: int
score_threshold is the minimum score value that an identification must have to be considered reliable

## Installation

Use the package manager pip to install blipfuzzytest

`pip install blipfuzzytest==0.1.0`

## Usage

### Using the Testing File:
```
from blipfuzzytest.blipfuzzytest import *
import pandas as pd

testing_file_df = pd.read_csv("C:/Documents/blipfuzzytestingFile.csv")

FT = blipfuzzytest("authorization key", "organization id")

result = FT.run_onemethod_file(testing_file_df, "ratio", 0)
print(result)
```
### Using an iterable:
```
from blipfuzzytest.blipfuzzytest import *

input_list = ["input1", "input2", "input3"]

my_map = {"category1" : ["element1", "element2"], "category2" : ["element3"]}

FT = blipfuzzytest("authorization key", "organization id")

result = FT.run_allmethods_map(input_list, 0, my_map)
print(result)
```
##Authors

Caio Souza
Diogo Machado