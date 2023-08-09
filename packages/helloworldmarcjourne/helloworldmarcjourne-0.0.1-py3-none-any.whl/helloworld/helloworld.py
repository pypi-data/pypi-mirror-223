import matplotlib.pyplot as plt

def plot ():
    fig, ax = plt.subplots()
    ax.plot([1, 3, 4, 6], [2, 3, 5, 1])

    plt.show() # affiche la figure à l'écran