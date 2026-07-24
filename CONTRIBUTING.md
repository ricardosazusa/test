> # 开源贡献指南 (CONTRIBUTING)
> 
> 欢迎参与 dev-helper 的开发！请遵守以下协作规范：
> 
> ## 分工与 Issue 指南
> 1. 请先在 Issues 中领领属于你的任务。
> 2. 基于 `main` 分支拉取新的 Feature 分支，命名规范为：`feat/功能名`（如 `feat/time-convert`）。
> 3. 开发完成后，提交 Pull Request (PR) 到 `main` 分支。
> 4. PR 必须由至少一名组内成员 Review 通过后，由 Team Lead (成员 A) 进行 Merge。
> 
> ## 代码规范
> - 所有新子命令统一在 `cli.py` 中通过 `@cli.command()` 进行扩展。
> - 确保子命令带有简单的帮助文档（Docstring）。
> 
> ```
> 
> 
