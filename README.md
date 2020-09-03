# GoFundMe Dataset

The GoFundMe dataset is part of the training data for the [CommonFrame](https://ra2.io/products) project. It is a collection of the individual fund raising campaigns available through the [GoFundMe](https://www.gofundme.com/) website. The dataset was designed to inform machine learning technologies about effective communications and campaign strategies.

# Data Collection

The GoFundMe dataset was collected using Python web technologies and is stored in a csv format. Each campaign category from the GoFundMe website was loaded and the resulting urls stored. Each url representing individual campaigns was then loaded and targeted elements coded into the webscraper. The resulting html object is then analyzed to return only relevant information needed for the project. The resulting csv is passed on to the CommonFrame database for further annotation. 

# Description of Data

A total of 7077 campaigns was gathered under 18 different campaign categories. The data includes the individual titles and text description of the campaigns. Also included are descriptive elements for individual campaigns. The dollar amount for each individual donation is not itemized – just the total sum. Please note that no attempt was made to verify the legitimacy of campaigns that were included in the dataset. Deactivated campaigns were dropped from the collection.
The column ‘story_tokens’ is a tokenized copy of the header: ‘c_story’. The Punkt sentence tokenizer from the Python Natural Language Toolkit was used to subset the campaign descriptions.
