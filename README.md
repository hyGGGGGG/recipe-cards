# Recipe Cards

一个极简的个人菜谱卡片站：Markdown 维护，Python 构建，GitHub Pages 展示。

## 新增菜谱

在 `recipes/` 下新建一个 Markdown 文件：

```md
# 红烧排骨

1. **煸**：热油炒姜，煎一面排骨，然后放香料
2. **烹**：烹白酒后小火调味
3. **炖**：1 小时
4. **收**：大火收汁，放青椒
```

约定非常简单：

- 第一条非空行必须是 `# 菜名`
- 后面只写有序步骤 `1. ...`
- 步骤中可用 `**文字**` 加粗
- 不使用标签、分类、数据库或前端框架

## 构建

```bash
python build.py
```

生成根目录的 `index.html`。

然后提交：

```bash
git add .
git commit -m "update recipes"
git push
```

## GitHub Pages

仓库 Settings → Pages：

- Source: Deploy from a branch
- Branch: `main`
- Folder: `/ (root)`

保存后即可使用 GitHub Pages 访问。
