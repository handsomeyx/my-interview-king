# 提交纪律清单

> 触发：每次 `git commit` 前过一遍。
> 目的：堵住"几周不提交、未跟踪文件堆积、一次误操作清零"的病。

## 提交前 checklist

- [ ] 这次改动是一个**可独立说明**的单元？（不是"做了一堆"，是"做完一件"）
- [ ] `git status` 看过，没有混入无关文件 / 缓存 / 密钥？
- [ ] 涉及的未跟踪文件都已 `git add <具体路径>`？（尤其新 `.vue` 组件、新 `.md` 文档）
- [ ] commit message 说清「为什么改」，不只说「改了什么」？

## 频率红线

- [ ] 距上次 commit 不超过 1 个工作日？（超过 → 现在就提）
- [ ] 没有 > 2 天未提交的工作沉淀在本地？（有 → 立刻提，哪怕拆成几次）

## 绝不提交（gitignore 应覆盖，提交前再核一遍）

- [ ] `.env`、密钥、token、`*.key`
- [ ] `node_modules/`、`target/`、`.vitepress/cache/`、`.npm-cache/`
- [ ] `docs.backup-*/`、本地数据库文件 `*.db`

## message 格式

`类型: 简述`，类型用 `docs` / `feat` / `fix` / `refactor` / `chore`。

好例子：`docs(java): 补充 JVM 内存模型 4 篇`
坏例子：`update`（没说为什么，也没说改了啥）

## 关于 push（远程在 GitHub handsomeyx/my-interview-king）

- push 到远程前，在本机确认走代理：`HTTPS_PROXY` 需在**同一条命令**里设置（端口 7897）。
- main 分支不 force push。
