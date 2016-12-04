import pylab
import numpy
import os
from hashing import BANDS, ROWS_PER_BAND


def lsh_probability(x):
    return 1 - (1 - x**ROWS_PER_BAND)**BANDS


if __name__ == "__main__":
    x = numpy.linspace(0, 1)

    # compose plot
    pylab.plot(x, lsh_probability(x))
    pylab.xlabel('Jaccard similarity')
    pylab.ylabel('Probability of collision')
    pylab.savefig(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'report', 'img', 'lsh_probability.jpg'), bbox_inches='tight')
    pylab.show()
