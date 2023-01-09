# Opinion Mining from Subreddit Threads of a Note-taking Application
 
**About this project**:

This project aims to mine opinions from the Reddit threads of GoodNotes, a note-taking application available on Apple devices. ([*Disclaimer](#disclaimer))

It is divided into four parts:

- **Part 1 Data Collection**:
  - Set up a MongoDB database and registered a Reddit application for script/web access
  - Built an Extract Transform Load (ETL) pipeline that extracts data (including posts and comments) from the GoodNotes subreddit, cleans/filters the data, and saves the data into the MongoDB database
  - Extracted data from Reddit using the Python Reddit API Wrapper (PRAW) library
  - Executed some preliminary queries to the MongoDB database for simple analytics
- **Part 2 Data Exploration and Pre-processing**:
  - Performed initial exploratory data analysis
  - Pre-processed data by
    - Checking for and removing null and duplicate values
    - Removing hyperlinks and hexadecimal color codes in comments
    - Creating new columns in data frame to obtain statistical summaries about threads and comments
  - Applied common natural language processing (NLP) techniques such as tokenization, stemming, n-gram, and removal of stop words using the NLTK library
  - Visualized word cloud and top 30 n-grams (unigrams, bigrams, trigrams) in charts
  - Performed topic modeling using Latent Dirichlet Allocation (LDA) with the Gensim library and used PyLDAvis for visualizing the topics
- **Part 3 Transfer Learning with Transformers**:
  - Applied deep learning and transfer learning to predict the tag (category/flair) of a thread in GoodNotes subreddit
  - Leveraged a Transformer model that had been pretrained on a huge corpus of English text and adapted it for this specific Reddit tag prediction task
  - The Transformer model was first trained with labeled data for a single task (tag prediction), and subsequently trained for multi-tasks (tag prediction and title generation, i.e. generating the title for a given thread)
  - Multi-task learning would improve the model performance as information from training on one task may inform and accelerate learning of other different tasks
  - Due to category imbalance in the data, data augmentation was performed by upsampling particular categories of tags
  - Model training, evaluation, and versioning were tracked using Weights & Biases
  - The tuned model was pushed to HuggingFace and called to inference on unseen data, i.e. to classify unlabeled subreddit threads with different tags
- **Part 4 Dashboard**:
  - An interactive data visualization dashboard was created using Streamlit
  - Data visualization includes plot of monthly thread count per month and word cloud of thread titles
  - By choosing a specific tag from the dropdown menu, the dashboard would be updated automatically to show tag-related visualizations only
  - In addition, a data frame is placed at the top of the dashboard to show the latest (within past 45 days) threads mentioning GoodNotes in competitors' subreddits
  - This allows for continuous monitoring of Reddit for any mentions of comparison with GoodNotes
  - This was achieved using the Pushshift Reddit API and PRAW

## Demo

The Streamlit app is hosted on Streamlit Cloud. [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://goodnotes-subreddit-threads.streamlit.app) to view the data visualizations.

## How to run this project

### Run from the command line

1. Set up the environment using Conda:
```bash
conda env create -n notes-subreddit-opinion-mining -f environment.yml
```

2. Execute the Jupyter notebooks in the folders `part1*` till `part4*`.

3. Launch Streamlit:
```bash
streamlit run part4_dashboarding/app.py
```
## Disclaimer

This repository and its author are not affiliated with GoodNotes in any capacity, and all work was done using publicly available data.
