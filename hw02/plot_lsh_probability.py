import pylab
import numpy as np
import os
from hashing import BANDS, ROWS_PER_BAND


R_ALT = 10
B_ALT = 10


def lsh_probability(x):
    return 1 - (1 - pow(x, ROWS_PER_BAND))**BANDS  # used pow() to avoid warning


def lsh_probability_alternative(x):
    return 1 - (1 - pow(x, R_ALT))**B_ALT  # used pow() to avoid warning


if __name__ == "__main__":
    x_axis = np.linspace(0, 1)
    pylab.plot(x_axis, lsh_probability(x_axis), label='r = %d, b = %d' % (ROWS_PER_BAND, BANDS))
    pylab.plot(x_axis, lsh_probability_alternative(x_axis), label='r = %d, b = %d' % (R_ALT, B_ALT))
    pylab.legend(loc=0)  # 0 -> best location
    pylab.xlabel('Jaccard similarity')
    pylab.ylabel('Collision probability')
    pylab.savefig(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'report', 'img', 'lsh_probability.jpg'), bbox_inches='tight')
    pylab.show()
