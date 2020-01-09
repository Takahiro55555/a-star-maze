"""
A* アルゴリズムを使用し、最短経路を求める
"""

__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

from a_star import AStar

def main():
    heuristics_func_list = [calc_euclidean_distance]
    
    print("# 読み込むファイル名を入力してください(何も入力しない場合はmap.csvの読み込みを試みます)")
    f_name = input()
    if f_name == '': a_star = AStar()
    else: a_star = AStar(f_name=f_name)

    a_star.print_map()

    print("# スタートの位置を空白区切りで入力してください(X, Yの順)")
    start = tuple(map(int, input().split()))
    print("# ゴールの位置を空白区切りで入力してください(X, Yの順)")
    goal = tuple(map(int, input().split()))
    print("# 使用するヒューリスティクス関数を以下の番号から指定してください")
    for i in range(len(heuristics_func_list)):
        print("#     %d: %s" % (i, heuristics_func_list[i].__name__))
    func_index = int(input())
    
    route = a_star.search(start, goal, heuristics_func_list[func_index])

    for x, y in route:
        print("(%s, %s) ->" % (x, y), end="")
    print("")


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