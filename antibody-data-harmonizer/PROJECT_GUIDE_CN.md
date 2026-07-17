# 从零开始使用这个 GitHub 项目

## 1. 先理解四个词

- **Repository / Repo（仓库）**：项目文件夹在 GitHub 上的版本。
- **Commit（提交）**：给当前一组修改拍一个带说明的快照。
- **Push（推送）**：把电脑上的提交上传到 GitHub。
- **README**：别人打开项目后首先看到的项目说明。

你不需要先学会命令行 Git。本项目建议新手使用：

1. GitHub 网页：展示和管理远程仓库。
2. GitHub Desktop：负责 commit 和 push。
3. VS Code 或 JupyterLab：实际修改代码和 Notebook。

## 2. 安装工具

在电脑上安装：

- Python 3
- GitHub Desktop
- VS Code
- VS Code 的 Python 和 Jupyter 扩展

也可以继续使用你已经熟悉的 Jupyter Notebook/JupyterLab。

## 3. 第一次在本地运行

1. 解压项目文件夹。
2. 打开 VS Code。
3. 选择 `File -> Open Folder`，打开整个
   `antibody-data-harmonizer` 文件夹，而不是只打开一个 `.ipynb`。
4. 打开 VS Code 的 Terminal。
5. 在项目根目录创建虚拟环境。

macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

6. 输入：

```bash
jupyter lab
```

7. 打开 `notebooks/01_demo_pipeline.ipynb`，从上到下运行。
8. 在项目根目录运行测试：

```bash
python -m pytest
```

## 4. 上传到 GitHub 的最简单方法

### GitHub Desktop 路径

1. 登录 GitHub Desktop。
2. 选择 `File -> Add Local Repository`。
3. 选择解压后的项目文件夹。
4. 如果提示该文件夹还不是 Git repository，选择创建 repository。
5. 在左下角 Summary 中写第一次提交信息，例如：

```text
Add initial antibody harmonization pipeline
```

6. 点击 `Commit to main`。
7. 点击顶部的 `Publish repository`。
8. 第一次建议先取消公开选项，发布为 **Private**。
9. 确认没有公司文件后，再考虑改为 Public。

以后每次工作循环都是：

```text
修改并保存文件
→ 在 GitHub Desktop 查看 Changes
→ 写 commit message
→ Commit to main
→ Push origin
```

## 5. 绝对不要上传的内容

- 公司真实抗体编码
- 真实序列
- 内部实验结果
- 未公开项目名称
- 内部表头或数据库结构（若其本身具有保密性）
- 原始 Excel
- 带有真实数据输出的 Notebook
- API key、账号、密码、服务器地址

`.gitignore` 已经设置为不上传 `data/raw/`、`data/processed/` 和
`outputs/` 中的内容，但你仍然要在每次 commit 前检查 GitHub Desktop
的 Changes 列表。

## 6. 你应该如何替换成自己的通用逻辑

不要直接复制公司的 Notebook。采用“从问题重新实现”的方式：

### 可以公开

- 通用 ID 清洗函数
- 通用列名标准化函数
- exact merge 和 unmatched report
- 特征序列搜索与标记
- 用虚构数据演示的相关性分析
- 对错误类型和 QC 方法的总结

### 不应公开

- 真实数据
- 内部命名规则的完整映射表
- 公司特有判定阈值
- 未公开业务结论
- 能反推出项目/分子的具体字段组合

## 7. 推荐的四周更新节奏

### Week 1：最小版本

- 跑通 sample 数据
- 理解文件夹结构
- 修改 README 中的个人项目说明
- 完成第一个 commit

### Week 2：ID harmonization

- 加入你实际遇到过的“通用错误类型”
- 例如大小写、空格、连接符和明确的链后缀
- 输出 matched、left_only、right_only、duplicates
- 写 2–3 个测试

### Week 3：feature locator

- 输入 motif 或 regex
- 输出 present、count、position、marked_sequence
- 将结果按 normalized antibody ID 合并回 assay table
- 做一个可视化或统计表

### Week 4：portfolio polish

- 清理 Notebook 输出
- 确保所有数据为 synthetic
- 增加流程图或结果截图
- 完善 README 的问题、方法、结果和局限
- 将仓库改为 Public（仅在确认安全后）

## 8. 建议的 commit 信息

每次只提交一个清楚的小变化：

```text
Add sample assay and Kabat tables
Add conservative antibody ID normalization
Add merge audit for unmatched records
Add sequence motif locator
Add CDR3 correlation summary
Add tests for ID harmonization
Improve README and privacy notes
```

## 9. 简历写法

项目完成后可以写成：

**Antibody Data Harmonization Pipeline | Python, pandas, Jupyter, GitHub**

- Built a reusable pipeline to standardize inconsistent antibody identifiers
  across assay and sequence-annotation tables, reducing manual reconciliation.
- Generated auditable matched, unmatched, and duplicate-ID reports and added
  sequence-feature counting, position tracking, and inline annotation.
- Prepared CDR3-length analyses against expression, HIC, and thermal stability
  using synthetic data and reproducible notebooks.

不要写无法量化或无法解释的夸张结果。等你实际用自己的工具节省了时间后，
再加入真实但不敏感的指标，例如 “reduced a 2-hour manual reconciliation
workflow to 10 minutes”。
