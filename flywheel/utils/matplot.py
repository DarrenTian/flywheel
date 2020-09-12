import matplotlib.pyplot as plt

def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    #print(x_data)
    #print(y_data)
    #x_data = [0, 1, 2, 3]
    #y_data = [2, 4, 6, 8]
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()