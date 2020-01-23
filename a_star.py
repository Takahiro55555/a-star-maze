"""
A* アルゴリズムを使用し、最短経路を求める
条件は以下の通り
    - 斜め移動禁止
    - 隣のマスへの移動コストは全て１
    - 四方を壁によって完全に囲まれていること

標準出力は、リッチなビジュアライザーを作成する僅かな可能性に期待して、パースしやすいようにする
具体的なルールは以下の通り
    - パースのしやすさよりも見やすさのほうを優先
    - ビジュアライズに関係ない出力は「#」でコメントアウト
    - 表示するデータのラベルは半角英数字でスネークケース
    - 表示するデータラベルと実際のデータは「:」で区切る
    - 1行につき１つのデータ
    - スペースは適宜入れる
"""

__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

import csv

from node import Node
from status import Status

OBSTACLE_CODE = "-1"
OPENED_CODE = "-10"
CLOSED_CODE = "-20"
ROUTE_CODE = "-30"
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
            print("size: [%s, %s]" % (self.map_size_col-2, self.map_size_row-2))  # 壁を考慮
            print('')  # 改行を挿入

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

        counter = 0
        goal_node = None
        while len(self.opened_list) != 0:
            node = self.opened_list.pop(0)
            node.set_status(Status.CLOSED)
            self.open_nodes(node)
            if self.show_process:
                counter += 1
                title = "round: %s\n%s" % (counter, "open_nodes_cost: %s" % str(list(map(lambda n: n.get_total_cost(), self.opened_list))))
                self.print_map(data=self.gen_current_map(node), title=title)
                print('')  # 改行を挿入
            if node.get_coordinate() == self.goal:
                goal_node = node
                break
        if self.show_process:
            if goal_node == None: print("result: failed")
            else: print("result: success")
        route_node = self.trace_node(node)
        route_coordinate = list(map(lambda node: node.get_coordinate(), route_node))
        route_coordinate.reverse()
        return route_coordinate

    def gen_current_map(self, node):
        """
        現在の探索の様子を可視化するためのデータを生成する

        Parameters
        ----------
        node : Node
            現在の先頭ノード
            このノードからスタートまでの経路が現時点の経路として設定される
        
        Returns
        -------
        map_date : list
            生成結果
            self.print_map関数に渡すと良い感じに表示してくれる
        """
        # 参照渡しによるマップデータの破壊を防ぐ
        current_map_data = list(map(list, self.map_data))

        for key in self.nodes_dict:
            n = self.nodes_dict[key]
            status = n.get_status()
            x, y = n.get_coordinate()
            if status == Status.OPEN:
                current_map_data[y][x] = OPENED_CODE
            elif status == Status.CLOSED:
                current_map_data[y][x] = CLOSED_CODE
        traced_node_list = self.trace_node(node)
        for n in traced_node_list:
            x, y = n.get_coordinate()
            current_map_data[y][x] = ROUTE_CODE
        return current_map_data

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
        if node == None: return []
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
                cost_a = parent_node.get_actual_cost() + 1
                node_tmp = Node(x_tmp, y_tmp)
                node_tmp.set_parent_node(parent_node)
                node_tmp.set_heuristics_cost(cost_h)
                node_tmp.set_actual_cost(cost_a)
                # node_tmp.calc_total_cost()
                self.opened_list.append(node_tmp)
                self.nodes_dict[key] = node_tmp
            elif self.nodes_dict[key].get_status() != Status.CLOSED:
                cost_a = parent_node.get_actual_cost() + 1
                self.nodes_dict[key].set_actual_cost(cost_a)
        # ヒューリスティクスコストのでソートする
        self.opened_list.sort(key=lambda n: n.get_heuristics_cost())
        # 実コストとヒューリスティックコストの合計でソートする
        self.opened_list.sort(key=lambda n: n.get_total_cost())

    def print_map(self, data=None, title=None):
        """
        迷路をコマンドラインに表示する

        Parameters
        ----------
        data : iterable
            表示したい迷路データ。何も指定しない場合は、現在の迷路の状況を表示する

        title : str
            タイトルを設定する。（指定しなくてもOK）
        
        Returns
        -------
            None
        """
        if data == None: data = self.map_data
        if title != None: print("%s" % title)
        for row in range(self.map_size_row):
            for col in range(self.map_size_col):
                cell = data[row][col]
                key = NODES_DICT_KEY_TEMPLATE % (col, row)
                if cell == OBSTACLE_CODE: print("[||]", end='')
                elif self.start == (col, row): print("{SS}", end='')
                elif self.goal == (col, row): print("{GG}", end='')
                elif cell == OPENED_CODE: print("[%2d]" % int(self.nodes_dict[key].get_total_cost()), end='')
                elif cell == CLOSED_CODE: print("[XX]", end='')
                elif cell == ROUTE_CODE: print("[@@]", end='')
                else: print("[  ]", end='')
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
