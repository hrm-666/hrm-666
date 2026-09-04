# Resumes

这个目录采用最直接的管理方式：

- `original-template/`：原始通用模板
- `huawei-adn-llm/`：面向华为 ADN 大模型方向的定制版

后续新增场景时，直接复制一个现有子文件夹，重命名后在该文件夹内修改 `main.tex` 即可。

## 推荐用法

1. 复制 `original-template/` 为新的目标文件夹
2. 在新文件夹里修改 `main.tex`
3. 用 `xelatex main.tex` 编译

每个版本都独立维护，互不影响。
