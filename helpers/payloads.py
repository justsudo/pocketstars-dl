import helpers.constants as constants


def make_list_users_payload(offset):
    payload = {
        'operationName': 'getListUsers',
        'variables': {
            'listId': 'followings',
            'offset': offset,
            'limit': constants.FOLLOWINGS_LIMIT
        },
        'query': 'query getListUsers($listId: String!, $limit: Int!, $offset: Int!) {\n  users: listUsers(listId: $listId, limit: $limit, offset: $offset) {\n    ...userTileDetails\n    __typename\n  }\n  lists {\n    id\n    name\n    __typename\n  }\n}\n\nfragment userTileDetails on Profile {\n  id\n  displayName\n  username\n  subscription {\n    state\n    expiresAt\n    __typename\n  }\n  role\n  banner\n  avatar\n  numImages\n  numVideos\n  numLikes\n  lastSeen\n  subscriptionPrice\n  featured\n  subscriptionBundles {\n    id\n    duration\n    discountPercentage\n    price\n    maxUsage\n    expiresAt\n    message\n    used\n    __typename\n  }\n  __typename\n}\n'
    }
    return payload


def make_profile_payload(username):
    payload = {
        'operationName': 'getProfile',
        'variables': {
            'username': username
        },
        'query': 'query getProfile($username: String!) {\n  user(username: $username) {\n    id\n    displayName\n    username\n    subscription {\n      state\n      expiresAt\n      __typename\n    }\n    numLikes\n    numPosts\n    listIds\n    banner\n    avatar\n    numImages\n    numVideos\n    lastSeen\n    bio\n    subscriptionPrice\n    role\n    featured\n    subscriptionBundles {\n      id\n      duration\n      discountPercentage\n      price\n      maxUsage\n      expiresAt\n      message\n      used\n      __typename\n    }\n    gender\n    postsAreHidden\n    canBeMessaged\n    blocked\n    __typename\n  }\n}\n'
    }
    return payload


def make_posts_payload(username, offset):
    payload = {
        'operationName': 'getProfilePosts',
        'variables': {
            'username': username,
            'limit': constants.POSTS_LIMIT,
            'offset': offset
        },
        'query': 'query getProfilePosts($username: String!, $limit: Int, $offset: Int) {\n  posts: profilePosts(username: $username, limit: $limit, offset: $offset) {\n    ...postDetails\n    __typename\n  }\n}\n\nfragment postDetails on Post {\n  __typename\n  id\n  text\n  isProcessing\n  attachments {\n    ... on VideoAttachment {\n      id\n      watermark {\n        weight\n        size\n        color\n        text\n        position\n        __typename\n      }\n      thumbnailUrl\n      url\n      tileUrl\n      __typename\n    }\n    ... on ImageAttachment {\n      id\n      watermark {\n        weight\n        size\n        color\n        text\n        position\n        __typename\n      }\n      url\n      tileUrl\n      __typename\n    }\n    __typename\n  }\n  user {\n    ...userDetails\n    __typename\n  }\n  numLikes\n  likedByUser\n  createdAt\n  deleteAt\n  comments {\n    ...postComments\n    __typename\n  }\n  tipsAmount {\n    usd\n    simp\n    __typename\n  }\n  ... on PaidPost {\n    price\n    message\n    purchased\n    subscribedToUser\n    __typename\n  }\n  ... on PrivatePost {\n    subscribedToUser\n    __typename\n  }\n  campaignGoal\n  userCampaignContributions {\n    usd\n    simp\n    __typename\n  }\n  totalCampaignContributions {\n    usd\n    simp\n    __typename\n  }\n  poll {\n    userCanVote\n    expiresAt\n    votes {\n      text\n      count\n      ownVote\n      __typename\n    }\n    __typename\n  }\n  pinned\n}\n\nfragment userDetails on UserView {\n  id\n  displayName\n  username\n  avatar\n  banner\n  role\n  __typename\n}\n\nfragment postComments on TopLevelComment {\n  id\n  text\n  user {\n    ...userDetails\n    __typename\n  }\n  numLikes\n  likedByUser\n  createdAt\n  comments {\n    ...nestedComments\n    __typename\n  }\n  __typename\n}\n\nfragment nestedComments on NestedComment {\n  id\n  text\n  user {\n    ...userDetails\n    __typename\n  }\n  numLikes\n  likedByUser\n  createdAt\n  __typename\n}\n'
    }
    return payload
