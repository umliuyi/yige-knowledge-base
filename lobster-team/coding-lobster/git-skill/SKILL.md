# Git版本控制Skill

> 适用场景：代码提交、分支管理、代码回滚、协作开发
> 编程龙虾专用

---

## Git核心流程（4步）

### 第一步：理解当前状态
- git status 查看当前修改
- git diff 查看具体改动
- git log 查看提交历史

### 第二步：添加修改
- git add . 添加所有修改
- git add <文件> 添加特定文件

### 第三步：提交
- git commit -m '提交信息'
- 提交信息要简洁说明做了什么

### 第四步：验证
- git log --oneline -3 查看最近3条提交
- git status 确认工作区干净

---

## 常用命令

### 查看
git status
git log --oneline -5
git diff
git branch -a

### 提交
git add .
git commit -m 'feat: 添加新功能'
git push

### 分支
git branch <新分支名>
git checkout <分支名>
git checkout -b <新分支名>

### 回滚
git log --oneline -5
git revert <commit_id>
git reset --hard <commit_id>

---

## 编程龙虾输出规范

每次Git操作后汇报：
1. 执行的命令
2. 操作结果
3. 提交ID/分支名

## 注意事项
- 重要修改前先git branch备份
- 合并前git pull最新代码
- 不要提交敏感信息（密码/Token/Keys）
