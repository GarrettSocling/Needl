import needl, needl.schedule as schedule, needl.utils as utils
import urllib.parse as url

TWITTER = 'https://www.twitter.com/{0}'


def register():
    # todo: ugly as hell
    gui = needl.settings['twitter']['get_user_interval']
    args = map(int, gui.split('..'))
    schedule.every(*args).minutes.do(get_user)

    se = needl.settings['twitter']['search_interval']
    args = map(int, se.split('..'))
    schedule.every(*args).minutes.do(search)


def get_user():
    first = utils.get_line(needl.args.datadir + '/first-names.txt').title()
    last = utils.get_line(needl.args.datadir + '/last-names.txt').title()

    needl.log.info('Finding Twitter user: "%s %s"', first, last)

    browser = utils.get_browser()
    browser.get(TWITTER.format(first + last))

    if "Sorry, that page doesn’t exist!" in browser.page_source:
        needl.log.debug('Twitter user "%s %s" not found', first, last)

    browser.quit()


def search():
    hashtag = '#' + utils.get_keywords(1)

    needl.log.info('Searching Twitter for: "%s"', hashtag)

    browser = utils.get_browser()
    browser.get(TWITTER.format('search?f=tweets&vertical=default&q=' + url.quote_plus(hashtag) + '&src=typd'))

    try:
        first_tweet_by = browser.find_elements_by_css_selector('.stream-item > .tweet')[0].get_attribute('data-screen-name')
        needl.log.info('Latest Tweet for %s by %s', hashtag, first_tweet_by)
    except:
        pass
    finally:
        browser.quit()