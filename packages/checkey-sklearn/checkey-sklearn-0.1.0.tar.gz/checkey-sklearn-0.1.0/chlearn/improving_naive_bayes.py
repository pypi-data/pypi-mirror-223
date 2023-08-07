import pandas as pd
import numpy as np
from sklearn.naive_bayes import CategoricalNB


# TODO 在未来的版本中，AVFWNB的类名会修改，同时会将原有的AVFWNB替换为基于scikit-learn的AVFWNB
class AVFWNB:
    def __init__(self,
                 alpha=1,
                 w_judge=True):
        """
        the __init__ of AVFWNB
        :param alpha: The Bayes estimates number, which is Laplacian smoothing alpha == 1.
        :param w_judge: Whether compute weight
        """
        self.__alpha = alpha
        self.__class_prior_flag = True
        self.__feature_prior_flag = True
        self.__f_flag = True
        self.__w_flag = True
        self.__w_judge = w_judge
        self.error_flag = False

    def fit(self,
            x,
            y):
        """
        Train the model by x and y
        :param x: the attribute matrix of instance
        :param y: the class of instance
        :return: None
        """
        self.__x = pd.DataFrame(x)
        self.__y = pd.Series(y)
        self.__get_w(x)
        self.__get_class_prior(y)  # compute P(Y_i == c_j)
        self.__get_feature_prior(x, y)
        # return self.__class_prior

    def __get_class_prior(self,
                          y: pd.Series) -> np.ndarray:
        # TODO: P(C)和P（a_j | c）同时计算可以优化算法
        """
        Compute the Laplacian smoothing of P(Y_i == c_j).
        :param y: the class of instance
        :return: the Laplacian smoothing of P(Y_i == c_j)
                 such as:
                               class_counts
                 No            0.361985
                 Yes           0.638015
                 the first column is the name of class, the second column is P(Y_i == c_j)
        """
        # y_value_counts = y.value_counts()  # the number of one class
        y_value_counts = pd.DataFrame(data=None,
                                      index=pd.unique(y),
                                      columns=['class_counts'])  # the number of one class with weights
        for i in y_value_counts.index:
            y_value_counts.loc[i, :] = np.dot(y == i, self.__w)
        y_count = float(self.__w.sum())  # the number of all class with weights
        self.__class_prior = (y_value_counts + self.__alpha) / (y_count + self.__alpha * float(y.nunique()))
        self.__class_prior_flag = False
        return self.__class_prior

    def __get_w(self,
                x: pd.DataFrame) -> np.ndarray:
        """

        :param x: the attribute matrix of instance
        :return: the weight of every instance
        """
        self.__w = pd.DataFrame(index=x.index, columns=['w'])
        # self.__w.w = 1

        if self.__w_judge:
            n = np.array([x[i].nunique() for i in x.columns])
            # print(n)
            self.__w = np.dot(self.__get_f(x), n)
        else:
            self.__w.w = 1
        self.__w = np.reshape(np.array(self.__w), (-1, ))
        self.__w_flag = False
        return self.__w

    @property
    def w(self) -> np.ndarray:
        """
        to get the weight beside the AVFWNB class
        :return: a np.ndarray w
        """
        if self.__w_flag:
            raise ValueError
        else:
            return self.__w

    @property
    def class_prior(self) -> pd.Series:
        """
        to get the P(Y_i == c_j) beside the AVFWNB class
        :return: a dataframe P(Y_i == c_j)
        """
        if self.__class_prior_flag:
            raise ValueError
        else:
            return self.__class_prior

    def __get_feature_prior(self,
                            x: pd.DataFrame,
                            y: pd.Series) -> dict:
        """
        compute the Laplacian smoothing of P(X^(j) = a_jl | Y = c_k)
        :param x: the attribute matrix of instance
        :param y: the class of instance
        :return: the Laplacian smoothing of multipy(P(X^(j) = a_jl | Y = c_k)) with weight
                 such as:
                 {
                     'Outlook':
                                     No       Yes
                     Sunny     0.571865  0.234234
                     Overcast  0.042813  0.410811
                     Rain      0.385321  0.354955,
                     'Temperature':
                                 No       Yes
                     Hot   0.379205   0.21982
                     Mild  0.415902  0.459459
                     Cool  0.204893  0.320721,
                     'Humidity':
                                   No       Yes
                     High    0.785942  0.345656
                     Normal  0.214058  0.654344,
                     'Windy':
                                   No       Yes
                     Weak    0.428115  0.669131
                     Strong  0.571885  0.330869
                 }
                 The first dim is the attribute of instance,
                 the second dim is the value of instance's attribute,
                 the third dim is the value of instance's class name.
        """
        self.__feature_prior = dict()
        for i in x.columns:
            # prior.index is the attribute of the i column in x
            # prior.column is the class in y
            prior = pd.DataFrame(data=None, index=pd.unique(x[i]), columns=pd.unique(y))
            for j in prior.columns:
                for k in prior.index:
                    # self.__w is the weight of every figure.
                    # (x[i] == k) is sigma(a_ij, a_j), x[i] is a_i.
                    ##################################################
                    ## test code
                    # print(np.array(((x[i] == k) & (y == j))))
                    # print(self.__w.shape)
                    ##################################################
                    prior.loc[k, j] = (self.__w.dot(((x[i] == k) & (y == j)).astype(float)) + self.__alpha) / (np.dot(self.__w, y == j) + len(prior.index))
            self.__feature_prior[i] = prior
        self.__feature_prior_flag = False
        return self.__feature_prior

    @property
    def feature_prior(self):
        """
        to get P(a_ij | c) beside the AVFWNB class
        :return: a dict P(a_ij | c)
        """
        if self.__feature_prior_flag:
            raise ValueError
        else:
            return self.__feature_prior

    def __get_f(self,
                x: pd.DataFrame) -> pd.DataFrame:
        """
        get f_ij to compute w
        :param x: the attribute matrix of instance
        :return: f_ij
        """
        self.__f = pd.DataFrame(data=None, index=x.index, columns=x.columns)
        for i in self.__f.index:
            for j in self.__f.columns:
                self.__f.loc[i, j] = sum(x.loc[:, j] == x.loc[i, j]) / x.shape[0]
        self.__f_flag = False
        return self.__f

    @property
    def f(self):
        """
        to get f_ij beside the AVFWNB
        :return: a dataframe f_ij
        """
        if self.__f_flag:
            raise ValueError
        else:
            return self.__f

    def predict(self,
                x: pd.DataFrame) -> np.ndarray:
        """
        predict the class of x[i, :]
        :param x: the instance matrix to predict
        :return: np.ndarray the class of all instance
        """
        ret: pd.DataFrame = pd.DataFrame(data=None, index=x.index, columns=pd.unique(self.__y))
        for k in ret.index:
            for i in ret.columns:
                prod = 1
                for j in x.columns:
                    # try:
                    #     prod *= float(self.__feature_prior[j].loc[x.loc[k, j], i])
                    # except KeyError:
                    #     prod *= 0
                    #     self.error_flag = True
                    prod *= self.__test_feature_prior(j, x.loc[k, j], i)

                    # print(my_model.feature_prior[j].loc[test_data.loc[k, j], i])
                # ret.append(my_model.class_prior.loc[i, :] * prod)
                # FIXME: 如果测试集中的分类没有出现在训练集中，会出现计算错误
                # test_class_prior = self.__class_prior.loc[i, :]
                test_class_prior = self.__test_class_prior(i)
                ret.loc[k, i] = float(test_class_prior * prod)
        ret: np.ndarray = np.array(ret.astype(float).idxmax(axis=1))
        return ret

    def __test_feature_prior(self, feature_name, feature_value, class_name) -> float:
        """
        count P(a_ij | c) of test instance
        :param feature_name: a_i.'s name
        :param feature_value: a_ij's value
        :param class_name: c's name
        :return: P(a_ij | c) of test instance
        """
        if (feature_value in self.__x[feature_name].unique()) and (class_name in self.__y.unique()):
            ret = float(self.__feature_prior[feature_name].loc[feature_value, class_name])
        else:
            ret = float(self.__alpha / (np.dot(self.__y == class_name, self.__w) + self.__x[feature_name].nunique() * self.__alpha))
        return ret

    def __test_class_prior(self, class_name):
        """
        count P(c) of test instance
        :param class_name: c's name
        :return: P(c) of test instance
        """
        if class_name in self.__y.unique():
            ret = self.__class_prior.loc[class_name, :]
        else:
            ret = self.__alpha / (self.__w.sum() + self.__y.nunique() * self.__alpha)
        return ret


class SklearnAVFWNB(CategoricalNB):
    def __init__(self, *, alpha=1.0, fit_prior=True, class_prior=None, min_categories=None):
        super().__init__(alpha=alpha, fit_prior=fit_prior, class_prior=class_prior, min_categories=min_categories)
        self.__w_flag = True
        self.__f_flag = True

    def fit(self, X, y):
        super().fit(X, y, sample_weight=self.__get_w(X))


    def __get_w(self, X):
        """
        compute the weight of every instance
        :param x: the attribute matrix of instance
        :return: the weight of every instance
        """
        x = pd.DataFrame(X)
        self.__w = pd.DataFrame(index=x.index, columns=['w'])
        # self.__w.w = 1
        n = np.array([x[i].nunique() for i in x.columns])
        # print(n)
        self.__w = np.dot(self.__get_f(x), n)
        self.__w = np.reshape(np.array(self.__w), (-1, ))
        self.__w_flag = False
        return self.__w

    @property
    def w(self) -> np.ndarray:
        """
        to get the weight beside the AVFWNB class
        :return: a np.ndarray w
        """
        if self.__w_flag:
            raise ValueError
        else:
            return self.__w

    def __get_f(self,
            x: pd.DataFrame) -> pd.DataFrame:
        """
        get f_ij to compute w
        :param x: the attribute matrix of instance
        :return: f_ij
        """
        self.__f = pd.DataFrame(data=None, index=x.index, columns=x.columns)
        for i in self.__f.index:
            for j in self.__f.columns:
                self.__f.loc[i, j] = sum(x.loc[:, j] == x.loc[i, j]) / x.shape[0]
        self.__f_flag = False
        return self.__f

    @property
    def f(self):
        """
        to get f_ij beside the AVFWNB
        :return: a dataframe f_ij
        """
        if self.__f_flag:
            raise ValueError
        else:
            return self.__f


# TODO `InstanceWeightedNB`的注释以后会进行修改
class InstanceWeightedNB(CategoricalNB):
    def __init__(self, alpha=1.0,
                 fit_prior=True,
                 class_prior=None,
                 min_categories=None):
        """
        alpha : float, default=1.0
            Additive (Laplace/Lidstone) smoothing parameter
            (0 for no smoothing).

        fit_prior : bool, default=True
            Whether to learn class prior probabilities or not.
            If false, a uniform prior will be used.

        class_prior : array-like of shape (n_classes,), default=None
            Prior probabilities of the classes. If specified, the priors are not
            adjusted according to the data.

        min_categories : int or array-like of shape (n_features,), default=None
            Minimum number of categories per feature.

        - integer: Sets the minimum number of categories per feature to
          `n_categories` for each features.
        - array-like: shape (n_features,) where `n_categories[i]` holds the
          minimum number of categories for the ith column of the input.
        - None (default): Determines the number of categories automatically
          from the training data.

        .. versionadded:: 0.24
        """
        super(InstanceWeightedNB, self).__init__(alpha=alpha,
                                                 fit_prior=fit_prior,
                                                 class_prior=class_prior,
                                                 min_categories=min_categories)

    def __get_w(self, X: np.ndarray) -> np.ndarray:
        self.__w: np.ndarray = self.__get_similarity(X) + 1
        # self.__w /= self.__w.sum()
        return self.__w

    @property
    def w(self):
        return self.__w

    def __get_mode(self, X: np.ndarray) -> np.ndarray:
        self.__mode: np.ndarray = np.array(pd.DataFrame(X).mode(axis=0).iloc[0, :])
        return self.__mode

    @property
    def mode(self):
        return self.__mode

    def __get_similarity(self, X: np.ndarray) -> np.ndarray:
        X = np.array(X)
        self.__get_mode(X)  # 计算众数向量
        # self.__similarity: np.ndarray = np.zeros(shape=(X.shape[0], X.shape[0]))
        self.__similarity: np.ndarray = np.zeros(shape=(X.shape[0],))
        # print(self.__mode)
        for i in range(self.__similarity.shape[0]):
            self.__similarity[i] = (X[i] == self.__mode).sum()
        # for i in range(self.__similarity.shape[0]):
        #     for j in range(i, self.__similarity.shape[1]):
        #         self.__similarity[i, j] = self.__similarity[j, i] = (X[i] == X[j]).sum()
        return self.__similarity

    @property
    def similarity(self) -> np.ndarray:
        return self.__similarity

    def fit(self, X, y):
        X = np.array(X)
        super(InstanceWeightedNB, self).fit(X, y, self.__get_w(X))