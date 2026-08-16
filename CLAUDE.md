# 项目红线

> 本文件随仓库走，换电脑 / 换人都能读到。详细 SOP 见 `.claude/rules/`，按场景读，不碰不读。
> 仓库内任何代码 / 文档改动，都受本文件约束。

## 当前阶段

**阶段一 · 静态引流期**（定义见 `ROADMAP.md` 第三节）
**北极星**：站点上线 + 被搜索引擎收录。除此之外的事，默认不做。

## 四条触发式红线（每次开任务前自检）

### ① 越阶段了吗？

- [ ] 这个任务属于阶段一？
- [ ] 阶段一退出条件全部达成？（清单见 `.claude/rules/phase-gate.md` 的 G1）
- 任意一个 No → 读 `.claude/rules/phase-gate.md`，**别直接写代码**。

### ② 宣称属实吗？（写文档 / README / 首页 / commit message 时）

- [ ] 文中每个数字、状态、功能清单，都能从代码或文件推导出来？
- No → 改文案。不要出现"150+""即将上线""已实现"等不可核对的说法。

### ③ 推进北极星吗？

- [ ] 这件事是否直接推进上面的北极星？
- No 或拿不准 → 读 `.claude/rules/priority.md` 排队，**不动代码**。

### ④ 要生成文章内容吗？（写新文章 / 改写 / 扩写 / 写教程讲解）

- [ ] 已读 `.claude/rules/content.md`，并会按它的「生成后验收清单」逐条过？
- No → 先读 `.claude/rules/content.md` 再动笔。**这是强制规则，不是参考。** 生成的文章若通不过验收清单，视为未完成。

## 按场景读 SOP（不碰不读）

- 写 / 改 markdown 文章 → `.claude/rules/content.md` ✅ 已写
- 碰 `backend/` → `.claude/rules/backend.md`（待补）
- 碰 Vue 组件 / 前端 → `.claude/rules/frontend.md`（待补）
- 部署 / 上线 / CI → `.claude/rules/deploy.md`（待补）
- 沙箱 / 密钥 / 新依赖 → `.claude/rules/security.md`（待补）
- **每次 commit 前** → `.claude/rules/commit.md` ✅ 已写
- **不知道该做什么** → `.claude/rules/priority.md` ✅ 已写
- **越界判定** → `.claude/rules/phase-gate.md` ✅ 已写

（✅ = 已写；其余等真碰到那块时再补——不为没在做的事预先写规则。）
