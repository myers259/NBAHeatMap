from urllib.parse import urljoin
from html.parser import HTMLParser
from urllib.request import urlopen
from court import Court


class Collector(HTMLParser):

    def __init__(self, player, season=""): # "" passed in if looking for league avg
        HTMLParser.__init__(self)

        self.data = dict()
        self.currTag = ""
        self.atSeasonTag = False
        self.season = season
        self.currRow = ""
        self.gettingLeagueAvg = False
        self.atLeagueAverageRow = False
        self.atShootingStats = False

        self.leagueAvgs = dict()

        if player != "":
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
        elif player != "":
            self.url = "https://www.basketball-reference.com/players/" + \
                lastInital.lower() + "/" + urlName.lower() + playerNum + "/shooting/" + season
            self.seasonSearch = False
            self.data[self.season] = dict()
        else: # Gathering League average data
            self.seasonUrl = "https://www.basketball-reference.com/leagues/NBA_" + season +".html"
            self.seasonSearch = False
            self.gettingLeagueAvg = True
            self.data[self.season] = {'leagueAvg' : dict()}
 

            
    def handle_data(self, data):
        """ appendings data found on the page to the list of data """

        if data == "Shot Distance":
            self.currRow = "Shot Distance"
        if data == "Shot Type":
            self.currRow = ""

        if self.currTag == "" or self.season == "":
            return

        if data == 'Shooting Stats':
            self.atShootingStats = True

        if data == "League Average" and self.atShootingStats:
            self.atLeagueAverageRow = True

        
        symbols = ['@', '#', '$', '%', '^', '*',
                   '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', ';', ':', '<', '>', '/', "\n"]
        # Loop through the symbols and see if the line has any as we do not want to include HTML logic

        for symbol in symbols:
            if symbol in data or not data.isdigit() and not data.replace('.', '', 1).strip().isdigit():
                # We found a symbol associated with HTML logic, so we do not add the line to data
                return
        
        if self.gettingLeagueAvg: 
            if self.atLeagueAverageRow:
                if self.currTag in self.data[self.season]['leagueAvg'].keys():
                    return # returning as there only should be one row and the scraper brings in extra that it shouldn't
                else:
                    self.data[self.season]['leagueAvg'][self.currTag] = float(data)
                return
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


class ShootingChart():
    def __init__(self):
        pass

    def format(self, data, leagueData):
        """ Returns a dictionary of formated shooting data  """

        leagueAvgs = leagueData[self.seasonPicked]['leagueAvg']

        shots = {'atRim': [0, 0], '3to10': [0, 0], '10to16': [
            0, 0], '16to3pt': [0, 0], '3pt': [0, 0]}
        i = 0
        for key in shots.keys():
            if i  < len(data[self.seasonPicked]['fgShot Distance']):
                shots[key] = [int(data[self.seasonPicked]['fgShot Distance'][i]), int(
                data[self.seasonPicked]['fgaShot Distance'][i])]
                i += 1
            else:
                shots[key] = [0,0]

        midRange = (shots['10to16'][0] + shots['16to3pt'][0]) / \
            (shots['10to16'][1] + shots['16to3pt'][1])
        paint = (shots['atRim'][0] + shots['3to10'][0]) / \
            (shots['atRim'][1] + shots['3to10'][1])
        three = 0

        leaguePaint = (((leagueAvgs['pct_fga_00_03'] * 100) * leagueAvgs['fg_pct_00_03']) + ((leagueAvgs['pct_fga_03_10'] * 100) * leagueAvgs['fg_pct_03_10']))/ \
            ((leagueAvgs['pct_fga_00_03'] * 100) + (leagueAvgs['pct_fga_03_10'] * 100))
        leagueMidRange = (((leagueAvgs['pct_fga_10_16'] * 100) * leagueAvgs['fg_pct_10_16']) + ((leagueAvgs['pct_fga_16_xx'] * 100) * leagueAvgs['fg_pct_16_xx']))/ \
            ((leagueAvgs['pct_fga_10_16'] * 100) + (leagueAvgs['pct_fga_16_xx'] * 100))
        leagueThree = leagueAvgs['fg_pct_fg3a']

        if shots['3pt'][1] != 0:
            three = shots['3pt'][0]/shots['3pt'][1]
        
        self.formatedShots = {
            'paint': paint, 'midRange': midRange, '3pt': three, 
            'avgPaint': leaguePaint, 'avgMidRange' : leagueMidRange, 'avg3pt' : leagueThree}

    def playerSeasonPicker(self):
        """ Asks the user for a player and then for which season they would like to visualize """

        self.player = input("Please enter in a players name :  ")

        collect = Collector(self.player)
        content = urlopen(collect.url).read().decode()
        collect.feed(content)

        print("Here is the seasons they have played :  ")
        for season in collect.getData().keys():
            print(season)

        self.seasonPicked = input("Which season would you like to map :  ")

        collectSeason = Collector(self.player, self.seasonPicked)
        contentS = urlopen(collectSeason.url).read().decode()
        collectSeason.feed(contentS)

        collectLeagueAvg = Collector("", self.seasonPicked)
        contentLeagueAvg = urlopen(collectLeagueAvg.seasonUrl).read().decode()
        collectLeagueAvg.feed(contentLeagueAvg)


        self.format(collectSeason.getData(), collectLeagueAvg.getData())

    def run(self):
        self.playerSeasonPicker()
        court = Court(self.formatedShots, self.player, self.seasonPicked)
        court.genCourt()


shootChart = ShootingChart()
shootChart.run()
