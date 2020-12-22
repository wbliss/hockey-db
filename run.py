from lxml import html
import requests
from requests.exceptions import ConnectionError
import dateparser
import re
import time

from models import db, Player, SkaterSeason

SKATER_STATS = [
    'age', 
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


class HockeyRefParser():

    def __init__(self, stats):
        self.client = requests.Session()
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        self.client.headers.update(headers)

    def get_link_position(self, player):
            
        try: #  current players are bold
            url = player.xpath('strong/a')[0].get('href')
        except IndexError:
            url = player.xpath('a')[0].get('href')

        position = re.search("\,(.*?)\)", player.xpath('text()')[0]).group(1).strip() #  icky

        return url, position

    def parse_letter(self, letter):

        r = self.client.get('https://www.hockey-reference.com/players/{}/'.format(letter))

        tree = html.fromstring(r.content)
        players = tree.xpath('//div[@id="div_players"]/p[@class="nhl"]')
        
        for player in players:
            
            url, position = self.get_link_position(player)
            try:
                self.get_player_info(url, position)
            except ConnectionError:  # if connection error commit then wait 10 minutes
                db.session.commit()
                time.sleep(60 * 10)
                get_player_info(url, position)

        db.session.commit()

    def get_birthplace(self, tree):

        birth_link = tree.xpath('//span[@itemprop="birthPlace"]/a')[0].get('href')
        locations = birth_link.split('?')[1].split('&')
        country = locations[0].split('=')[1]
        
        if country == "CA":
            state = locations[1].split('=')[1]
        elif country == "US":
            state = locations[2].split('=')[1]
        else:
            state = None

        return (country, state)

    def get_player_info(self, url, position):

        r = self.client.get('https://www.hockey-reference.com' + url)

        tree = html.fromstring(r.content)
        slug = url.split('/')[3].split('.')[0]
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

        try:
            country, state = self.get_birthplace(tree)
        except IndexError:
            country, state = None, None

        is_hof = True if 'Hall of Fame' in tree.xpath(
            '//*[@class="important special"]/a/text()') else False

        player = Player(slug, name, position, shoots, height, weight, dob, is_hof, country, state)

        db.session.add(player)
        db.session.flush()
        if position != 'G':
            total_stats = self.parse_skater(tree)
            season = self.parse_season(player, total_stats)
        time.sleep(10)

    def parse_skater(self, tree):

        seasons_old = tree.xpath('//table[@id="stats_basic_nhl"]/tbody/tr|//table[@id="partial_table"]/tbody/tr')
        seasons_new = tree.xpath('//table[@id="stats_basic_plus_nhl"]/tbody/tr|//table[@id="partial_table"]/tbody/tr')
        seasons = seasons_old or seasons_new
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


    def parse_season(self, player, total_stats):


        for year, team_stats in total_stats.items():
            for team, stats in team_stats.items():
                season = SkaterSeason(player.id, year, team)
                for stat, value in stats.items():
                    setattr(season, stat, value)
                db.session.add(season)

    def run_alphabet(self):

        ALPHABET = 'abcdefghijklmnopqrstuvwzyz'
        db.drop_all()
        db.create_all()
        for letter in ALPHABET:
            self.parse_letter(letter)
        db.session.commit()

if __name__ == '__main__':

    h = HockeyRefParser(SKATER_STATS)
    h.run_alphabet()
