import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d

# read data from disk
e, sr1, u, l, resid = np.loadtxt("fig_4.dat", unpack=True)

# read background from disk
eb0, b0 = np.loadtxt("b0.txt", unpack=True)

# check significance from paper
ty = 0.65  # tonne-years observed
observed = sr1[(e < 7.) & (e > 1.)].sum() * ty
background_function = interp1d(eb0, b0, kind="cubic")
expected = quad(background_function, 1., 7.)[0] * ty
z = (observed - expected) / expected**0.5


if __name__ == "__main__":

    # style of error bars
    style = dict(c="black", ms=3, fmt='o', capsize=2, elinewidth=2, markeredgewidth=2)

    fig, ax = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0)

    # top panel of data
    ax[0].set_ylabel(r"Events/(t$\cdot$y$\cdot$keV)")
    ax[0].plot(eb0, b0, label="$B_0$", c="#FF0000")
    ax[0].errorbar(e, sr1, yerr=[sr1 - l, u - sr1], label="SR1 data", **style)
    ax[0].legend(loc="lower right", frameon=False)
    ax[0].set_ylim(0, 120)

    # bottom panel of residuals
    ax[1].set_ylabel(r"$\sigma$")
    ax[1].set_xlabel(r"Energy [keV]")
    ax[1].scatter(e, resid, c="black", s=10)
    ax[1].set_xlim(0, 30)
    ax[1].set_ylim(-5, 5)

    # bands
    x = np.linspace(0., 30., 1000)
    ax[1].fill_between(x, -2., y2=-1., color="#CCF24C", zorder=0)
    ax[1].fill_between(x, 1., y2=2., color="#CCF24C", zorder=0)
    ax[1].fill_between(x, -1., y2=1., color="#FFFF7F", zorder=0)
    ax[1].set_yticks([-2, 2])

    plt.savefig("fig_4.pdf")
