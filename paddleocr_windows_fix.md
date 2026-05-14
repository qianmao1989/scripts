# PaddleOCR Windows 安装踩坑记

## 背景

需要在 Windows 上用 PaddleOCR 做本地 OCR 识别。百度在线 API 能用，但本地方案更稳定、不走网络、准确率更高。

## 踩坑过程

### 第一次尝试：小助理装，崩了

小助理（OpenClaw）尝试直接在全局环境安装，把自己干崩了。原因：小助理没有终端操作权限，强行装依赖包会卡住。

### 第二次尝试：CC 装，卡死了

Claude Code 接手，默认用国外 PyPI 源下载，PaddlePaddle 包有 100MB+，直接卡死。

### 第三次尝试：成功

三板斧搞定：

#### 1. 虚拟环境隔离

```bash
mkdir -p D:/CherryAI_Workspace
python -m venv D:/CherryAI_Workspace/paddle_env
```

独立环境，不污染全局 Python，出问题直接删掉重建。

#### 2. 国内镜像加速

```bash
pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple
```

清华镜像源，下载速度从几 KB/s 提升到 30MB/s+。

#### 3. 降版本解决兼容性

PaddlePaddle 3.x + PaddleOCR 3.x 在 Windows 上有 oneDNN 兼容问题：

```
NotImplementedError: ConvertPirAttribute2RuntimeAttribute not support [pir::ArrayAttribute<pir::DoubleAttribute>]
```

最终可用组合：

| 组件 | 版本 |
|------|------|
| paddlepaddle | 2.6.2 |
| paddleocr | 2.9.1 |

## 测试结果

17 张图片测试：

- 精耐值准确率：100%
- 角色ID 全对率：60%
- 角色ID 可匹配修正：40%
- 角色ID 未识别（极短名）：2 张

结论：配合表格匹配，实际胜任率接近 100%。

## 经验总结

1. **虚拟环境**：Python 项目必须用 venv 隔离，别装全局
2. **国内镜像**：大包必用清华源，不然等到天荒地老
3. **降版本**：新版不一定好，稳定压倒一切
4. **任务边界**：AI 助手分工明确，环境安装交给有终端权限的工具

## 环境配置

```bash
# 激活环境
source D:/CherryAI_Workspace/paddle_env/Scripts/activate

# 验证安装
python -c "from paddleocr import PaddleOCR; ocr = PaddleOCR(use_angle_cls=True, lang='ch'); print('OK')"
```
