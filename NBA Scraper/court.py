import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import seaborn as sns


class Court():
    def __init__(self, prct, player, season):
        self.prct = prct
        self.player = player
        self.seasonPicked = season

    def createCourt(self):
        # Drawing of court from https://github.com/venkatesannaveen/medium-articles/blob/master/nba_shotchart.ipynb

        # 3-point end lines
        self.court.plot([-220, -220], [0, 140], linewidth=2,
                        color=self.shotColors['3pt'])
        self.court.plot([220, 220], [0, 140], linewidth=2,
                        color=self.shotColors['3pt'])

        # 3-point arc
        arc = mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180,
                              facecolor='none', edgecolor=self.shotColors['3pt'], lw=2)
        self.court.add_artist(arc)

        # Lane and Key
        self.court.plot([-80, -80], [0, 190], linewidth=2,
                        color=self.shotColors['midRange'])
        self.court.plot([80, 80], [0, 190], linewidth=2,
                        color=self.shotColors['midRange'])
        self.court.plot([-60, -60], [0, 190], linewidth=2,
                        color=self.shotColors['midRange'])
        self.court.plot([60, 60], [0, 190], linewidth=2,
                        color=self.shotColors['midRange'])
        self.court.plot([-80, 80], [190, 190], linewidth=2,
                        color=self.shotColors['midRange'])
        self.court.add_artist(mpl.patches.Circle(
            (0, 190), 60, facecolor='none', edgecolor=self.shotColors['midRange'], lw=2))

        # Rim
        self.court.add_artist(mpl.patches.Circle(
            (0, 60), 15, facecolor='none', edgecolor=self.shotColors['paint'], lw=2))

        # Backboard
        self.court.plot([-30, 30], [40, 40], linewidth=2,
                        color=self.shotColors['paint'])

        # Remove ticks
        self.court.set_xticks([])
        self.court.set_yticks([])

        # Set axis limits
        self.court.set_xlim(-250, 250)
        self.court.set_ylim(0, 470)

    def genColor(self, leagueAvg, maxVal, minVal, playerVal):
        """ Generates the colors for shooting percentages based on league average values """

        if (playerVal - leagueAvg) >= 0:
            length = math.ceil((maxVal - leagueAvg)*100)
            palette = sns.color_palette("light:r", length)
            return palette[math.ceil((playerVal - leagueAvg)*100)]
        else:
            length = math.ceil((leagueAvg - minVal)*100)
            palette = sns.color_palette("light:b_r", length)
            return palette[math.ceil((leagueAvg - playerVal)*100) - 1] # minus 1 because list starts at 0

    def genCourt(self):
        """ generates the visualization """

        fig = plt.figure(figsize=(4, 3.76))
        self.court = fig.add_axes([0, 0, 1, 1])
        self.shotColors = {'paint': self.genColor(self.prct['avgPaint'], .80, .32, self.prct['paint']), 'midRange': self.genColor(self.prct['avgMidRange'], .70, .20, self.prct['midRange']),
                           '3pt': self.genColor(self.prct['avg3pt'], .50, 0, self.prct['3pt'])
                           }
        self.createCourt()

        plt.text(0, 430, self.player + ",\n" + self.seasonPicked + " Season", horizontalalignment='center')

        plt.text(1, 320, "3pt: " + str(math.trunc(self.prct['3pt']*100)) + "%" , horizontalalignment='center')
        plt.text(1, 192, "Midrange: " + str(math.trunc(self.prct['midRange']*100)) + "%" , horizontalalignment='center')
        plt.text(1, 18, "Paint: " + str(math.trunc(self.prct['paint']*100)) + "%" , horizontalalignment='center')

        plt.text(-235, 410, "League Averages : Paint {}%, Midrange {}%, 3pt {}%".format(math.trunc(self.prct['avgPaint'] * 100), math.trunc(self.prct['avgMidRange'] * 100), math.trunc(self.prct['avg3pt'] * 100)))

        plt.show()
