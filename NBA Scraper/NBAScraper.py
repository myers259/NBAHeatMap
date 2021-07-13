from urllib.parse import urljoin
from html.parser import HTMLParser
from urllib.request import urlopen
from court import Court


class Collector(HTMLParser):

    def __init__(self, player, season=""):
        HTMLParser.__init__(self)

        self.data = dict()
        self.currTag = ""
        self.atSeasonTag = False
        self.season = season
        self.currRow = ""

        self.shotData = dict()

        splitName = player.split()
        lastInital = splitName[1][0]
        urlName = ""
        try:
            urlName = splitName[1][:5]
        except:
            urlName = splitName[1][:len(splitName[1])]

        urlName = urlName + splitName[0][:2]

        playerNum = "01"
        if len(splitName) > 2:
            playerNum = "02"

        if season == "":
            self.url = "https://www.basketball-reference.com/players/" + \
                lastInital.lower() + "/" + urlName.lower() + playerNum + ".html"
            self.seasonSearch = True
        else:
            self.url = "https://www.basketball-reference.com/players/" + \
                lastInital.lower() + "/" + urlName.lower() + playerNum + "/shooting/" + season
            self.seasonSearch = False
            self.data[self.season] = dict()

    def handle_data(self, data):
        """ appendings data found on the page to the list of data """

        if data == "Shot Distance":
            self.currRow = "Shot Distance"
        if data == "Shot Type":
            self.currRow = ""

        if self.currTag == "" or self.season == "":
            return
        symbols = ['@', '#', '$', '%', '^', '*',
                   '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', ';', ':', '<', '>', '/', "\n"]
        # Loop through the symbols and see if the line has any as we do not want to include HTML logic

        for symbol in symbols:
            if symbol in data or not data.isdigit() and not data.replace('.', '', 1).strip().isdigit():
                # We found a symbol associated with HTML logic, so we do not add the line to data
                return

        if self.currTag + self.currRow in self.data[self.season].keys():
            self.data[self.season][self.currTag + self.currRow].append(data)
        else:
            self.data[self.season][self.currTag + self.currRow] = [data]

    def handle_starttag(self, tag, attrs):
        """ Appends necessary data from the page """

        if tag == 'td':
            for attr in attrs:
                if attr[0] == 'data-stat':
                    self.currTag = attr[1]

        if tag == 'tr':
            if self.seasonSearch:
                self.season = ""
                for attr in attrs:
                    if attr[0] == 'id':
                        seasons = attr[1].split('.')
                        self.season = seasons[1]
                        self.data[self.season] = dict()

    def getData(self):
        """ returns a list of the data from the page """
        return self.data

    def getShotData(self):
        """ returns a list of the shooting data from the page """
        return self.shotData


class ShootingChart():
    def __init__(self):
        pass

    def format(self, season, data):
        """ Returns a dictionary of formated shooting data  """

        shots = {'atRim': [0, 0], '3to10': [0, 0], '10to16': [
            0, 0], '16to3pt': [0, 0], '3pt': [0, 0]}
        i = 0
        for key in shots.keys():
            shots[key] = [int(data[season]['fgShot Distance'][i]), int(
                data[season]['fgaShot Distance'][i])]
            i += 1

        midRange = (shots['10to16'][0] + shots['16to3pt'][0]) / \
            (shots['10to16'][1] + shots['16to3pt'][1])
        paint = (shots['atRim'][0] + shots['3to10'][0]) / \
            (shots['atRim'][1] + shots['3to10'][1])
        self.formatedShots = {
            'paint': paint, 'midRange': midRange, '3pt': shots['3pt'][0]/shots['3pt'][1]}

    def playerSeasonPicker(self):
        """ Asks the user for a player and then for which season they would like to visualize """

        player = input("Please enter in a players name :  ")

        collect = Collector(player)
        content = urlopen(collect.url).read().decode()
        collect.feed(content)

        print("Here is the seasons they have played :  ")
        for season in collect.getData().keys():
            print(season)

        season = input("Which season would you like to map :  ")

        collectSeason = Collector(player, season)
        contentS = urlopen(collectSeason.url).read().decode()
        collectSeason.feed(contentS)

        self.format(season, collectSeason.getData())

    def run(self):
        self.playerSeasonPicker()
        court = Court(self.formatedShots)
        court.genCourt()


shootChart = ShootingChart()
shootChart.run()
