import os
import re
import glob 
from cgai_io import copyfile



class CGAIPATH(object):

    def __init__(self):
        pass



    def isSequence(self,path,_type=''):
        """
        判定该路径是否为一个序列路径
        path: 输入文本路径
        _type: 可以指定文件类型,需带.,不指定则全部识别 比如： .exr 
        """
        result = False
        pt = '(.*)(%\d+d).*' if not _type else '(.*)(%\d+d).*\\'+_type
        groups = re.match(pt,path)
        try:
            pre = groups.group(1)
            patter = groups.group(2)
            result = pre,patter
        except Exception as ERR:
            print(ERR)
        
        return result

    def get_pnum(self,patter):
        """
        获取匹配中的字符数值
        """
        result = False
        try:
            g = re.match('.*%(\d+).*',patter)
            result = g.group(1)
        except Exception as NUMERR:
            print(NUMERR)

        return result

    def get_no_version_name(self,path,ignores=['.','_']):
        """
        获取去除版本的文件名称
        """
        fullname = os.path.basename(path)
        result = False
        try:
            g = re.match('(.*)(v\d+)',fullname)
            result = g.group(1)
            if result[-1] in ignores:
                result = result[:-1]
        except Exception as VERR:
            result = os.path.splitext(fullname)[0]

        return result


    def get_files(self,path,missing=False):
        """
        获取路径下的所有文件路径
        """
        fpaths = []
        missing_files = []
        result = self.isSequence(path)
        if result:  # 序列路径
            pre,patter = result
            dir_path,file_name = os.path.split(path)
            count = int(self.get_pnum(patter))
            file_name = file_name.replace(patter,'?'*count) 
            fs = glob.glob(os.path.join(dir_path,file_name))
            fpaths = sorted(fs)
            if missing:
                missing_files = self.get_missing_files(path,patter,fpaths)
                
        else:
            if os.path.isdir(path): # 目录
                fpaths = [os.path.join(path,i) for i in path if os.path.isfile(os.path.join(path,i))]
            elif os.path.isfile(path): # 本身是文件
                fpaths = [path]
        if missing:
            return fpaths,missing_files
        else:
            return fpaths

    def get_filename(self,path,ignores=['.','_']):
        """
        传入路径获取当前文件除去序列的名称
        path : 传入的路径
        ignores: 忽略的前缀
        """
        filename = ''
        if os.path.isfile(path):
            filename = os.path.basename(path)
            return os.path.splitext(filename)[0]
        result = self.isSequence(path)
        if result:
            pre,patter = result
            name = os.path.basename(pre)
            if name[-1] in ignores:
                filename = name[:-1]

        return filename




    def get_missing_files(self,ori_path,patter,paths):
        """
        注意： 获取缺失文件，必须是序列
        获取缺失的文件路径
        ori_path: 原始格式化路径
        patter: 匹配格式
        paths: 查询到的当前所有文件路径
        """
        pre,_tail = ori_path.split(patter)
        numbers = []
        for path in paths:
            number = path.replace(pre,'').replace(_tail,'')
            numbers.append(int(number))
        if numbers:
            min_num = min(numbers)
            max_num = max(numbers)
            miss_files = []
            for i in range(min_num,max_num+1):
                upath = pre + patter%i + _tail
                if upath not in paths:
                    miss_files.append(upath)

        return miss_files






    def repadding(self,src_dir,des_dir,padding=4):
        """
        输入目录将文件重命名,同时指定补零位置
        eg：  D:/A/out1.png  ->  D:/A/out0001.png
        """
        files = os.listdir(src_dir)
        try:
            
            for i in files:
                print(i)
                g = re.match('(.*\D)(\d+)(\..*)',i)
                pre = g.group(1)
                num = g.group(2)
                _type = g.group(3)
                patter = pre + '%0'+str(padding)+'d' 
                new_name = patter%int(num) + _type
                new_path = os.path.join(des_dir,new_name)
                copyfile(os.path.join(src_dir,i),new_path,True)

        except Exception as NUM_ERR:
            print(NUM_ERR)


        