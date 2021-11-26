# comment-sentiment-analyzer

# Youtube Comments Analyzer
### Youtube comments topics modeling and sentiment analyzer
Youtube Comments Analyzer is a Python scripted tool to collect and analyze Youtube's videos comments (in Arabic). Tool provides the service of sentiment analysis and topics modeling based on arguments submitted by user. All fetched comments are saved in a MongoDB named "yt" inside a collection named "comments".

Sentiment analyzer is being trained using 1000 positive-labeled and another 1000 negative-labeled tweets with accuracy of ~88% based on 80% training and 20% test sets. Accuracy may found lower with text and comments analysis as a result of dialect phrases.

## Table of contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Web Endpoint](#web-endpoint)
- [Validation](#validation)



## Requirements
- many_stop_words==0.2.2
- httplib2==0.11.3
- gensim==3.4.0
- Flask==1.0.2 (For web endpoint only)
- nltk==3.2.5
- google_api_python_client==1.6.7

## Usage
*Usage: analyze.py Tool Arg1 Arg2

*Tool: 'topics' or 'sentiment'

*Arg1: topics=>Quantity of topics, sentiment=>'video' or 'text'

*Arg2: topics=>Videos IDs seperated by commas(,), sentiment=>Video ID or Text

- Comments Topics Modeling (Supports multiple videos)
```bash
python3 analyze.py topics <number of topics> <Youtube videos IDs separated by commas(,)>
```
- Comments Sentiment Analysis (Single video)
```bash
python3 analyze.py sentiment video <Youtube video ID>
```
- Text Sentiment Analysis
```bash
python3 analyze.py sentiment text '<Your text>'
```
- Sentiment Scores (Accuracy and F-Measure)
```bash
python3 analyze.py sentiment scores
```
- Text Sentiment Analysis (Web Endpoint)
```bash
python3 websentiment.py
```

## Web Endpoint
You can start a web endpoint for the sentiment analyzer (text only) by running the following in your terminal:

```bash
python3 websentiment.py
```
Follow your server's IP address followd by the port number showed on terminal and submit your text. Example:
```bash
local server used : 3000
```
Example Respone:
```bash
{"Sentiment": "positive", "Text": "great Video"}
```

## Validation
While the accuracy is considered low because of dialect languages there is always a room for improvement. Therefore you can always add new positive and negative labeled data to pos.txt and neg.txt files respectively in order to improve results and cover more dialect phrases and words.

![image](https://user-images.githubusercontent.com/54684919/143523037-fa1ccd9b-f0d5-4d66-a243-b17e8231700c.png)
![image](https://user-images.githubusercontent.com/54684919/143523074-978bce94-bfc3-4f4d-aaae-3e33e132de66.png)
![image](https://user-images.githubusercontent.com/54684919/143523226-339e8c93-fb0b-41d4-8820-b61e701cccb6.png)
