# Sentiment Analysis of Vasco da Gama Supporters

This project focuses on the sentiment analysis of Vasco da Gama supporters based on comments scraped from the website supervasco.com. The main goal is to understand how fans perceive various events and topics related to their football club. 

The project is divided into three main parts: data scraping, model building, and data analysis.
Project Structure

├── scrapper
│   ├── scrapper.py
│   ├── main.py
│   ├── pages.csv
│   └── commentaries.csv
│
├── model
│   ├── preprocessed_data/
│   ├── lexicon_test.py
│   ├── model_preprocessing.py
│   ├── model_training.py
│   └── vasco_model.sav
│
├── analysis
│   ├── analysis_en.py
│   └── top_tokens.csv
│
├── requirements.txt
│
└── README.md


## 1. Scrapper

The scrapper module is responsible for collecting comments from supervasco.com. These comments form the dataset used for training the sentiment analysis model.

## 2. Model

In the model module, the cleaned and processed data is used to train a sentiment analysis model. The steps involved include:

    model_preprocessing.py: Further processes the data to prepare it for model training.
    model_training.py: Trains various models and tunes hyperparameters. A fine-tuned SGDClassifier was chosen, achieving an 82% accuracy on test data.
    lexicon_test.py: Tests different methods searching for a better accuracy.
    vasco_model.sav: The final trained model ready for deployment.

## 3. Analysis

The analysis module takes the trained model and applies it to new data to generate insights and visualizations. This is the most critical part of the project, showcasing the value of the analysis.

### Key Insights from the Analysis

#### Positive Sentiments

![alt text](/app/analysis/plot_images/image.png)

This plot highlights the terms that fans associate with positive sentiment. For instance, terms like "Paiva (coach)", "Fans", and "Match" are seen in a positive light by the supporters.

#### Negative Sentiments

![alt text](/app/analysis/plot_images/image-1.png)

Conversely, this plot shows the terms with a negative sentiment. Interestingly, terms like "Go", "Evil", and "Botafogo (Rival Club)" evoke strong negative feelings among the fans.

#### Sentiment Over Time

![alt text](/app/analysis/plot_images/image-2.png)

This time-series plot illustrates how fan sentiment has varied over a specific period. Key events, such as a lawsuit by an ex-coach or the announcement of a new player, are annotated to show their impact on overall sentiment. The blue line represents the cumulative average sentiment, while the green line represents the model's predicted sentiment over time.

