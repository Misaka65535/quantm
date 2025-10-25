__all__ = ['loaded_apis']

import os
import importlib
import traceback  # 输出错误信息，更好的纠错

loaded_apis: dict[str] = {}  # 这个字典用于保存加载好的插件对象
path = os.path.join("impl")
plugin_suffix = "py"  # 插件后缀为.py
file_in_impl_dir = os.listdir(path)  # 读取该目录下的的文件和文件夹


def pick_module(file_name: str):
    if file_name.endswith(plugin_suffix):  # 检查文件名后缀是否是.py
        return file_name.split(".")[0]  # 后缀是.py 就提取文件名
    else:
        return ""  # 后缀不是.py 就把这项置空


# 挑选出.py 为后缀的文件
py_file_in_impl_dir = map(pick_module, file_in_impl_dir)

# 去除列表中的空值
py_file_in_impl_dir = [_ for _ in py_file_in_impl_dir if _ != ""]

# 加载插件
for py_file_name in py_file_in_impl_dir:
    try:
        loaded_apis[py_file_name] = importlib.import_module(f"{py_file_name}")
    # 插件缺少依赖(ImportError 包括 ModuleNotFoundError)
    except ModuleNotFoundError:
        traceback.print_exc()  # 输出报错信息，包括行号之类的
        continue
    except ImportError:  # 其他的导入问题
        traceback.print_exc()
        continue
    except Exception as e:  # 兜底
        print(f"init_file_module inside Exception:{e}")
        traceback.print_exc()
        continue
