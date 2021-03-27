# pocketstars-dl

A Python program for downloading content from your favorite creators on PocketStars.

<img src="https://raw.githubusercontent.com/Amenly/pocketstars-dl/main/media/terminal.png" width="600">

## Installation

*REQUIRES Python 3.9+*

First run the following at the command line:

`pip install -r requirements.txt`


## Prerequisites

To be able to use this, you're going to need to get a couple bits of information through your PocketStars account. It might seem a little daunting at first but it's really not that bad. If you're familiar with DIGITALCRIMINAL's OnlyFans program, you'll recognize it's nothing new.

You'll notice that there's an `auth.json` file in the main directory. You're going to need to fill it out:

```json
{
    "auth":
        "cookies": {
            "session": "",
            "session.sig": ""
        },
        "user_agent": ""
}
```

Let's work on getting the `session` and `session.sig` cookies. First, go to the PocketStars website and go to any creator's account that you're subscribed to. At this point, you need to open your browser's developer tools. To do that, consult the following table:

| Operating System | Keys (for Google Chrome) |
| :----------------: | :----: |
| macOS | <kbd>alt</kbd> + <kbd>cmd</kbd> + <kbd>i</kbd> |
| Windows | <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>i</kbd> |
| Linux | <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>i</kbd> |

Once you have your tools open, click on the `Network` tab at the top of the developer tools. Then find and click the subtab called `XHR`.

<img src="https://raw.githubusercontent.com/Amenly/pocketstars-dl/main/media/graphql.png">

Now, scroll all the way to the bottom of that creator's posts until you see the "Load more" button. Click "Load more" and you should see a network request called `graphql`. Click on that and scroll down until you see a section titled `Request Headers`.

Once you find the `Request Headers`, look for a subsection called `Cookie`. Inside of that will be your `session` and `session.sig` cookies. Copy their corresponding values and paste them into the `auth.json` file.

<img src="https://raw.githubusercontent.com/Amenly/pocketstars-dl/main/media/cookies.png">

Now we need the `user_agent`, but this is the easiest part. You have two options: you can get your `user_agent` from inside of the `Request Headers` or you can simply go to Google and search 'What is my user agent?'. Whichever one you use, paste it into the `auth.json` file as well.

## Usage

Now that that's out of the way, you can now use the program. Simply run this in your command line:

`python main.py`

After that, just follow the directions that the program gives you.
