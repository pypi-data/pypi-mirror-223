import numpy as np
import scipy.optimize
from geographiclib.geodesic import Geodesic


def geodist_point_lineseg(point, *, start, end, geod=None):
    if geod is None:
        geod = Geodesic.WGS84

    line = geod.InverseLine(*start, *end, Geodesic.LATITUDE | Geodesic.LONGITUDE)
    arc_min, arc_max = 0, line.a13

    def _dist(arc):
        point2 = line.ArcPosition(arc, Geodesic.LATITUDE | Geodesic.LONGITUDE)
        lat2, lon2 = point2["lat2"], point2["lon2"]
        return geod.Inverse(*point, lat2, lon2, Geodesic.DISTANCE)["s12"]

    res = scipy.optimize.minimize_scalar(_dist, bounds=(arc_min, arc_max))
    assert res.success

    return min([res.fun, _dist(0), _dist(arc_max)])


def geodist_points_lineseg(points, *, start, end, geod=None):
    return np.array(
        [
            geodist_point_lineseg(point, start=start, end=end, geod=geod)
            for point in points
        ]
    )


def filter(points, threshold, geod=None):
    if len(points) == 0:
        return np.empty(0, dtype=bool)

    points = np.array(points)

    n_points = points.shape[0]
    if n_points <= 2:
        return np.full(n_points, True)

    dist = geodist_points_lineseg(
        points[1:-1], start=points[0], end=points[-1], geod=geod
    )
    i_max = np.argmax(dist) + 1  # dist[i] = dist(points[i+1], line seg.)
    dist_max = dist[i_max - 1]

    return (
        np.concatenate(
            [
                filter(points[: i_max + 1], threshold)[:-1],
                filter(points[i_max:], threshold),
            ]
        )
        if dist_max > threshold
        else np.array(
            [True] + [False] * (n_points - 2) + [True],
        )
    )
