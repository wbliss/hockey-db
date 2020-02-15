from lxml import html
import requests
import dateparser


from models import db, Player





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
    db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    get_player_info('https://www.hockey-reference.com/players/a/appssy01.html', 'C')
    



    



