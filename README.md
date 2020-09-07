# The GoFundMe Dataset

The GoFundMe dataset is part of the training data for the [CommonFrame](https://ra2.io/products) project. It is a collection of the individual fund raising campaigns available through the [GoFundMe](https://ca.gofundme.com/) website. The dataset was designed to inform machine learning technologies about effective communications and campaign strategies to maximize stakeholder objectives.

## Data Collection

The GoFundMe dataset was collected using Python web technologies and is stored in *csv* format. Each campaign category from the GoFundMe website was loaded until all active campaigns were cached. The resulting urls were then stored in a separate file, where each url representing individual campaigns was loaded onto a custom built webscraper that targeted elements relevant to the project. The resulting html object is then analyzed to return only the relevant information for the project. The resulting csv file is then stored to disk and imported as a dataframe where further data processing is conducted. The final dataset is again stored in csv format and passed on to the CommonFrame database for further annotation by researchers. This forms the initial training data for machine learning models.

## Description of Data

A total of 7077 campaigns was gathered under 18 different campaign categories. The data includes the individual titles and text description of the campaigns. Descriptive elements for individual campaigns were also included during the scrape which can be used for exploratory data analysis (i.e. EDA / descriptive statistics). 

The dollar amount for each individual donation is not itemized – just the total sum of donations per campaign. 

Please note that no attempt was made to verify the legitimacy of campaigns that were included in the dataset.

**Deactivated campaigns** were dropped from the collection.

The column `story_tokens` is a tokenized copy of the header: `c_story` (campaign descriptions). The Punkt sentence tokenizer from the Python Natural Language Toolkit was used to subset the campaign descriptions.

|Column Header|Data Type|Description|
|:---|:---|:---|
|`title`|string|The given title for the campaign as published on the GoFundMe webpage|
|`raised`|int64|Total dollar (USD) amount  raised at time of scraping. The actual value in the dataset may change depending on whether the campaign had reached it’s target amount or not.|
|`target`|int64|The published target amount for the campaign.|
|`m_campaign`|string|One of 18 categories set by GoFundMe to categorize each individual campaign.|
|`created_date`|datetime64|The date the campaign was officially launched in the GoFundMe website|
|`donors`|float64|Total number of donors for the campaign|
|`shares`|float64|Total number of social media shares for the campaign using embedded media sharing feature of the GoFundMe website|
|`followers`|float64|Total number of followers for the campaign|
|`scrape_date`|datetime64|Date of data mining|
|`c_story`|string|A text description of the campaign written by registered users.|
|`story_tokens`|list/string|Sentence tokens for c_story to break whole campaign descriptions into sentences (tokens). These tokens are then annotated individually to become part of the training data for the model.|



## Descriptive Statistics

Below is a quick summary of the different campaign categories within the dataset. The first table shows the total number of campaigns per category. The second table compares the category with the most amount raised and shows the *mean* number of donors per campaign .


|**Category**|**Number of Campaigns**|
|--------|-------------------:|
|`medical-fundraiser`|	584|
|`community-fundraiser`|	574|
|`volunteer-fundraiser`|	458|
|`emergency-fundraiser`|	450|
|`family-fundraiser`|	437|
|`faith-fundraiser`|	434|
|`education-fundraiser`|	432|
|`creative-fundraiser`|	427|
|`animal-fundraiser`|	410|
|`memorial-fundraiser`|	408|
|`sports-fundraiser`|	382|
|`event-fundraiser`|	378|
|`business-fundraiser`|	377|
|`travel-fundraiser`|	369|
|`wishes-fundraiser`|	341|
|`competition-fundraiser`|	338|
|`newlywed-fundraiser`|	191|
|`environment-fundraising`|	9|



|**m_campaign**|**donors**|**raised**|
|----------|:-----|-----:|
|`competition-fundraiser`|	63.36|	2,961,875.28|
|`newlywed-fundraiser`|	17.96|	1,395,502.04|
|`travel-fundraiser`|	64.64|	264,085.01|
|`medical-fundraiser`|	201.33|	31,943.06|
|`memorial-fundraiser`|	218.95|	28,224.20|
|`emergency-fundraiser`|	190.52|	26,020.81|
|`community-fundraiser`|	84.28|	11,660.54|
|`family-fundraiser`|	102.96|	11,300.43|
|`animal-fundraiser`|	80.82|	6,078.93|
|`education-fundraiser`|	51.66|	5,723.30|
|`volunteer-fundraiser`|	38.23|	4,385.90|
|`business-fundraiser`|	52.92|	4,384.40|
|`creative-fundraiser`|	31.04|	3,590.32|
|`sports-fundraiser`|	33.72|	3,029.88|
|`wishes-fundraiser`|	15.98|	2,111.20|
|`environment-fundraising`|	20.29|	1,760.33|
|`faith-fundraiser`|	19.70|	1,591.90|
|`event-fundraiser`|	18.05|	1,140.53|

