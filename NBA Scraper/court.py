import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from colour import Color
import seaborn as sns

arc = None

def createCourt(court, colors):
    global arc
    # Drawing of court from https://github.com/venkatesannaveen/medium-articles/blob/master/nba_shotchart.ipynb
    # 3-point end lines
    court.plot([-220, -220], [0, 140], linewidth=2, color= colors['3pt'])
    court.plot([220, 220], [0, 140], linewidth=2, color=colors['3pt'])
    
    # 3-point arc
    arc = mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor= colors['3pt'], lw=2)
    court.add_artist(arc)

    # Lane and Key
    court.plot([-80, -80], [0, 190], linewidth=2, color= colors['midRange'])
    court.plot([80, 80], [0, 190], linewidth=2, color= colors['midRange'])
    court.plot([-60, -60], [0, 190], linewidth=2, color=colors['midRange'])
    court.plot([60, 60], [0, 190], linewidth=2, color=colors['midRange'])
    court.plot([-80, 80], [190, 190], linewidth=2, color=colors['midRange'])
    court.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=colors['midRange'], lw=2))

    # Rim
    court.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=colors['paint'], lw=2))
    
    # Backboard
    court.plot([-30, 30], [40, 40], linewidth=2, color=colors['paint'])
    
    # Remove ticks
    court.set_xticks([])
    court.set_yticks([])
    
    # Set axis limits
    court.set_xlim(-250, 250)
    court.set_ylim(0, 470)


def genColor(leagueAvg, maxVal, minVal, playerVal):
    if (playerVal - leagueAvg) >= 0:
        length = math.ceil((maxVal - leagueAvg)*100)
        palette = sns.color_palette("light:r", length)
        return palette[math.ceil((playerVal - leagueAvg)*100)]
    else:
        length = math.ceil((leagueAvg - minVal)*100)
        palette = sns.color_palette("light:b_r", length)
        return palette[math.ceil((leagueAvg - playerVal)*100)]

def genCourt(prct):
    fig = plt.figure(figsize=(4, 3.76))
    court = fig.add_axes([0, 0, 1, 1])
    shotColors = {'paint': genColor(.58, .80, .32, prct['paint']), 'midRange': genColor(.42, .70, .20, prct['midRange']), 
                  '3pt': genColor(.36, .50, .18, prct['3pt']) 
                  }
    createCourt(court, shotColors)  

    plt.show()
#plt.savefig('NBAplot.png')

""", 'midRange': genColor(math.ceil(prct['midRange'])), 
                  '3pt': genColor(math.ceil(prct['3pt']))"""