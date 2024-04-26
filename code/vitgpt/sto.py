from django.core.files.storage import FileSystemStorage
import os

class mystorage(FileSystemStorage):
    def get_available_name(self, name, max_length=255):
        if self.exists(name):
            # 获取完整的文件路径
            full_path = self.path(name)

            # 删除已存在的文件
            os.remove(full_path)

        return name
