# Top 50 Trending Subreddits Score Calculator

This Project is calculating the Top 50 trending subreddits score and this score is based on the total score of top 10 posts for each subreddits.
The total score of all the 10 posts is based on the 5 higher scoring comments for each post.

Steps to run the code:
1. Clone the repository.
2. Create an account on Reddit to use its API.
3. Create a new app on Reddit to generate CLIENT_ID and SECRET_TOKEN.
4. Install library Luigi using: 
    pip install luigi
5. Use the generated CLIENT_ID, SECRET_TOKEN, Username and Password to authorize the Reddit API.
6. Use below command to run the code:
    PYTHONPATH='.' luigi --module toptrendingsubreddits GetSubRedditsPosts --local-scheduler
7. A csv file gets created with top trending subreddits with their scores in real-time.

