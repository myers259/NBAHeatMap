import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import seaborn as sns


class Court():
    def __init__(self, prct):
        self.prct = prct

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
            return palette[math.ceil((leagueAvg - playerVal)*100)]

    def genCourt(self):
        """ generates the visualization """

        fig = plt.figure(figsize=(4, 3.76))
        self.court = fig.add_axes([0, 0, 1, 1])
        self.shotColors = {'paint': self.genColor(.58, .80, .32, self.prct['paint']), 'midRange': self.genColor(.42, .70, .20, self.prct['midRange']),
                           '3pt': self.genColor(.36, .50, .18, self.prct['3pt'])
                           }
        self.createCourt()

        plt.show()
