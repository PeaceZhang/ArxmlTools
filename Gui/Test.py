import glob
import os
def find_files_recursive(folder_path, file_extension):
    pattern = os.path.join(folder_path, f"**/*.{file_extension}")
    file_list = glob.glob(pattern, recursive=True)
    return file_list

# 例子：递归查找当前目录下所有的 .txt 文件
folder_path = "D:\AutosarTutorial\ArxmlTools\Export"
file_extension = "arxml"
txt_files_recursive = find_files_recursive(folder_path, file_extension)

print("Found .txt files recursively:")
for file in txt_files_recursive:
    print(file)

