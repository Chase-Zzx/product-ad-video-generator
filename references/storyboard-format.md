# 分镜设计格式规范

## 目录
- [分镜格式](#分镜格式)
- [完整示例](#完整示例)
- [设计要点](#设计要点)
- [Prompt生成指南](#prompt生成指南)

## 分镜格式

### 标准格式（JSON）

```json
{
  "storyboard": [
    {
      "id": "seg_01",
      "sequence": 1,
      "duration": 4.0,
      "scene_type": "opening",
      "visual_description": "科技感城市夜景，蓝色和紫色灯光在建筑间流转，镜头缓慢推近",
      "product_position": {
        "location": "none",
        "size": "none",
        "action": "none"
      },
      "digital_human": {
        "position": "voiceover",
        "appearance": "professional female, business attire",
        "action": "voice narration only"
      },
      "camera_movement": "slow push in",
      "lighting": "neon lights, cool tones, cinematic",
      "text_overlay": null,
      "transition": "fade in"
    },
    {
      "id": "seg_02",
      "sequence": 2,
      "duration": 5.0,
      "scene_type": "showcase",
      "visual_description": "智能手表正面特写，表盘亮起显示时间和健康数据，金属边框反射微光",
      "product_position": {
        "location": "center",
        "size": "close-up",
        "action": "rotating slowly to show 360 degree view"
      },
      "digital_human": {
        "position": "left",
        "appearance": "professional female",
        "action": "gesturing towards the watch"
      },
      "camera_movement": "slight rotation",
      "lighting": "studio lighting, soft shadows, product highlight",
      "text_overlay": "全新X系列",
      "transition": "cut"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 分镜唯一标识符 |
| `sequence` | integer | 是 | 序号（1, 2, 3...） |
| `duration` | float | 是 | 时长（秒） |
| `scene_type` | string | 是 | 场景类型：opening/showcase/selling/ending |
| `visual_description` | string | 是 | 画面详细描述 |
| `product_position` | object | 是 | 商品位置和展示方式 |
| `digital_human` | object | 是 | 数字人配置 |
| `camera_movement` | string | 是 | 摄像机运动 |
| `lighting` | string | 是 | 灯光描述 |
| `text_overlay` | string/null | 否 | 文字叠加内容 |
| `transition` | string | 是 | 转场方式 |

## 完整示例

### 示例1：智能手表（30秒，4个分镜）

```json
{
  "storyboard": [
    {
      "id": "seg_01",
      "sequence": 1,
      "duration": 4.0,
      "scene_type": "opening",
      "visual_description": "科技感城市夜景，高层建筑窗户透出的蓝色和紫色灯光在夜空中流转，镜头缓慢推近，营造未来感氛围",
      "product_position": {
        "location": "none",
        "size": "none",
        "action": "none"
      },
      "digital_human": {
        "position": "voiceover",
        "appearance": "professional female, 30s, elegant attire",
        "action": "voice narration only"
      },
      "camera_movement": "slow push in from distance",
      "lighting": "neon lights, cool blue and purple tones, cinematic",
      "text_overlay": null,
      "transition": "fade in"
    },
    {
      "id": "seg_02",
      "sequence": 2,
      "duration": 6.0,
      "scene_type": "showcase",
      "visual_description": "智能手表正面特写，表盘亮起显示数字时间界面，金属边框反射柔和光线，表面玻璃质感清晰可见",
      "product_position": {
        "location": "center",
        "size": "close-up",
        "action": "rotating slowly 360 degrees to show all angles"
      },
      "digital_human": {
        "position": "left",
        "appearance": "professional female",
        "action": "gesturing towards the watch with left hand"
      },
      "camera_movement": "slight orbit around the watch",
      "lighting": "studio lighting, soft shadows, product highlight from top-left",
      "text_overlay": "全新X系列",
      "transition": "cut"
    },
    {
      "id": "seg_03",
      "sequence": 3,
      "duration": 8.0,
      "scene_type": "selling",
      "visual_description": "手表显示健康监测界面，心率波形、血氧数值、睡眠数据图表依次浮现，背景是模糊的健身房场景",
      "product_position": {
        "location": "center-right",
        "size": "medium",
        "action": "screen displaying changing data"
      },
      "digital_human": {
        "position": "left",
        "appearance": "professional female",
        "action": "pointing to screen data while speaking"
      },
      "camera_movement": "static with slight zoom on screen",
      "lighting": "bright and clean, daylight balanced",
      "text_overlay": null,
      "transition": "cut"
    },
    {
      "id": "seg_04",
      "sequence": 4,
      "duration": 4.0,
      "scene_type": "ending",
      "visual_description": "手表特写与品牌Logo叠加，渐变为纯色背景",
      "product_position": {
        "location": "center",
        "size": "close-up",
        "action": "static with subtle glow effect"
      },
      "digital_human": {
        "position": "voiceover",
        "appearance": "professional female",
        "action": "voice narration only"
      },
      "camera_movement": "static",
      "lighting": "clean white background, even lighting",
      "text_overlay": "立即抢购 | www.example.com",
      "transition": "fade out"
    }
  ]
}
```

## 设计要点

### 1. 场景类型（scene_type）

| 类型 | 用途 | 时长建议 | 画面特点 |
|------|------|---------|---------|
| `opening` | 吸引注意，建立氛围 | 3-5秒 | 氛围感强，商品可以不出场 |
| `showcase` | 多角度展示商品 | 5-15秒 | 商品为主，细节清晰 |
| `selling` | 突出卖点和功能 | 5-10秒 | 场景化展示，结合使用 |
| `ending` | 品牌强化和行动引导 | 3-5秒 | 简洁明了，CTA明确 |

### 2. 商品位置（product_position）

| 位置 | 适用场景 | 说明 |
|------|---------|------|
| `none` | 开场、纯氛围场景 | 商品不出场 |
| `center` | 展示、卖点 | 商品居中，最显眼 |
| `left` | 数字人配合 | 数字人在右侧，商品在左侧 |
| `right` | 数字人配合 | 数字人在左侧，商品在右侧 |
| `background` | 数字人为主 | 商品作为背景元素 |

### 3. 商品尺寸（product_position.size）

| 尺寸 | 适用场景 | 说明 |
|------|---------|------|
| `close-up` | 细节展示 | 商品占据画面70-90% |
| `medium` | 整体展示 | 商品占据画面40-60% |
| `full` | 场景展示 | 商品与场景协调 |

### 4. 数字人位置（digital_human.position）

| 位置 | 说明 | 适用场景 |
|------|------|---------|
| `voiceover` | 画外音，不出镜 | 开场、结尾 |
| `left` | 在画面左侧 | 商品在右侧时 |
| `right` | 在画面右侧 | 商品在左侧时 |
| `center` | 居中，与商品共存 | 商品作为背景时 |

### 5. 摄像机运动（camera_movement）

| 运动 | 效果 | 适用场景 |
|------|------|---------|
| `static` | 静止 | 强调稳定性、细节 |
| `push in` | 推近 | 引导注意力、聚焦 |
| `pull back` | 拉远 | 展示环境、全景 |
| `pan left/right` | 平移 | 跟随物体、扫描 |
| `tilt up/down` | 俯仰 | 展示高度、层次 |
| `orbit` | 环绕 | 展示360度、立体感 |
| `zoom in/out` | 变焦 | 突出重点、环境 |

### 6. 灯光描述（lighting）

| 灯光类型 | 效果 | 适用产品 |
|---------|------|---------|
| `studio lighting` | 专业、干净 | 数码、化妆品 |
| `natural daylight` | 自然、真实 | 服装、家居 |
| `neon lights` | 科技、潮流 | 数码、潮流商品 |
| `warm lighting` | 温馨、舒适 | 家居、母婴 |
| `dramatic lighting` | 戏剧、高端 | 奢侈品、艺术品 |

## Prompt生成指南

### 基于分镜生成视频Prompt

每个分镜需要生成详细的视频生成Prompt，包含以下要素：

#### 1. 核心要素（必需）
- **商品描述**：基于扣图详细描述商品（颜色、材质、形状、细节）
- **场景环境**：背景、环境元素、氛围
- **数字人**：形象、服装、动作、表情
- **摄像机**：角度、运动、景深

#### 2. 风格关键词（推荐）
- **风格**：cinematic, professional, modern, minimalist, elegant
- **质感**：premium, sleek, matte, glossy, textured
- **色彩**：warm, cool, vibrant, muted, pastel
- **光影**：soft lighting, dramatic lighting, natural light, studio light

#### 3. 技术参数（可选）
- **分辨率**：4K, 1080p
- **帧率**：24fps, 30fps
- **宽高比**：16:9, 9:16
- **时长**：具体秒数

### Prompt示例

**分镜信息**：
- 场景：智能手表正面特写
- 商品位置：居中
- 摄像机：缓慢旋转
- 灯光：studio lighting

**生成Prompt**：
```
A professional product shot of a premium smartwatch, centered in the frame, 
metallic silver case with sapphire crystal glass, digital watch face displaying time, 
clean white studio background with soft shadows, 
slow 360-degree rotation to show all angles, 
studio lighting with soft highlights, 
cinematic quality, 4K resolution, 30fps, 16:9 aspect ratio, 
premium sleek design, sharp focus, realistic textures
```

**分镜信息**：
- 场景：数字人左侧手势引导
- 商品：智能手表右中位置
- 数字人：professional female, business attire

**生成Prompt**：
```
A professional female digital human in elegant business attire standing on the left side of the frame, 
gesturing towards a premium smartwatch positioned on the right, 
the watch is in medium shot showing the digital display, 
clean minimalist office background with soft natural light, 
professional tone, cinematic lighting, 
sharp focus on both the person and product, 
realistic facial expression and hand gesture, 
4K quality, 30fps, commercial video style
```

## 注意事项
- 分镜描述要具体但不过于冗长
- 考虑视频生成AI的理解能力，使用明确的视觉描述
- 每个分镜的Prompt应保持风格一致性
- 避免过于复杂的场景，保持生成可控性
- 测试Prompt效果后可迭代优化
