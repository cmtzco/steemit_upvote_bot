from piston.steem import Steem
from piston.steem import BroadcastingError
import threading
import time
import creds

top_writers = ["reported"]

my_favorites = []

my_subscriptions = top_writers  + my_favorites

upvote_history = []


def multifeed(puppet, puppet_active_key, puppet_posting_key):
    print("Waiting for new posts by {}".format(my_subscriptions))
    steem = Steem(wif=puppet_posting_key)
    for comment in steem.stream_comments():

        if comment.author in my_subscriptions:
            if len(comment.title) > 0:

                if comment.identifier in upvote_history:
                    continue

                print("New post by @{} {}".format(comment.author, url_builder(comment)))

                try:
                    print("Voting from {} account".format(puppet))
                    comment.vote(100, puppet)
                    print("====> Upvoted")
                    upvote_history.append(comment.identifier)
                except BroadcastingError as e:
                    print("Upvoting failed...")
                    print("We have probably reached the upvote rate limit.")
                    print(str(e))
                except Exception as er:
                    print("Error:{}".format(e))

def feed():
    print("Waiting for new posts by %s\n" % my_subscriptions)
    steem = Steem(wif=posting_key)
    for comment in steem.stream_comments():

        if comment.author in my_subscriptions:
            # Comments don't have titles. This is how we can know if we have a post or a comment.
            if len(comment.title) > 0:

                # check if we already upvoted this. Sometimes the feed will give duplicates.
                if comment.identifier in upvote_history:
                    continue

                print("New post by @%s %s" % (comment.author, url_builder(comment)))

                try:
                    comment.vote(100, account)
                    print("====> Upvoted")
                    upvote_history.append(comment.identifier)
                except BroadcastingError as e:
                    print("Upvoting failed...")
                    print("We have probably reached the upvote rate limit.")
                    print(str(e))
                # commenting out unless we decide to use the tip
                #if comment.author in my_favorites:
                #    send_a_tip(comment.author)
                #    print("====> Sent $2 SBD to @%s" % comment.author)


# send $2 in SBD
def send_a_tip(author):
    steem = Steem(wif=active_key)
    steem.transfer(author, 2.0, "SBD", memo="I love your blog. Here is a small gift for you.", account=account)


def url_builder(comment):
    return "https://steemit.com/%s/%s" % (comment.category, comment.identifier)

if __name__ == "__main__":
    while True:
        try:
           time.sleep(1)
           for ea_acct in accounts:
               pupp = ea_acct
               pupp_ak = accounts[ea_acct]['active_key']
               pupp_pk = accounts[ea_acct]['posting_key']
               t = threading.Thread(target=multifeed, args=(pupp, pupp_ak, pupp_pk))
               t.start()
               t.join()
        except (KeyboardInterrupt, SystemExit):
            print("Quitting...")
            break
        except Exception as e:
            print(e)
            print("### Exception Occurred: Restarting...")
