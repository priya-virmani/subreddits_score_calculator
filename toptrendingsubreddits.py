import requests
import luigi
# import tornado.web
# import tornado.ioloop
import reddit_oauth as roa


def authorize_api():
    """Authorize the Reddit API"""

    CLIENT_ID = "<CLIENT_ID"
    SECRET_TOKEN = "<SECRET_TOKEN>"
    username = "<username>"
    pwd = "<password>"

    # CLIENT_ID and SECRET_TOKEN are used to authorize
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': username,
            'password': pwd}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    return headers


class GetSubRedditsPosts(luigi.Task):
    """
    Get list of the top 10 subreddits posts
    """

    def output(self):
        return luigi.LocalTarget("topSubRedditsPosts.csv")

    def run(self):

        # fetch header after the authorization
        headers = authorize_api()

        # Get the top 50 trending subreddits and creating a list
        res = requests.get(
            "https://oauth.reddit.com/r/trendingsubreddits", headers=headers)

        top_subreddits = []
        top_subreddits = roa.get_top10_post_list(res)

        # Get the top 10 posts for each subreddit
        top_subreddits_postId = roa.get_post_ids(top_subreddits, headers)

        # Get top 5 higher scoring comments in descending order for each 10 posts
        # calculating the subreddits scores
        subreddits_with_post_scores = {}
        for subreddits, ids in top_subreddits_postId.items():
            post_scores = []
            for idx in ids:
                each_post_comm = requests.get(
                    "https://oauth.reddit.com"+subreddits+'/comments/'+idx, headers=headers, params={'sort': 'top'})
                p = 0
                score_sum = 0
                for each in each_post_comm.json()[1]['data']['children']:
                    if p < 5:
                        if 'score' in each['data']:
                            score_sum += each['data']['score']
                            p += 1
                    else:
                        break
                post_scores.append(score_sum/5)
            scores_sum = 0
            for every in post_scores:
                scores_sum += every
            subreddits_with_post_scores[subreddits] = round(
                scores_sum/(1 if len(post_scores) == 0 else len(post_scores)), 3)

        with self.output().open("w") as f:
            for key in subreddits_with_post_scores.keys():
                f.write("%s,%s\n" % (key, subreddits_with_post_scores[key]))
