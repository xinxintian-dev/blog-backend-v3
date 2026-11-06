import json
import time

from app.domain.article.repository import ArticleRepository
from app.domain.article.entity import Article
from app.domain.exceptions import DuplicateTitleError,ArticleNotFoundError,IsnullTitleError
from app.infrastructure.cache.redis_lock import RedisLock
from app.domain.notification.service import NotificationService
from app.domain.logging.acticon_logger import ActionLogger
class ArticleService:
    def __init__(
            self,
            repo:ArticleRepository,
            cache,
            notifier: NotificationService,
            action_logger: ActionLogger =None
            ):
        self.repo=repo  #只依赖接口
        self.cache=cache
        self.notifier=notifier
        self.action_logger=action_logger

    def _record_and_return(self, article: Article, article_id: int, user_id: int) -> Article:
        if self.action_logger:
            # 建议：这里最好是用异步发送（比如丢到消息队列），否则会阻塞主线程
            self.action_logger.log_view(user_id=user_id, article_id=article_id)
        return article
    
    def incr_views(self, article_id: int):
        article=self.repo.get_by_id(article_id)
        if not article:
            print(f"找不到文章{article_id},直接返回！")
            return
        
        # # 重点2：看看你要写的 key 到底是什么
        # key_name = f"article:views:{article_id}"
        # print(f"✅ 准备写入 Redis, key 为: {key_name}")
        
        # # 重点3：捕获异常，看看是不是 Redis 连不上
        # try:
        #     result = self.cache.incr(key_name)
        #     print(f"🎉 Redis 自增成功，当前值是: {result}")
        # except Exception as e:
        #     print(f"💥 写入 Redis 失败！错误信息: {e}")
            
        # 不查数据库，直接在 Redis 里原子自增(逻辑有错不能直接自增，如果数据库里没有呢)
        self.cache.incr(f"article:views:{article_id}")
        
    def create_article(self,title: str,content: str,author_id: int)->Article:
        if not title or not title.strip():  #需要考虑title字段被少传 和title为空 两种情况
            raise IsnullTitleError("文章标题不能为空")
        if self.repo.get_by_title(title):
            raise DuplicateTitleError("文章标题已存在")
        
        article=Article(
            id=None,
            title=title,
            content=content,
            author_id=author_id
            )
        
        save_article=self.repo.save(article)
        self.cache.delete("article_list_page_1")

        #创建文章，邮件通知
        self.notifier.send_new_article_email("author@test.com",article.title)
        
        return save_article

    def get_article(self,article_id: int,user_id: int)->Article:
        # article=self.repo.get_by_id(article_id)
        # if not article:
        #     raise ArticleNotFoundError("文章不存在")
        # return article

        #------分布式锁逻辑------

        cache_key=f"article:{article_id}"
        lock_key=f"lock:article:{article_id}"

        #用while True 代替递归
        while True:
            #1.先查缓存
            cache_data=self.cache.get(cache_key)
            if cache_data:
                article=Article(**json.loads(cache_data))
                return self._record_and_return(article,article_id,user_id)
            
            #2.缓存没命中，尝试获取分布式锁
            lock=RedisLock(self.cache)
            identifier=lock.acquire(lock_key)
            if identifier:
                #3.抢到锁，再次检查缓存（防止获取锁的间隙，别人已经重建了缓存）
                try:
                    cache_data=self.cache.get(cache_key)
                    if cache_data:
                        Article(**json.loads(cache_data))
                        return self._record_and_return(article,article_id,user_id)

                    #查库并回写
                    article=self.repo.get_by_id(article_id)
                    if not article:
                        raise ArticleNotFoundError("文章不存在")

                    #写入缓存（设置5 分钟过期）
                    self.cache.setex(cache_key,300,json.dumps(article.__dict__))

                    return self._record_and_return(article,article_id,user_id)
                    
                    return article
                finally:
                    #释放锁防止死锁
                    lock.release(lock_key,identifier)
            else:
                #没拿到锁的请求，不是去递归，等一会儿，然后通过continue 再次进入循环查缓存
                time.sleep(0.2)
                continue    #跳出本轮if，进入下一次while循环


        
        #----下面递归方法容易导致栈溢出
        # if cache_data:
        #     return Article(**json.loads(cache_data))

        # #缓存没命中，尝试获取分布式锁
        # lock=RedisLock(self.cache)
        # lock_key=f"lock:article:{article_id}"
        # identifier=lock.acquire(lock_key)
        # if identifier:
        #     try:
        #         #获取到锁，再次检查缓存（防止获取锁的间隙，别人已经重建了缓存）
        #         cache_data=self.cache.get(cache_key)
        #         if cache_data:
        #             return Article(**json.loads(cache_data))

        #         #查数据库
        #         article=self.repo.get_by_id(article_id)
        #         if not article:
        #             raise ArticleNotFoundError("文章不存在")

        #         #写入缓存（设置5 分钟过期）
        #         self.cache.setex(cache_key,300,json.dumps(article.__dict__))
        #         return article
        #     finally:
        #         #释放锁防止死锁
        #         self.lock.release(lock_key,identifier)
        # else:
        #     #没拿到锁的请求，自旋等待一会儿，然后递归调用自己重新查缓存
        #     time.sleep(0.5)
        #     return self.get_article(article_id)

