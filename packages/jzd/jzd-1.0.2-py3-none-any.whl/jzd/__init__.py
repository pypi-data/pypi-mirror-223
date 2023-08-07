import zipfile
import json
import tempfile
def load(jzdpath, classs):
    """
    从JZD文件中读取数据并返回解析后的字典对象。
    Args:
        jzdpath (str): JZD 文件路径
        classs (str): 类名
    Returns:
        dict: 解析后的字典对象
    """
    data = None
    with zipfile.ZipFile(jzdpath, 'r') as zip_file:
        with zip_file.open(f"{classs}.jzdc") as json_file:
            data = json.load(json_file)
    return data

def write(jzdpath, classs, data):
    """
    将JSON数据写入到ZIP文件中。
    Args:
        jzdpath (str): JZD 文件路径
        classs (str): 类名
        data (dict): 要写入的JSON数据字典对象
    """
    with zipfile.ZipFile(jzdpath, 'a') as zip_file:
        with zip_file.open(f"{classs}.jzdc", 'w') as json_file:
            json.dump(data, json_file)

def list_class(jzdpath):
    """
    列出JZD文件中的所有类名。
    Args:
        jzdpath (str): JZD 文件路径
    Returns:
        list: 所有类名列表
    """
    class_list = []
    with zipfile.ZipFile(jzdpath, 'r') as zip_file:
        for file_name in zip_file.namelist():
            if file_name.endswith('.jzdc'):
                class_name = file_name[:-6]
                class_list.append(class_name)
    return class_list

def delete_class(jzdpath, classs):
    """
    从JZD文件中删除指定的类。
    Args:
        jzdpath (str): JZD 文件路径
        classs (str): 要删除的类名
    Returns:
        bool: 如果成功删除类，则为True；否则为False
    """
    try:
        with zipfile.ZipFile(jzdpath, 'a') as zip_file:
            zip_file.extractall('temp')
            with zipfile.ZipFile(jzdpath, 'w') as new_zip_file:
                for file_name in zip_file.namelist():
                    if not file_name.startswith(f"{classs}."):
                        new_zip_file.write(f"temp/{file_name}", file_name)
        return True
    except:
        return False

def rename_class(jzdpath, old_name, new_name):
    """
    将JZD文件中的一个类名修改为另一个类名。
    Args:
        jzdpath (str): JZD 文件路径
        old_name (str): 要修改的旧类名
        new_name (str): 修改后的新类名
    Returns:
        bool: 如果成功修改类名，则为True；否则为False
    """
    try:
        temp_dir = tempfile.mkdtemp()  # 创建临时文件夹
        with zipfile.ZipFile(jzdpath, 'a') as zip_file:
            zip_file.extractall(temp_dir)
            with zipfile.ZipFile(jzdpath, 'w') as new_zip_file:
                for file_name in zip_file.namelist():
                    if file_name.startswith(f"{old_name}."):
                        new_file_name = file_name.replace(old_name, new_name)
                        new_zip_file.write(f"{temp_dir}/{file_name}", new_file_name)
                    else:
                        new_zip_file.write(f"{temp_dir}/{file_name}", file_name)
        return True
    except:
        return False