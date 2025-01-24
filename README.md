# Zendure Integration for Home Assistant

## 安装方法

### 方法一：通过HACS安装（推荐）

1. 确保已经安装了[HACS](https://hacs.xyz/)
2. 在HACS中添加自定义存储库：
   - 点击HACS侧边栏中的"集成"
   - 点击右上角的三个点
   - 选择"自定义存储库"
   - 输入仓库URL
   - 类别选择"集成"
3. 点击"下载"
4. 重启Home Assistant
5. 在集成页面中搜索"Zendure"并添加集成

### 方法二：手动安装

1. 将`custom_components/zendure`文件夹复制到你的Home Assistant配置目录下的`custom_components`文件夹中
2. 重启Home Assistant
3. 在集成页面中搜索"Zendure"并添加集成
4. 按照配置向导完成设置

## 开发说明

这个集成使用了以下Home Assistant的核心功能：

- Config Entries
- Entity Platform
- Sensor Platform
- MQTT

## 支持的设备

- Zendure便携式储能设备

## 功能

- 电池电量显示
- 充电状态监控
- 输入功率监测
- 输出功率监测

## 许可证

MIT License