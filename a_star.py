"""
A* アルゴリズムを使用し、最短経路を求める
条件は以下の通り
    - 斜め移動禁止
    - 隣のマスへの移動コストは全て１
"""

__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

import csv

from node import Node
from status import Status

OBSTACLE_CODE = '-1'
NODES_DICT_KEY_TEMPLATE = "%d,%d"  # ノードを格納する辞書のキーを作成するためのテンプレート

class AStar:
    def __init__(self, f_name="map.csv", show_process=True):
        """
        Parameters
        ----------
        f_name : string
            マップファイル（CSV）
        """
        self.load_map(f_name)
        self.map_size_row = len(self.map_data)
        self.map_size_col = len(self.map_data[0])
        self.show_process = show_process
        self.start = (-1, -1)
        self.goal = (-1, -1)
        if self.show_process:
            print("file_name: %s" % f_name)
            print("size: [%s, %s]" % (self.map_size_col, self.map_size_row))

    def search(self, s, g, heuristics_func):
        """
        経路を探索して返す

        Parameters
        ----------
        s : iterable
            座標（要素数２、int型）、[x, y]の順
        g : iterable
            座標（要素数２、int型）、[x, y]の順
        heuristics_func : function
            ヒューリスティクス関数
        
        Returns
        -------
        route_coordinate : list
            経路（tuple型の座標のリスト）
        """
        self.start = tuple(s)
        self.goal = tuple(g)
        self.heuristics_func = heuristics_func
        if self.show_process:
            print("heuristics_name: %s" % self.heuristics_func.__name__)
            print("start: [%d, %d]" % self.start)
            print("goal: [%d, %d]" % self.goal)

        self.nodes_dict = {}  # 作成済みノード（フラグで管理しても良い）

        # スタート地点のノードを作成
        cost_h = self.heuristics_func(self.start, self.goal)
        start_x, start_y = self.start
        key = NODES_DICT_KEY_TEMPLATE % (start_x, start_y)
        start_node = Node(start_x, start_y)
        start_node.set_heuristics_cost(cost_h)
        start_node.set_actual_cost(0)
        self.opened_list = [start_node]
        self.nodes_dict[key] = start_node

        goal_node = None
        while len(self.opened_list) != 0:
            node = self.opened_list.pop(0)
            node.set_status(Status.CLOSED)
            if node.get_coordinate() == self.goal:
                goal_node = node
                break
            self.open_nodes(node)
        if self.show_process:
            if goal_node == None: print("result: failed")
            else: print("result: success")
        route_node = self.trace_node(node)
        route_coordinate = list(map(lambda node: node.get_coordinate(), route_node))
        route_coordinate.reverse()
        return route_coordinate

    def trace_node(self, node):
        """
        当該ノードからスタートまでたどった結果を返す

        Parameters
        ----------
        node : Node
            基準ノード（Nodeクラスのインスタンス）
        
        Returns
        -------
        route : tuple
            Nodeクラスのインスタンスのリスト
        """
        route = [node]
        while node.get_parent_node() != None:
            node = node.get_parent_node()
            route.append(node)
        return route

    def open_nodes(self, parent_node):
        """
        親ノードの周辺ノードをOpenし、パラメータを設定する
        その後、openのリストをソートする

        Parameters
        ----------
        parent_node : Node
            基準ノード（Nodeクラスのインスタンス）
        """
        pivot_x, pivot_y = parent_node.get_coordinate()
        coordinates = [(pivot_x-1, pivot_y), (pivot_x+1, pivot_y), (pivot_x, pivot_y-1), (pivot_x, pivot_y+1)]
        for x_tmp, y_tmp in coordinates:
            key = NODES_DICT_KEY_TEMPLATE % (x_tmp, y_tmp)
            if self.map_data[y_tmp][x_tmp] == OBSTACLE_CODE: continue
            if not key in self.nodes_dict:
                cost_h = self.heuristics_func((x_tmp, y_tmp), self.goal)
                cost_a = parent_node.get_actual_cost() + 1  # ノードによって移動コストを変えることもデキル
                node_tmp = Node(x_tmp, y_tmp)
                node_tmp.set_parent_node(parent_node)
                node_tmp.set_heuristics_cost(cost_h)
                node_tmp.set_actual_cost(cost_a)
                # node_tmp.calc_total_cost()
                self.opened_list.append(node_tmp)
                self.nodes_dict[key] = node_tmp
        # 実コストとヒューリスティックコストの合計でソートする
        self.opened_list.sort(key=lambda n: n.get_total_cost())

    def print_map(self, data=None, title=None):
        """
        迷路をコマンドラインに表示する
        """
        if data == None: data = self.map_data
        if title != None: print("\n%s" % title)
        for row in range(self.map_size_row):
            for col in range(self.map_size_col):
                cell = data[row][col]
                if cell == OBSTACLE_CODE: print("|||", end='')
                elif self.start == (col, row): print("'S'", end='')
                elif self.goal == (col, row): print("'G'", end='')
                else: print("   ", end='')
            print('')  # 改行を入れる

    def load_map(self, f_name="map.csv"):
        """
        マップを読み込む

        Parameters
        ----------
        f_name : string
            マップファイル（CSV）
        """
        with open(f_name) as f:
            reader = csv.reader(f)
            self.map_data = [row for row in reader]
    
    def get_map_size(self):
        """
        マップのサイズを取得する

        Returns
        -------
        size : tuple
            (col:int, row:int)の順
        """
        return (self.map_size_col, self.map_size_row)
