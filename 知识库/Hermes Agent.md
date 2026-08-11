江湖人称爱马仕

[08_Hermes Agent Skills_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV13YRjBTEPb?spm_id_from=333.788.player.switch&vd_source=0654d6128bca42b9dcdd87e813b1f867&p=8)

开源的自主AI Agent框架，2026.2月低发布，功能类似OpenClaw

> 与OpenClaw对比：
>
> - token消耗少
> - 长期记忆高于OpenClaw

Hermes的一些特点：

- 自动从交互中生成skill
  - 比如说第一次让Hermes去联网搜索一些热门ai时间，在完成任务后，他可以将该时间总结成skill，下次进行相同或者类似的事件时会非常快
- 在使用中持续迭代技能
- 主动持久化知识和用户偏好
  - 有memory与user两个文件，有大小限制，不大
    - memory：Agent的个人笔记
    - user：用户画像

  - 历史对话机会被保存到一个数据库文件中，但只保存最近几周的

- 跨会话构建对用户的深度理解
- 可以接入MCP扩张ai工具
  - 本事内置，可以调用外部的工具
    - 外部的工具是只别人写好的工具放在服务器上，你去调用api接口，有些需要配置连接，有些要钱，MCP协议（本地编写的）只是负责教Agent怎么使用这些工具（传什么参数，返回什么格式）

  - 理论上来说可以扩展为无限的工具


**目录下有 SOUL.md**

> 系统的第一提示词，用于定制化Herme

**可以统一为全平台或指定平台定制工具**

> Hermes内置多个工具，通过命令将这些工具配置到指定平台

**可以在云服务器中部署Hermes**

> 让Hermes一直处于交互状态：可以一直用绑定的qq、微信等软件进行互动

**skill**

> - 官方有许多skill，有些是下载的时候就绑定的，有些是后面根据任务自己生成的，有些需要自己下载
>
> - 可以自己创建skill
>
> - skill模版：
>
>   > ```
>   > ---
>   > name: taiyuan-weather
>   > description: 获取太原市实时天气预报和未来天气趋势
>   > version: 1.0.0
>   > metadata:
>   > hermes:
>   >  tags: [weather, forecast, utility]
>   >  category: creative
>   >  fallback_for_toolsets: [web]
>   >  requires_toolsets: [terminal]
>   >  config:
>   >       - key: weather.city
>   >         description: "目标城市名称，用于天气查询"
>   >         default: "Taiyuan"
>   >         prompt: "请输入城市名称（默认太原，英文或
>   > 拼音）"
>   >       - key: weather.units
>   >         description: "温度单位，celsius 或 
>   > fahrenheit"
>   >         default: "celsius"
>   >         prompt: "选择温度单位 
>   > (celsius/fahrenheit)"
>   > ---
>   > # 太原天气预报 Skill
>   > ## 何时使用
>   > - 用户询问“今天天气怎么样”、“未来几天会下雨吗”、“周
>   > 末气温多少度”等与天气相关的问题。
>   > - 需要为出行、活动安排等决策提供太原地区的气象信息。
>   > - 需要获取实时气温、湿度、风速、降水概率或未来3-7天
>   > 趋势。
>   > ## 操作步骤
>   > 1. **读取配置**  
>   > 从 `config` 中获取目标城市（默认为 Taiyuan）和
>   > 温度单位（celsius 或 fahrenheit）。
>   > 2. **调用天气 API**  
>   > 使用 `curl` 或 `wget` 请求免费公开天气服务 
>   > `wttr.in`（示例）：  
>   >    ```bash
>   >    curl -s "https://wttr.in/${city}?
>   > format=%C+%t+%w+%h&u"   # 如需华氏度添加 &u
>   > ```
>   >
>   > 最后一行的地址是全球开源的天气预报
>   >
> - 可以直接指定skill，当agent自己识别到了也会直接采用



Hermes在周宏凯的简历里与claude code、opencode放在一起，标注为agent编码工具



⚠️5月后的版本Herme不仅仅只能在linux或mac或windows上wsl中下载了，可以直接在windows桌面下载