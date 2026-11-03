# 多用户博客后端系统 (Blog Backend)

> 这是一个基于 **FastAPI** 和 **整洁架构 (Clean Architecture)** 开发的工业级博客后端项目。项目旨在解决传统开发中业务逻辑与底层框架强耦合的问题，并实现了读写分离、分布式锁、异步任务及接口限流等高阶功能。

## 技术栈

* **Web框架**：FastAPI, Uvicorn
* **数据库/ORM**：MySQL, SQLAlchemy (读写分离)
* **缓存/中间件**：Redis (缓存、分布式锁、JWT黑名单、接口限流)
* **异步任务**：Celery + Redis
* **测试/部署**：Pytest (单元测试), Docker, Docker Compose

## 架构设计 (整洁架构)

项目严格遵循“依赖只向内”的原则，分为四层：

* `api`: 路由层，处理 HTTP 请求、参数校验与依赖注入装配。
* `application`: 应用层，编排核心业务逻辑（Use Cases）。
* `domain`: 领域层，纯 Python 实现，定义实体（Entity）与抽象接口（Repository）。
* `infrastructure`: 基础设施层，实现具体的数据库、缓存、消息队列及第三方调用。

## 核心功能与亮点

1. **依赖注入与解耦**：利用 FastAPI `Depends` 机制，在 `deps.py` 中动态注入底层实现，业务层不依赖具体框架。
2. **读写分离**：通过配置双引擎，读操作路由至从库，写操作路由至主库。
3. **防缓存击穿**：手写 Redis 分布式锁（UUID + Lua脚本），保护从库免受高并发冲击。
4. **异步削峰**：使用 Celery 异步发送通知邮件，接口响应速度提升 90%。
5. **安全防护**：JWT 鉴权 + Redis Token 黑名单 + 基于 Redis 的接口限流器。
6. **毫秒级单元测试**：纯内存级测试，不依赖真实数据库环境。

## 快速启动 (Docker 部署)

1. 克隆项目并进入目录：

   ```bash
   git clone https://github.com/你的用户名/blog-backend-v3.git
   cd blog-backend-v3