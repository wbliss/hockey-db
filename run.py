from lxml import html
import requests
import dateparser
import re
import time

from models import db, Player, SkaterSeason

SKATER_STATS = ['age', 
                'lg_id', 
                'games_played', 
                'goals',
                'assists', 
                'points', 
                'plus_minus', 
                'pen_min', 
                'goals_ev',
                'goals_pp',
                'goals_sh',
                'goals_gw',
                'assists_ev',
                'assists_pp',
                'assists_sh',
                'shots',
                'time_on_ice',
                'time_on_ice_avg',
                'award_summary'
                ]

ALPHABET = 'abcdefghijklmnopqrstuvwzyz'

def run(base):

    pass
    # start on a
    # get list of urls
    # for url
    # get player info
    # determine if goalie or skater
    # get reg season info
    # get playoff info

    # hit end
    # go to b

    # repeat

def get_link_position(player):
        
    try: #  current players are bold
        url = player.xpath('strong/a')[0].get('href')
    except IndexError:
        url = player.xpath('a')[0].get('href')

    position = re.search("\,(.*?)\)", player.xpath('text()')[0]).group(1).strip() #  icky

    return url, position

def parse_letter(letter):

    r = requests.get('https://www.hockey-reference.com/players/{}/'.format(letter))

    tree = html.fromstring(r.content)
    players = tree.xpath('//div[@id="div_players"]/p[@class="nhl"]')
    
    for player in players:
        
        url, position = get_link_position(player)
        get_player_info(url, position)

    db.session.commit()

def get_player_info(url, position):

    r = requests.get('https://www.hockey-reference.com' + url)

    tree = html.fromstring(r.content)
    slug = None
    name = tree.xpath('//h1[@itemprop="name"]/span/text()')[0]

    try:
        shoots = tree.xpath('//*[@id="meta"]/div/p[1]/text()[2]')[0][2]
    except IndexError:
        shoots = None

    dob = dateparser.parse(tree.xpath('//*[@id="necro-birth"]/a/text()')[0] + ' ' + tree.xpath('//*[@id="necro-birth"]/a/text()')[1])
    try:
        weight = tree.xpath('//*[@id="meta"]/div/p/span[@itemprop="weight"]/text()')[0][:-2]
    except IndexError:
        weight = None
    try:
        height = tree.xpath('//*[@id="meta"]/div/p/span[@itemprop="height"]/text()')[0]
    except IndexError:
        height = None
    # nationality = tree.xpath('//*[@itemprop="birthPlace"]/a/@href') # regex needed to get url
    is_hof = True if 'Hall of Fame' in tree.xpath(
        '//*[@class="important special"]/a/text()') else False

    player = Player(slug, name, position, shoots, height, weight, dob, is_hof)

    db.session.add(player)
    db.session.flush()
    if position != 'G':
        total_stats = parse_skater(tree)
        season = map_skater(player, total_stats)
    time.sleep(4)

def parse_skater(tree):

    seasons = tree.xpath('//table[@id="stats_basic_nhl"]/tbody/tr|//table[@id="partial_table"]/tbody/tr')
    skater = {}
    # each season object
    for season in seasons:
        season_id = season.values()[0]

        try: 
            season_year = season_id.split('.')[1]
        except IndexError:
            pass

        # special logic for the team
        # if the column is a total, then skip
        try:
            team = tree.xpath('//tr[@id="{}"]/td[@data-stat="team_id"]/a/text()'.format(season_id))[0]
        except IndexError:
            continue
        # creates mapping structure
        skater[season_year] = {}
        skater[season_year][team] = {}
        for stat in SKATER_STATS:
            # these stats are links
            if stat in ['lg_id', 'award_summary']:
                try:
                    skater[season_year][team][stat] = tree.xpath(
                        '//tr[@id="{}"]/td[@data-stat="{}"]/a/text()'.format(season_id, stat))[0]
                except IndexError:
                    skater[season_year][team][stat] = None
            else:
                try:
                    value = tree.xpath(
                        '//tr[@id="{}"]/td[@data-stat="{}"]/text()'.format(season_id, stat))[0]
                    
                    # convert avg toi from mm:ss to float
                    if stat == 'time_on_ice_avg':
                        minutes, seconds = value.split(':')
                        seconds = int(seconds) / 60
                        value = int(minutes) + seconds

                    skater[season_year][team][stat] = value
                        
                except IndexError:
                    skater[season_year][team][stat] = None

    return(skater)


def map_skater(player, total_stats):
    
    season = None
    for year, team_stats in total_stats.items():
        for team, stats in team_stats.items():
            season = SkaterSeason(player.id, year, team)
            for stat, value in stats.items():
                setattr(season, stat, value)
            db.session.add(season)
            




"""db.drop_all()
    db.create_all()
    get_player_info('https://www.hockey-reference.com/players/a/appssy01.html', 'C')
    db.session.commit()"""

if __name__ == '__main__':

    for letter in ALPHABET:
        parse_letter(letter)