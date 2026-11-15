# 发布 GBA-GCs 和 MCGC 到 Hugging Face

这里准备了两个独立 Hub 仓库的发布材料：`你的HF用户名/GBA-GCs`（dataset）和 `你的HF用户名/MCGC`（model）。账号尚未注册、尚未执行上传时，这些名称只是拟用仓库名。

## 1. 注册并验证邮箱

打开 https://huggingface.co/join ，本人完成注册、服务条款确认和邮箱验证。GitHub 账号不会自动成为 Hugging Face 账号，可以尽量使用一致的公开用户名。不要把密码或访问令牌粘贴到 GitHub Issue 或聊天中。

## 2. 在本机准备与登录

在包含本目录的 GBA-GCs 仓库根目录执行（Python 3.10+）：

```bash
python -m pip install -r hf_release/requirements.txt
hf auth login
```

`hf auth login` 的令牌输入只在你自己的终端中完成；使用仅满足目标仓库上传需求的权限。发布脚本使用已保存的本机登录，不将令牌写进输出目录。

## 3. 生成和核对发布目录

把 `YOUR_HF_USERNAME` 替换成你注册后的实际用户名：

```bash
python hf_release/publish.py prepare --namespace YOUR_HF_USERNAME
python hf_release/publish.py verify
```

默认输出 `.hf-release/`。准备步骤仅使用标准库，不需要登录，也不会上传。它校验公开来源文件的固定 SHA-256、记录数量、重复 ID、官方划分互斥性和完整覆盖，然后生成数据集卡、模型卡、原始公开数据副本、五组官方 CSV 划分和发布清单。查看 `.hf-release/dataset/README.md` 与 `.hf-release/model/README.md` 即可审阅最终页面文本。

`mainland` 是默认配置，使用 `all` 分区；`paper_v1` 是与论文数量一致的确定性公开子集，不能直接宣称是原始受控数据的逐条复制；`hk_macao` 是迁移诊断；广州人工标注和五组官方划分有单独配置。扩展版、子集和五组重复使用的标注数据不能相加作为独立样本数量。

## 4. 上传两个公开仓库并检查加载

下面的命令会下载约 1.72 GB 的原始模型权重，校验 GitHub Release 的 SHA-256，再将两个仓库公开发布到上一步指定的 HF 命名空间。预留至少约 4 GB 可用磁盘空间。

```bash
python hf_release/publish.py publish --download-checkpoint
```

如果本机已有原始 checkpoint，可避免重复下载：

```bash
python hf_release/publish.py publish --checkpoint /path/to/trimodal_io_fused_gba_full.pth
```

上传只允许清单中列出的文件。已有的私有目标仓库会触发停止，不会自动改为公开。脚本不会扫描或上传受控仓库，不会删除远端现有文件。登录或上传失败后可重试同一 `publish` 命令，现有完整且校验通过的模型文件会复用。

上传后脚本会重新从 Hub 加载全部九个数据配置，核对数量、官方划分顺序和每个单元格的值；检查模型远端文件名、大小和 Hub 返回的 SHA-256（如提供）。成功后输出两个实际仓库链接。随后打开数据集页面确认 Dataset Viewer 处理完成；不要把上传成功当成 Viewer 已验证。

模型采用 Niels 建议的 `hf_hub_download` 路线。当前仓库中的轻量参考网络与论文完整模型不同，因此这里不声称支持完整权重的 `from_pretrained`、直接推理或性能复现，也不为原始 checkpoint 编造架构配置。

## 5. 论文页面与后续回复

登录后打开 https://huggingface.co/papers/2609.03804 。若页面尚不存在，按提示索引论文，或在 Papers 页搜索 arXiv ID `2609.03804` 并选择索引入口。页面建立后点击自己的作者姓名，选择 `claim authorship` 并确认申请；通过后补充 GitHub 地址 https://github.com/MinweiZhao/GBA-GCs 。如需投稿 Daily Papers，再使用其提交入口。作者认领需要平台审核，提交不等于审核通过。

两张卡片都包含 `arxiv:2609.03804` 标签及数据集/模型互链。数据和 checkpoint 验证成功后，将实际 Hub 链接补充到 https://github.com/MinweiZhao/GBA-GCs/issues/1 ，再更新主 README 的下载入口。

参考官方文档：[上传数据集](https://huggingface.co/docs/hub/datasets-adding)、[数据配置](https://huggingface.co/docs/datasets/repository_structure)、[上传模型](https://huggingface.co/docs/hub/models-uploading)、[论文页面](https://huggingface.co/docs/hub/paper-pages)。
