# Archive

本目录存放**阶段一红线外、已宣布取消**的代码，保留可追溯，但不再维护。

## 内容

- `frontend-interview-agent/` —— 智能面试助手的前端（Vue3）+ 后端（Flask）应用骨架
- `backend/` —— 站内判题微服务骨架（Java）

## 为什么归档

- `.claude/rules/phase-gate.md` 明确：**阶段一不做判题微服务**
- `docs/changelog.md` 已宣布：取消站内判题，改走 LeetCode 跳转
- 这两块是死代码，留在主干会误导维护（看着像在做）

归档不等于删除，git 历史仍可完整追溯。后续若启动判题功能（阶段三），可从 archive 取出重启。
