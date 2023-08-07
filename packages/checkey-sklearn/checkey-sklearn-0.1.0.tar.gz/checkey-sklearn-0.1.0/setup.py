from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = """
自己平时会使用的一些统计学和数学模型,目前有两个改进的朴素贝叶斯算法和一个TOPSIS
"""
LONG_DESCRIPTION = """
# 使用说明

自己平时会使用的一些统计学和数学模型,目前有两个改进的朴素贝叶斯算法和一个TOPSIS

GitHub: [https://github.com/CheckeyZerone/Checkey-Sklearn](https://github.com/CheckeyZerone/Checkey-Sklearn)

PyPI: [https://pypi.org/project/checkey-sklearn/](https://pypi.org/project/checkey-sklearn/)

## 版权声明
    Checkey-Sklearn
    Copyright (C) 2023  CheckeyZerone

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

## 安装方法
```commandline
pip install chlearn
```

## 依赖的第三方模块包

```
numpy
pandas
scikit-learn
```

## 实现算法

- 朴素贝叶斯改进
- 熵权-TOPSIS模型

## 使用方法

```python
model = Model(*params)
model.fit(x_train[, y_train, params])
model.predict(x_test)  # or model.transform(x_test)
```

"""


setup(
    name='checkey-sklearn',
    version=VERSION,
    author='Checkey01',
    author_email='Chiaki2048@outlook.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'scikit-learn'],
    keywords=['Machine Learning', 'Python']
)
