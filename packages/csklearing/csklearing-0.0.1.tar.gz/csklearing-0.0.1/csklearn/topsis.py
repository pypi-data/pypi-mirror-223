import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class TOPSIS(BaseEstimator, TransformerMixin):
    def __init__(self,
                 weights: np.ndarray = None,
                 benefit: np.ndarray = None):
        """
        初始化
        :param weights: np.ndarray，初始权重，如果为`None`则使用熵权法进行计算
        :param benefit: np.ndarray，指标是正向的还是负向的，即指标越大越好还是越小越好，
                        True为正向，如果为`None`则全为正向，默认为`None`
        """
        self.weights = weights
        self.benefit = benefit
        self.__index = None

    def __check_default(self, X):
        if self.weights is None:
            self.weights = self.entropy_weight(X)
        if self.benefit is None: self.benefit = np.ones(X.shape[1], dtype=bool)

    def entropy_weight(self, X):
        p = np.array(X)
        # 计算熵值
        e = np.nansum(-p * np.log(p) / np.log(len(X)), axis=0)
        # 计算权系数
        return (1 - e) / (1 - e).sum()

    def __check_x(self, X):
        # if type(X) == type(pd.DataFrame(X)):
        if isinstance(X, pd.DataFrame):
            self.__index = X.index
        return np.array(X)

    def fit(self, X, y=None):
        X = self.__check_x(X)
        self.__check_default(X)
        self.n_samples, self.n_features = X.shape
        self.scores_ = np.zeros(self.n_samples)

        # 计算正负理想解
        self.ideal_best_ = np.zeros(self.n_features)
        self.ideal_worst_ = np.zeros(self.n_features)
        for i in range(self.n_features):
            if self.benefit[i]:
                self.ideal_best_[i] = np.max(X[:, i])
                self.ideal_worst_[i] = np.min(X[:, i])
            else:
                self.ideal_best_[i] = np.min(X[:, i])
                self.ideal_worst_[i] = np.max(X[:, i])

        # 计算距离矩阵
        self.dist_best_ = np.sqrt(np.sum((X - self.ideal_best_) ** 2, axis=1))
        self.dist_worst_ = np.sqrt(np.sum((X - self.ideal_worst_) ** 2, axis=1))

        # 计算得分
        self.scores_ = self.dist_worst_ / (self.dist_worst_ + self.dist_best_)
        return self

    def transform(self, X):
        check_is_fitted(self)
        ret = self.scores_.reshape(-1, 1)
        if self.__index is not None:
            ret = pd.DataFrame(ret, index=self.__index, columns=['scores'])
        return ret

    def summary(self):
        check_is_fitted(self)
        ret = pd.DataFrame(index=self.__index)
        ret['dist_best_'] = self.dist_best_
        ret['dist_worst_'] = self.dist_worst_
        ret['scores_'] = self.scores_
        return ret
