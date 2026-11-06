from abc import ABC,abstractmethod

class ActionLogger(ABC):
    """行为日志记录接口（只管发，不管发给谁）"""

    @abstractmethod
    def log_view(self,user_id: int,article_id: int) ->None:
        """记录用户浏览文章的行为"""
        pass

