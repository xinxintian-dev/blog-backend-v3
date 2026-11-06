


class FakeCache:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    # 修正拼写，测试里用的通常是 set
    def set(self, key, value, *args, **kwargs): 
        self.data[key] = value

    # 如果真实环境用的是 setex，也可以留着，但参数要对应
    def setex(self, key, time, value):
        self.data[key] = value

    # 补上 delete 方法！
    def delete(self, key):
        self.data.pop(key, None)

    # 补上 incr 方法（如果有测浏览量递增的话）
    def incr(self, key):
        self.data[key] = int(self.data.get(key, 0)) + 1

     # 补上 expire 这个方法！
    def expire(self, key, seconds):
        return True # 假装设置成功