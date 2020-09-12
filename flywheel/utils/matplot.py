import matplotlib.pyplot as plt

def lineplot(x_data, y_datas, x_label="", y_label="", title=""):
	for y_data in y_datas:
		plt.plot(x_data, y_data)
	plt.show()

def subfig_lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()