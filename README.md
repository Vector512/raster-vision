# GIS 栅格数据处理软件--rastervision

## 简介

本项目为一款基于 Python 开发的图形界面应用软件，支持加载、显示和处理 GIS 栅格数据（GeoTIFF 文件）。该软件采用 PyQt 实现前端界面，用户界面通过 Qt Designer 可视化设计，并采用动态加载技术（uic.loadUi）将.ui 文件集成至程序中，从而提高开发效率与界面灵活性。后端结合 GDAL、NumPy、Matplotlib 等核心库，实现栅格数据的读取、图像绘制与基本分析功能。该软件旨在降低传统 GIS SDK 使用门槛，便于教学、演示与后续二次开发。

## 软件主要功能

- 支持 GeoTIFF 文件的导入与多波段展示
- 以树状结构展示文件与波段信息
- 支持图像的灰度线性拉伸显示
- 提供波段统计分析（最小值、最大值、均值、标准差）
- 图像显示支持缩放与拖动

## 安装说明

### 1. 创建并激活虚拟环境（推荐使用 Conda）

```bash
conda create -n gis_raster_env python=3.9 -y
conda activate gis_raster_env 
```

### 2. 安装依赖库

```bash
conda install pyqt=5 -c conda-forge -y
conda install matplotlib -c conda-forge -y
conda install numpy -c conda-forge -y
conda install gdal -c conda-forge -y
pip install mplcursors
```

## 项目结构

![image](https://github.com/user-attachments/assets/ad294b07-0241-4f73-8574-0b64a8caa8bf)

