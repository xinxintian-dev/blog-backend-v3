import pytest
from app.application.services.article_service import ArticleService
from tests.fakes.fake_article_repo import FakeArticleRepository
from app.domain.exceptions import IsnullTitleError, ArticleNotFoundError, DuplicateTitleError
from tests.fakes.fake_cache import FakeCache
from tests.fakes.fake_notifier import FakeNotificationService
# pytest 的 fixture：帮我们在每次测试前生成一个干净的假仓库和 Service
import pytest
from unittest.mock import patch, MagicMock

# 自动拦截所有对 RedisLock 的请求
@pytest.fixture(autouse=True)  #做全局的mock拦截
def mock_redis_lock():
    with patch('app.application.services.article_service.RedisLock') as mock:
        # 模拟成功获取到锁
        mock_instance = MagicMock()
        mock_instance.acquire.return_value = "fake-lock-id"
        mock.return_value = mock_instance
        yield mock
        
@pytest.fixture
def article_service():
    fake_repo = FakeArticleRepository()  #每次测试都是一个空的新字典
    fake_cache=FakeCache()
    fake_notifier=FakeNotificationService()
    return ArticleService(repo=fake_repo,cache=fake_cache,notifier=fake_notifier)

# 测试 1：正常创建文章
def test_create_article_success(article_service):
    # 传入标题、内容、作者 ID
    article = article_service.create_article("测试标题", "内容", 1)
    assert article.title=="测试标题"
    #验证是否调用了通知器
    assert len(article_service.notifier.sent_emails) ==1

    # assert article.id == 1
    # assert article.title == "我的第一篇"
    # assert article.author_id == 1

# 测试 2：标题重复拦截（核心业务逻辑）
def test_create_article_duplicate_title(article_service):
    # 先创建第一篇
    article_service.create_article("重复的标题", "内容", 1)
    
    # 再创建同名文章，预期会抛出 ValueError
    with pytest.raises(DuplicateTitleError) as exc_info:
        article_service.create_article("重复的标题", "别的", 2)
    
    # 验证报错信息是否正确
    assert exc_info.value.args[0]=="文章标题已存在"

# 测试 3：查询不存在的文章
def test_get_article_not_found(article_service):
    with pytest.raises(ArticleNotFoundError) as exc_info:
        article_service.get_article(999,10)
    assert exc_info.value.args[0]=="文章不存在"
#测试 4：文章标题为空字符串
def test_create_article_isnull_title(article_service):
    
    with pytest.raises(IsnullTitleError) as exc_info:
        article_service.create_article("","内容",1)
    assert exc_info.value.args[0]=="文章标题不能为空"

    