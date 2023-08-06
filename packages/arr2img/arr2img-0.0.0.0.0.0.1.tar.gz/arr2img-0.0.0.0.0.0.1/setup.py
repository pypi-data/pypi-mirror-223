#!/GPFS/zhangli_lab_permanent/zhuqingjie/env/py3_tf2/bin/python
'''
@Time    : 20/11/05 下午 01:56
@Author  : zhuqingjie 
@User    : zhu
@FileName: setup.py
@Software: PyCharm
'''
import setuptools
import arr2img

''' 
🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣
🀥🀗🀐🀏🀎🀍🀌🀋🀊🀉
🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣
🀥🀗🀐🀏🀎🀍🀌🀋🀊🀉

'''

with open('requirements.txt') as f:
    req = [line.strip() for line in f.readlines() if line.strip()]

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="arr2img",
    version=arr2img.__version__,
    author="azzhu",
    author_email="zhu.qingjie@qq.com",
    description="Convert any numpy array to image so that you can show it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=req,
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
