import requests


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
