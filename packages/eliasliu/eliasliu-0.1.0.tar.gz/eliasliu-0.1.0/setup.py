# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:31:31 2023

@author: Elias.Liu
"""

from setuptools import setup, find_packages

setup(
    name='eliasliu',  # 包名
    version='0.1.0',  # 版本号
    description='A brief description of your package',  # 包的简要描述
    author='Elias Liu 刘益廷',  # 作者名称
    author_email='liuyiting120@126.com',  # 作者邮箱
    packages=find_packages(),  # 包含的包列表
    install_requires=[],  # 依赖的其他包（如果有）
    classifiers=[  # 包的分类标签
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
