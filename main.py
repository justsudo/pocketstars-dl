import json
import itertools

import requests

import helpers.auth as auth
import helpers.constants as constants
import helpers.payloads as payloads
import helpers.utils as utils


def scrape_posts(s, username, offset=0):
    payload = payloads.make_posts_payload(username, offset)
    with s.post(constants.URL, data=json.dumps(payload)) as r:
        if r.ok:
            posts = r.json()['data']['posts']
            attachments = [
                (post['attachments'], post['createdAt']) for post in posts]
            urls = [
                (data['url'], date) for attachment, date in attachments for data in attachment if attachment and not data['url'].startswith('/')]
            if len(posts) < constants.POSTS_LIMIT:
                return urls
            urls += scrape_posts(s, username, offset + constants.POSTS_LIMIT)
            return urls
        r.raise_for_status()


def parse_profile(profile):
    def print_profile_info(info):
        for i, j in info.items():
            print(f"{i.capitalize().replace('_', ' ')}: {j}")
        return

    user = profile['data']['user']
    if not user['subscription']:
        raise requests.exceptions.InvalidHeader(
            'Your cookies or user-agent are/is invalid.')
    info = dict(display_name=user['displayName'],
                username=user['username'],
                num_posts=user['numPosts'],
                num_images=user['numImages'],
                num_videos=user['numVideos'])
    print_profile_info(info)
    lists = [[] for i in range(constants.NUM_DATA)]
    profile_media = list(itertools.zip_longest(
        [user['banner'], user['avatar']], *lists))
    return profile_media


def get_profile(s, username):
    payload = payloads.make_profile_payload(username)
    with s.post(constants.URL, data=json.dumps(payload)) as r:
        if r.ok:
            return r.json()
        r.raise_for_status()


def get_username(s, offset=0):
    def print_usernames(usernames: dict):
        for count, username in usernames.items():
            print('{:<3}: {:^20}'.format(count, username))
        return

    def get_num_input(length, message) -> int:
        while True:
            try:
                num = int(input(message))
                if 0 < num <= length:
                    return num
            except ValueError:
                pass
            print('Invalid input. Try again.')

    payload = payloads.make_list_users_payload(offset)
    with s.post(constants.URL, data=json.dumps(payload)) as r:
        if r.ok:
            users = r.json()['data']['users']
            usernames = [i['username'] for i in users]
            if len(usernames) < constants.FOLLOWINGS_LIMIT:
                if offset:
                    return usernames
            else:
                usernames += get_username(
                    s, offset + constants.FOLLOWINGS_LIMIT)
            dict_usernames = dict(enumerate(usernames, 1))
            print_usernames(dict_usernames)
            return dict_usernames[
                get_num_input(
                    len(dict_usernames), '\nEnter the number next to the user whose content you would like to download: ')]
        r.raise_for_status()


def main():
    cookies, user_agent = auth.get_auth()
    s = auth.make_session(cookies, user_agent)
    username = get_username(s)
    profile = get_profile(s, username)
    profile_media = parse_profile(profile)
    posts_media = scrape_posts(s, username)
    utils.create_main_dir(username)
    utils.prepare_download(
        profile_media + posts_media, s, username)


if __name__ == '__main__':
    main()
