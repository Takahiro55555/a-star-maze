"""
迷路のノードを表現したクラス
"""

__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

from status import Status

class Node:
    def __init__(self, x, y):
        """
        迷路のノード（マス）を表すクラス

        Parameters
        ----------
        x : int
            x座標
        y : int
            y座標
        """
        self.x = x
        self.y = y
        self.status = Status.OPEN
        self.actual_cost = 0
        self.heuristics_cost = 0
        self.total_cost = 0  # 上記2つのコストを合計したもの（ソートの際に必要）
        self.parent_node = None

    def get_total_cost(self):
        """
        実コストとヒューリスティックコストの合計を求める

        Returns
        -------
        total_cost : int
            合計コスト
        """
        return self.actual_cost + self.heuristics_cost

    def get_coordinate(self):
        """
        座標を取得する

        Returns
        -------
        coordinate : tuple
            (x, y)の順
        """
        return (self.x, self.y)

    def get_actual_cost(self):
        """
        設定されている実コストを取得する

        Returns
        -------
        self.actual_cost : int
        """
        return self.actual_cost
    
    def set_actual_cost(self, cost):
        """
        実コストを設定する

        Parameters
        ----------
        cost : int
        """
        self.actual_cost = int(cost)

    def get_heuristics_cost(self):
        """
        設定されているヒューリスティックコストを取得する
        
        Returns
        -------
        self.heuristics_cost : int
        """
        return self.heuristics_cost
    
    def set_heuristics_cost(self, cost):
        """
        ヒューリスティックコストを設定する

        Parameters
        ----------
        cost : int
        """
        self.heuristics_cost = int(cost)

    def get_parent_node(self):
        """
        親ノードを取得する

        Returns
        -------
        self.parent_node : Node
            Nodeクラスのインスタンス
        """
        return self.parent_node
    
    def set_parent_node(self, node):
        """
        親ノードを設定する

        Parameters
        ----------
        node : Node
            Nodeクラスのインスタンス
        """
        self.parent_node = node

    def get_status(self):
        """
        ノードの状態を取得する

        Returns
        -------
        self.status : Status
        """
        return self.status

    def set_status(self, status):
        """
        ノードの状態を設定する

        Parameters
        ----------
        status : Status
            設定したいノードの状態
        """
        self.status = status
