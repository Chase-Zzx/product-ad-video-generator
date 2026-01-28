# 商品广告视频生成器

根据商品图片自动生成专业广告视频的 Coze Skill。包含商品扣图、信息识别、脚本创作、分镜设计、视频生成和后期合成全流程。

## 功能特点

- **商品主体扣图** - 自动去除背景，提取商品主体
- **智能信息识别** - AI 分析商品类型、特征、卖点
- **广告脚本创作** - 自动生成专业广告文案
- **分镜设计** - 智能规划视频画面结构
- **视频生成** - 调用 AI 生成视频片段
- **后期合成** - TTS 配音 + BGM 配乐 + 视频拼接

## 适用场景

- 商品推广
- 电商营销
- 品牌宣传

## 依赖安装

```bash
pip install rembg==2.0.50 moviepy==1.0.3 Pillow==10.0.0
```

## 项目结构

```
├── SKILL.md                 # Skill 主文件（完整流程说明）
├── scripts/
│   ├── remove_background.py # 商品扣图脚本
│   ├── generate_video.py    # 视频生成脚本
│   └── merge_video.py       # 视频拼接与音频合成
├── references/
│   ├── script-template.md   # 脚本模板（280-320字/分钟）
│   ├── storyboard-format.md # 分镜格式规范
│   └── video-prompt-guide.md# 视频 Prompt 指南
└── assets/                  # 资源文件夹
```

## 使用方法

1. 将此 Skill 导入 Coze
2. 上传商品图片
3. 告诉 AI 你想生成广告视频
4. AI 将自动完成全流程并输出最终视频

## License

MIT
