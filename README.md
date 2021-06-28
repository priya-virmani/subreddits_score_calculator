# Top 50 Trending Subreddits Score Calculator

This Project is calculating the Top 50 trending subreddits score and this score is based on the total score of top 10 posts for each subreddits.
The total score of all the 10 posts is based on the 5 higher scoring comments for each post.

Steps to run the code:

1. Clone the repository.
2. Create an account on Reddit to use its API.
3. Create a new app on Reddit to generate CLIENT_ID and SECRET_TOKEN.
4. Use the generated CLIENT_ID, SECRET_TOKEN, Username and Password to authorize the Reddit API.
5. Use below Docker commands to run the code:
   Build: docker build -t subreddits_score_calculator .
   Run:   docker run subreddits_score_calculator
6. A csv file gets created with top trending subreddits with their scores in real-time.
