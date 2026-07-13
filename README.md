# Edge TTS Gateway

一个基于 **Microsoft Edge TTS** 的轻量级流式语音合成网关。

通过 HTTP API 调用 Edge 在线语音服务，将文字转换为自然语音，并支持流式音频输出。

适用于：

- Android TTS Server
- 阅读器朗读
- 有声书制作
- 自动化语音服务
- AI Agent 语音输出


## ✨ 特性

- 🚀 基于 FastAPI，高性能异步接口
- 🎧 支持音频流式返回
- 🌏 支持 Microsoft Edge TTS 全部语音
- 🔊 支持中文、英文、多语言声音
- 🐳 Docker 一键部署
- 📋 自动管理声音列表
- 💾 简单缓存机制
- ❤️ 提供健康检查接口
- 🔐 支持 HTTPS 反向代理部署
- ⚡ 低资源占用，适合家庭服务器运行


## 🏗️ 工作流程

```
客户端
  |
  | HTTP API
  |
Edge TTS Gateway
  |
  | edge-tts
  |
Microsoft Edge TTS Service
  |
音频流输出
```


## 📁 项目结构

```
edge-tts-gateway
│
├── app.py                 # FastAPI 主程序
├── config.py              # 配置文件
├── logger.py              # 日志模块
├── requirements.txt       # Python依赖
├── Dockerfile              # Docker镜像构建
├── docker-compose.yml      # Docker部署
├── README.md
├── LICENSE
│
├── services/
│   ├── edge.py             # Edge TTS核心服务
│   └── __init__.py
│
├── utils/
│   ├── cache.py            # 缓存处理
│   ├── param.py             # 参数处理
│   ├── response.py          # 响应处理
│   └── __init__.py
│
└── data/
    └── voices.json          # 声音列表缓存
```


# 🚀 快速开始


## Docker 部署


### 构建镜像

```bash
docker compose build
```


### 启动服务

```bash
docker compose up -d
```


### 查看日志

```bash
docker logs -f edge-tts-gateway
```


服务启动后：

```
http://localhost:3978
```


---

# 📡 API 接口


## 健康检查

GET

```
/health
```

返回：

```json
{
  "status": "ok"
}
```


---

## 获取声音列表

GET

```
/voices
```

返回当前支持的 Edge TTS 声音。


示例：

```json
[
  {
    "name": "zh-CN-XiaoxiaoNeural",
    "locale": "zh-CN",
    "gender": "Female"
  }
]
```


---

## 文本转语音

POST

```
/tts
```


请求：

```json
{
  "text": "你好，这是 Edge TTS 测试",
  "voice": "zh-CN-XiaoxiaoNeural"
}
```


返回：

```
audio/mpeg
```


示例：

```bash
curl \
-X POST \
-H "Content-Type: application/json" \
-d '{"text":"你好","voice":"zh-CN-XiaoxiaoNeural"}' \
http://localhost:3978/tts \
--output test.mp3
```


---

# 🌐 HTTPS 部署

推荐搭配：

- Caddy
- Cloudflare DNS
- 自有域名


示例：

```
用户
 |
HTTPS
 |
Caddy Reverse Proxy
 |
Edge TTS Gateway
```


Caddy 示例：

```caddy
edgetts.example.com {

    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }

    reverse_proxy 127.0.0.1:3978
}
```


---

# 📱 Android TTS Server

填写服务地址：

```
https://你的域名
```


接口：

```
/tts
```


声音：

例如：

```
zh-CN-XiaoxiaoNeural
```


即可使用 Edge TTS 作为在线语音服务。


---

# 🐳 Docker Compose 示例

```yaml
services:

  edge-tts-gateway:

    image: edge-tts-gateway:latest

    container_name: edge-tts-gateway

    ports:
      - "3978:3978"

    volumes:
      - ./data:/app/data

    restart: unless-stopped
```


---

# 🛠️ 技术栈

- Python 3.12
- FastAPI
- Uvicorn
- edge-tts
- Docker


---

# 🔮 Roadmap

计划支持：

- [ ] API Key 鉴权
- [ ] Web 管理界面
- [ ] 在线声音搜索
- [ ] 批量文本转语音
- [ ] EPUB 自动生成有声书
- [ ] 音频缓存优化
- [ ] 多用户管理


---

# 🤝 Contributing

欢迎提交 Issue 和 Pull Request。

如果这个项目对你有帮助，欢迎 Star ⭐


---

# 📄 License

MIT License


