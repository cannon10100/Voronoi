import numpy as np
import sys

from matplotlib import pyplot as plt
from scipy.spatial.distance import cityblock
from scipy.spatial.kdtree import KDTree

def random_voronoi(size, num_points, use_kd=True):
    """
    Method that generates random points in a size x size square, then displays the Voronoi regions
    for these random points in the square.
    :param size: the size length of the square.
    :param num_points: the number of random points to generate.
    :param use_kd: a boolean specifying whether a Scipy KDTree should be used to speed calculations.
    :return: None
    """
    sources = []

    # Generate random points
    for i in range(num_points):
        temp = [np.random.randint(0, size) for j in range(2)]
        sources.append((temp[0], temp[1]))

    im = np.zeros((size, size))
    im2 = np.zeros((size, size))

    for source in sources:
        im[source] = 255
        im2[source] = 255

    # Use KDTree to find the closest source point to each pixel, and set pixel to appropriate color
    if use_kd:
        sources_kd = KDTree(sources, 2)
        it = np.nditer(im, flags=["multi_index"])

        while not it.finished:
            loc = it.multi_index
            print("Processing location (%d, %d)" % (loc[0], loc[1]))

            # Easy way to have len(sources) distinct colors
            im2[loc] = (255 / len(sources)) * sources_kd.query([loc], p=1)[1][0]
            it.iternext()
    else:
        # Otherwise, simply use brute force.
        it = np.nditer(im, flags=["multi_index"])

        while not it.finished:
            loc = it.multi_index
            print("Processing location (%d, %d)" % (loc[0], loc[1]))

            min_dist = float('inf')
            for i in range(len(sources)):
                if cityblock(loc, sources[i]) < min_dist:
                    im2[loc] = (255 / len(sources)) * i
                    min_dist = cityblock(loc, sources[i])

            it.iternext()

    plt.subplot(1, 2, 1)
    plt.imshow(im, interpolation='nearest', vmin=0, vmax=255)
    plt.title("Source points")

    plt.subplot(1, 2, 2)
    plt.imshow(im2, interpolation='nearest', vmin=0, vmax=255)
    plt.title("Voronoi regions")

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if str(sys.argv[1]).lower() in ["true", "t"]:
            print("Using KDTree")
            random_voronoi(200, 20)
        else:
            print("Using brute force")
            random_voronoi(200, 20, False)
    else:
        random_voronoi(200, 20)

    # start = datetime.datetime.now()
    # random_voronoi(200, 20)
    # end = datetime.datetime.now()
    #
    # print("Voronoi calculation took %d milliseconds" % (end - start).microseconds)
    #
    # start = datetime.datetime.now()
    # random_voronoi(200, 10, False)
    # end = datetime.datetime.now()
    #
    # print("Voronoi calculation took %d milliseconds without KDTree" % (end - start).microseconds)


