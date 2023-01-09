import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import requests
import os
import praw


@st.cache(suppress_st_warning=True)
def get_mentioned_threads():
    url = 'http://api.pushshift.io/reddit/search/submission?q=goodnotes&subreddit=notabilityapp,evernote,onenote,notion,RoamResearch&after=45d&before=1h&sort=score'
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()

    submissions = result['data']
    
    if len(submissions) > 0:
        reddit = praw.Reddit(client_id=os.environ['reddit_client_id'], client_secret=os.environ['reddit_client_secret'], user_agent=os.environ['reddit_user_agent'])
        subreddit, created, title, content, num_comments, url = [], [], [], [], [], []

        for submission in submissions:
            comment_count = 0
            subreddit.append(submission['subreddit'])
            created.append(submission['utc_datetime_str'])
            title.append(submission['title'])
            content.append(submission['selftext'])
            url.append(submission['url'])
            
            post = reddit.submission(submission['id'])
            post.comments.replace_more(limit=None)
            comment_count += len(post.comments.list())
            num_comments.append(comment_count)

        df_result = pd.DataFrame(data={'subreddit': subreddit, 'created_utc': created, 'title': title, 'content': content, 'num_comments': num_comments, 'url': url})
    
    else:
        df_result = None

    return df_result

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data():
    df = pd.read_csv('./data/tagged_threads.csv').reset_index(drop=True)
    df = df.sort_values(by=['score'], ascending=False).reset_index(drop=True)
    return df

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_groupby_data(df):
    df['date'] = pd.to_datetime(df['created'], infer_datetime_format=True).dt.strftime('%Y-%m')
    df_gb_monthly_tag = df.groupby(by=['tag', 'date']).size().index.to_frame(index=False)
    df_gb_monthly_tag['count'] = df.groupby(by=['tag', 'date']).size().values
    return df_gb_monthly_tag

def tally_threads_by_tag(df):
    fig, ax = plt.subplots()
    for tag in df['tag'].unique():
        ax.plot(df[df['tag'] == tag]['date'], df[df['tag'] == tag]['count'], label=tag)
        ax.legend()
    plt.xticks(rotation=90)
    st.pyplot(fig)

def word_cloud(df):
    fig = plt.figure()
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(' '.join(df['submission_title']))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)

def display_threads(df):
    st.dataframe(df)


if __name__ == '__main__':
    st.set_page_config(page_title='GoodNotes Subreddit Threads Dashboard', layout='centered')
    st.title('Subreddit Threads Dashboard')

    st.header('Threads mentioning GoodNotes in other competitor subreddits')
    df_mentions = get_mentioned_threads()
    if df_mentions is None:
        st.write('No mentions found in competitors\' subreddits for the past 45 days')
    else:
        st.dataframe(df_mentions)

    df = load_data()
    tags = df['tag'].unique()
    df_monthly_tag = get_groupby_data(df)
    
    selected_tag = st.sidebar.selectbox(label='Select a Tag', options=tags)
    checkbox = st.sidebar.checkbox(label='Show Analysis by Tag', value=False)
    
    if checkbox:
        df = df[df['tag'] == selected_tag].reset_index(drop=True)
        df_monthly_tag = df_monthly_tag[df_monthly_tag['tag'] == selected_tag]
        st.header('Tag-Level Threads')
        display_threads(df)
        st.header('Tag-Level Monthly Thread Count')
        tally_threads_by_tag(df_monthly_tag)
        st.header('Tag-Level Word Cloud from Thread Titles')
        word_cloud(df)
    else:
        st.header('Threads')
        display_threads(df)
        st.header('Monthly Thread Count')
        tally_threads_by_tag(df_monthly_tag)
        st.header('Word Cloud from Thread Titles')
        word_cloud(df)
