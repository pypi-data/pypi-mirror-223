import seaborn as sns
import matplotlib.pyplot as plt


class Plot:

    def __init__(self):
        self.axes = None

    def shape(self, dim=(10, 5)):
        plt.figure(figsize=dim)
        return self

    def grid(self, c="#EAEAF1"):
        # grid color
        self.axes.set_facecolor(c)
        # grid lines
        self.axes.grid(True, linestyle='-', color='white', linewidth=0.5, alpha=0.5)
        return self

    def label(self, xlabel, ylabel, tlabel):
        self.axes.set_ylabel(ylabel, fontsize=10)
        self.axes.set_xlabel(xlabel, fontsize=10)
        self.axes.set_title(tlabel, pad=10)
        return self

    def spine(self, top=False, right=False, bottom=False, left=False):
        self.axes.spines['top'].set_visible(top)
        self.axes.spines['right'].set_visible(right)
        self.axes.spines['bottom'].set_visible(bottom)
        self.axes.spines['left'].set_visible(left)
        return self

    def tick(self, left=False, bottom=False, labelleft=False, labelbottom=False):
        self.axes.tick_params(labelcolor='black', labelsize='small', width=0.5, labelleft=labelleft,
                              labelbottom=labelbottom, left=left, bottom=bottom)
        return self

    def set_axes(self, ax):
        self.axes = ax

    def render(self):
        plt.show()


class Barplot(Plot):

    def create(self, x, y, data, hue=None, width=0.8, c="#69b3a2", ax=None):
        self.axes = sns.barplot(x=x, y=y, hue=hue, data=data, width=width,
                                estimator="sum", errorbar=None, color=c, ax=ax)
        return self

    def bar_label(self, fmt='%.0f', pad=1):
        self.axes.bar_label(self.axes.containers[0], fmt=fmt, padding=pad, color='black',
                            fontweight=None, fontstyle='italic', family=['monospace'], fontsize=10)
        return self


class Lineplot(Plot):

    def create(self, x, y, data):
        self.axes = sns.lineplot(data=data, x=x, y=y)
        return self

    def limit(self, y_start, y_end):
        self.axes.set_ylim(y_start, y_end)
        return self


class Mapplot(Plot):

    def create(self, ct, data, x, y, c, ct_name, ax=None):
        self.axes = ax
        self.country_shape_plot(ct)
        self.data_plot(data, x, y, c)
        self.country_name_plot(ct, ct_name)
        return self

    def country_shape_plot(self, ct):
        ct.plot(ax=self.axes, facecolor="white", edgecolor="k", alpha=1, linewidth=1)

    def data_plot(self, data, x, y, c):
        data.plot(x=x, y=y, kind="scatter", c=c, colormap="Set2", ax=self.axes)

    def country_name_plot(self, ct, ct_name):
        for a, b, label in zip(
                ct.geometry.centroid.x, ct.geometry.centroid.y, ct[ct_name]
        ):
            plt.text(a, b, label, fontsize=8, ha="center")
