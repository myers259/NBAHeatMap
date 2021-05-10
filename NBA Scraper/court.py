import matplotlib.pyplot as plt
import matplotlib as mpl

def createCourt(court, color):
    # Drawing of court from https://github.com/venkatesannaveen/medium-articles/blob/master/nba_shotchart.ipynb

    # 3-point end lines
    court.plot([-220, -220], [0, 140], linewidth=2, color="black")
    court.plot([220, 220], [0, 140], linewidth=2, color="black")
    
    # 3-point arc
    court.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

    # Lane and Key
    court.plot([-80, -80], [0, 190], linewidth=2, color=color)
    court.plot([80, 80], [0, 190], linewidth=2, color=color)
    court.plot([-60, -60], [0, 190], linewidth=2, color=color)
    court.plot([60, 60], [0, 190], linewidth=2, color=color)
    court.plot([-80, 80], [190, 190], linewidth=2, color=color)
    court.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

    # Rim
    court.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    
    # Backboard
    court.plot([-30, 30], [40, 40], linewidth=2, color=color)
    
    # Remove ticks
    court.set_xticks([])
    court.set_yticks([])
    
    # Set axis limits
    court.set_xlim(-250, 250)
    court.set_ylim(0, 470)
  

fig = plt.figure(figsize=(4, 3.76))
court = fig.add_axes([0, 0, 1, 1])
createCourt(court, "black")
plt.show()