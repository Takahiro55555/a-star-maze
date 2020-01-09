"""
A* アルゴリズムを使用し、最短経路を求める
"""

__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

from a_star import AStar

def main():
    a_star = AStar()
    route = a_star.search((1, 1), (5, 6), calc_euclidean_distance)
    a_star.print_map()
    print(route)


def calc_euclidean_distance(s, g):
    """
    ２点間のユークリッド距離を算出

    Parameters
    ----------
    s : iterable
        座標（要素数２）、[x, y]の順
    g : iterable
        座標（要素数２）、[x, y]の順
    
    Returns
    -------
    distance : int
        ２点間の距離（小数点以下切捨）
    """
    return int(((s[0] - g[0])**2 + (s[1] - g[1])**2)**0.5)

if __name__ == "__main__":
    main()