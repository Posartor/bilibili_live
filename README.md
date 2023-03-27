# Bilibili Live 直播状态监控 Home Assistant 集成
bilibili_live 是一个使用 GPT-4 开发的 Home Assistant 自定义集成，用于显示指定 Bilibili 直播间的状态和信息。集成可以显示直播间的标题、主播名、头像、直播间地址、封面以及直播状态。通过将集成与 Home Assistant 配合使用，您可以监控您最喜欢的 Bilibili 直播间，以便及时了解直播状态并获得最新信息。

## 功能
* 显示直播间的标题、主播名、头像、直播间地址、封面以及直播状态。
* 在实体启动时立即获取新信息，以防出现传感器状态变为未知。
* 检测并避免配置重复的 UID，确保每个实体都有唯一的主播信息。
* 在 Home Assistant 中与其他传感器、开关、通知等组件配合使用。

## 安装

1. 访问项目的 [Latest Release](https://github.com/Posartor/bilibili_live/releases/latest) 页面，下载最新的 Release 版本。
2. 解压下载的压缩包，将其中的 `custom_components/bilibili_live` 文件夹复制到您的 Home Assistant 的 `custom_components` 目录下，确保文件夹名称为 `bilibili_live`。
   ```
   path/to/your/home-assistant/config/custom_components/bilibili_live
   ```
   如果您的 Home Assistant 配置目录中没有 `custom_components` 文件夹，请先创建一个。
3. 重新启动您的 Home Assistant 以加载新的集成。

## 配置
在 Home Assistant 的“配置”>“设备与服务”>“添加集成”中，找到“Bilibili Live”并点击添加。
在弹出的配置界面中，输入主播的 UID 和自定义名称，然后点击“提交”。

## 实体
实体将根据您的配置创建。如果您为集成设置了自定义名称，实体名称将为 `sensor.<自定义名称>`；如果保留默认值 "Bilibili Live"，则实体名称将为 `sensor.<主播名称>`。

## 属性
* `status`: 直播状态（直播中/休息中）
* `title`: 直播间名称
* `name`: 主播名称
* `face`: 主播头像
* `url`: 直播间链接
* `cover`: 直播间封面

## 示例
在 Home Assistant 的概览仪表盘中添加一个实体卡片，选择您刚刚添加的 Bilibili Live 实体，即可查看直播状态和相关信息。