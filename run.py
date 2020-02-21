from lxml import html
import requests
import dateparser


from models import db, Player

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

    #repeat



def get_player_info(url, position):

    r = requests.get(url) # this will be determined later

    tree = html.fromstring(r.content)
    slug = None
    name = tree.xpath('//h1[@itemprop="name"]/text()')[0]

    ## below is a weird thing with 
    # position is going to come from the site
    shoots = tree.xpath('//*[@id="meta"]/div/p[1]/text()[2]')[0]
    dob = dateparser.parse(tree.xpath('//*[@id="necro-birth"]/a/text()')[0] + ' ' + tree.xpath('//*[@id="necro-birth"]/a/text()')[1]) 
    weight = tree.xpath('//*[@id="meta"]/div/p[2]/span[2]/text()')[0][:-2]
    height = tree.xpath('//*[@id="meta"]/div/p[2]/span[1]/text()')[0]
    # nationality = tree.xpath('//*[@itemprop="birthPlace"]/a/@href') # regex needed to get url
    is_hof = True if tree.xpath('//*[@class="important special"]/a/text()')[0] == 'Hall of Fame' else False


    player = Player(slug, name, position, shoots, height, weight, dob, is_hof)

    db.session.add(player)


def parse_skater(player_id):

    seasons = tree.xpath('//table[@id="stats_basic_nhl"]/tbody/tr')
    ids = []
    for season in seasons:
        ids.append(season.value()[0])


    for id in ids:
        
        season = id.split('.')[1]
        age = tree.xpath('//tr[@id="{}"]/td[@data-stat="age"]/text()'.format(id))

    
"""db.drop_all()
    db.create_all()
    get_player_info('https://www.hockey-reference.com/players/a/appssy01.html', 'C')
    db.session.commit()"""

if __name__ == '__main__':
   
    """
    seasons = tree.xpath('//table[@id="stats_basic_nhl"]/tbody/tr')
    print("foo")"""
    
    r = requests.get('https://www.hockey-reference.com/players/a/appssy01.html') # this will be determined later

    tree = html.fromstring(r.content)
    
    seasons = tree.xpath('//table[@id="stats_basic_nhl"]/tbody/tr')
    stats = ['age', 'pen_min']
    ids = []
    for season in seasons:
        ids.append(season.values()[0])
    skater_season = {}
    for id in ids:
        
        season = id.split('.')[1]
        skater_season[season] = {}
        for stat in stats:
            skater_season[season][stat] = tree.xpath('//tr[@id="{}"]/td[@data-stat="{}"]/text()'.format(id, stat))[0]

    print(skater_season)
        




    



    



