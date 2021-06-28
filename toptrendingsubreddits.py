import requests
import luigi
import schedule
import time


def authorize_api():
    """Authorize the Reddit API"""

    CLIENT_ID = "oDkt39mpoGzKjQ"
    SECRET_TOKEN = "PcGeuGZ1ovIfzIDpKi_YLTYK8zjVIw"
    username = "priya_1292"
    pwd = "Priya@1292"

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


def get_top10_post_list(res):
    """Get top 10 posts for each subreddits"""
    i = 0
    top_subreddits = []
    titles_list = []
    for post in res.json()['data']['children']:
        if i < 10:
            subreddit_title = post['data']['title']+','
            titles_list.append(subreddit_title[36:].split(','))
            i += 1
        else:
            break
    for outer in titles_list:
        for el in outer:
            if len(el) != 0:
                el = el.strip()
                top_subreddits.append(el)
    return top_subreddits


def get_post_ids(top_subreddits, headers):
    """Get 5 higher scoring comments for each post"""
    j = 0
    top_subreddits_postId = {}
    for key in top_subreddits:
        each_post_res = requests.get(
            "https://oauth.reddit.com"+top_subreddits[j]+'/top', headers=headers)
        k = 0
        if 'reason' not in each_post_res.json():
            posts_title_list = []
            for post in each_post_res.json()['data']['children']:
                if k < 10:
                    posts_title_list.append(post['data']['id'])
                    k += 1
                else:
                    break
            top_subreddits_postId[key] = posts_title_list
        else:
            pass
        j += 1
    return top_subreddits_postId


class GetSubRedditsPosts(luigi.Task):
    """
    Get list of the top 10 subreddits posts
    """

    def output(self):
        return luigi.LocalTarget("topSubRedditsPosts.csv")

    def run(self):

        # fetch header after the authorization
        print("hello world")
        headers = authorize_api()

        # Get the top 50 trending subreddits and creating a list
        res = requests.get(
            "https://oauth.reddit.com/r/trendingsubreddits", headers=headers)

        top_subreddits = []
        top_subreddits = get_top10_post_list(res)

        # Get the top 10 posts for each subreddit
        top_subreddits_postId = get_post_ids(top_subreddits, headers)

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
        print(subreddits_with_post_scores)

        with self.output().open("w") as f:
            for key in subreddits_with_post_scores.keys():
                f.write("%s,%s\n" % (key, subreddits_with_post_scores[key]))

obj = GetSubRedditsPosts()

if __name__ == '__main__':

    luigi.build([GetSubRedditsPosts()], local_scheduler=True)
    schedule.every(12).hours.do(obj.run())

    while 1:
        schedule.run_pending()
        time.sleep(1)
