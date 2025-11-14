# 📷 camchain_to_intri 中文说明文档

## 🔍 项目简介
本工具用于将`Kalibr`标准输出转为 OpenCV 风格的相机内参文件，即包含 `cam0`, `cam1` 等相机内参的 `camchain.yaml` 文件（或多个 YAML 文件）转换为 OpenCV 风格的相机内参文件（`.yml` 格式），便于在 SLAM、三维重建等项目中使用。


支持功能包括：

✅ 读取单个 `camchain.yaml` 文件，或一个文件夹下所有包含 `camX` 的 YAML 文件；  
✅ 支持通过配置文件将 `cam0`/`cam1`/... 映射为真实相机编号；  
✅ 自动格式化为 OpenCV 标准格式，包括 K 矩阵 和 畸变参数。

---

## 📂 输入输出说明

| 类型       | 说明                          |
|------------|-------------------------------|
| 单文件     | 一个包含 `cam0`, `cam1` 等键的 `camchain.yaml` |
| 多文件目录 | 一个文件夹，里面包含不同相机的 `.yaml` / `.yml` 文件 |

文件中需包含字段示例：

```yaml
cam0:
  name: some_name
  intrinsics: [fx, fy, cx, cy]
  distortion_coeffs: [k1, k2, ...]
```
## ⚙️ 可选配置文件说明（--config）  
你可以提供一个 config.yaml 文件，用于将默认的 cam0, cam1 替换成真实的相机编号或名称：

示例 config.yaml：

```yaml
cam0: 220403117
cam1: 220403119
cam2: 220403129
cam3: 220403131
```
## 📥 使用方法  
命令行执行方式：

```bash
python convert.py 输入路径 输出路径 [--config 映射配置路径]
```

参数说明：

| 参数     | 是否必需 | 说明                                                         |
|----------|----------|--------------------------------------------------------------|
| input    | ✅       | camchain.yaml 文件路径或包含多个 YAML 文件的文件夹路径       |
| output   | ✅       | 输出的 OpenCV 格式 intrinsics `.yml` 文件路径                |
| --config | 可选     | 一个映射 cam0/cam1/... 到真实相机编号的配置文件              |

## 📦 示例用法

### 示例 1：转换单个文件
```bash
python convert.py ./camchain.yaml ./intri.yml
```

### 示例 2：转换整个文件夹
```bash
python convert.py ./calib_folder ./intri.yml
```

### 示例 3：添加相机编号映射
```bash
python convert.py ./camchain.yaml ./intri.yml --config ./config.yaml
```

## 📝 输出文件格式（OpenCV）

输出文件为 OpenCV 可读格式，包含：

- 相机名称列表 `names`
- 各相机的内参矩阵 `K_相机名`
- 各相机的畸变系数 `dist_相机名`

### 示例输出（部分）：
```yaml
%YAML:1.0
---
names:
  - "220403117"

K_220403117: !!opencv-matrix
  rows: 3
  cols: 3
  dt: d
  data: [fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0]

dist_220403117: !!opencv-matrix
  rows: 1
  cols: 5
  dt: d
  data: [k1, k2, p1, p2, k3]
```

## ✅ 注意事项

- `intrinsics` 必须是长度为 4 的列表：`[fx, fy, cx, cy]`
- `distortion_coeffs` 可为任意长度，将自动追加一个 0（补齐或兼容性处理）
- 如果未提供映射配置，将优先使用相机的 `"name"` 字段，否则使用 `camX` 作为名称

---


## 📧 联系方式

如有问题或建议，欢迎反馈。  
邮箱：suweenliang@163.com  
使用愉快！🎉



