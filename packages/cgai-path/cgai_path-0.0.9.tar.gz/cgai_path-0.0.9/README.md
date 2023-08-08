#cgai-path


#### 功能

应用于CG行业的文件路径


#### 基本使用

```python
import os
from cgai_path import CGAIPATH



p = r'C:\PyOut\Test\test_hiero\v001\musk_%04d.exr'

cpath = CGAIPATH()

# 判断提供的路径是否为序列
result = cpath.isSequence(p)
print(result)  # ('C:\\PyOut\\Test\\test_hiero\\v001\\musk_', '%04d')

if result:
    filename = cpath.get_filename(p)
    print(filename)  # musk

# 获取文件序列
paths,missings = cpath.get_files(p)
print(paths) # ['C:\\PyOut\\Test\\test_hiero\\v001\\musk_0001.exr',...,'C:\\PyOut\\Test\\test_hiero\\v001\\musk_0049.exr']
print()
print(missings)


a = r'C:\PyOut\Test\test_hiero\v001\musk_0001.exr'

# 获取文件名称
filename = cpath.get_filename(a)
print(filename)  # musk_0001



```
