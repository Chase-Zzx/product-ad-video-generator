#!/usr/bin/env python3
"""
视频生成脚本
调用外部视频生成API（如Runway、Pika等）生成商品视频片段
"""

import argparse
import os
import sys
import json
import time
from pathlib import Path


def generate_video_segment(
    prompt: str,
    product_image: str,
    duration: float,
    output_path: str,
    api_key: str,
    api_url: str,
    model: str = None
) -> bool:
    """
    调用视频生成API生成单个视频片段
    
    Args:
        prompt: 视频生成Prompt（包含商品、场景、风格描述）
        product_image: 商品扣图路径
        duration: 视频时长（秒）
        output_path: 视频输出路径
        api_key: API密钥
        api_url: API端点
        model: 模型名称（可选）
    
    Returns:
        bool: 生成是否成功
    """
    try:
        from coze_workload_identity import requests
        
        print(f"正在生成分镜视频...")
        print(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")
        print(f"商品图片: {product_image}")
        print(f"目标时长: {duration}秒")
        
        # 检查输入文件
        if not os.path.exists(product_image):
            print(f"错误：商品图片不存在: {product_image}")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 构建API请求
        # 注意：以下是一个通用框架，实际API调用需要根据具体服务进行调整
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 准备请求数据
        payload = {
            "prompt": prompt,
            "image": product_image,
            "duration": duration,
            "model": model or "default"
        }
        
        print(f"正在调用API: {api_url}")
        
        # 发起请求（异步生成模式）
        # 实际实现需要根据API文档调整
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        # 处理生成结果
        # 不同API有不同的返回格式，这里提供一个通用框架
        if "task_id" in result:
            # 异步任务，需要轮询状态
            task_id = result["task_id"]
            print(f"任务已提交，ID: {task_id}")
            
            # 轮询任务状态
            max_wait = 300  # 最多等待5分钟
            check_interval = 5  # 每5秒检查一次
            elapsed = 0
            
            while elapsed < max_wait:
                status_response = requests.get(
                    f"{api_url}/tasks/{task_id}",
                    headers=headers,
                    timeout=30
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status", "unknown")
                print(f"任务状态: {status}")
                
                if status == "completed":
                    # 下载视频
                    video_url = status_data.get("result", {}).get("video_url")
                    if video_url:
                        print(f"下载视频: {video_url}")
                        video_response = requests.get(video_url, timeout=60)
                        video_response.raise_for_status()
                        
                        with open(output_path, "wb") as f:
                            f.write(video_response.content)
                        
                        print(f"视频已保存: {output_path}")
                        return True
                    else:
                        print("错误：未找到视频下载链接")
                        return False
                        
                elif status == "failed":
                    error_msg = status_data.get("error", "未知错误")
                    print(f"任务失败: {error_msg}")
                    return False
                
                # 继续等待
                time.sleep(check_interval)
                elapsed += check_interval
            
            print(f"错误：任务超时（{max_wait}秒）")
            return False
            
        elif "video_url" in result:
            # 同步返回，直接下载
            video_url = result["video_url"]
            print(f"下载视频: {video_url}")
            
            video_response = requests.get(video_url, timeout=60)
            video_response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            
            print(f"视频已保存: {output_path}")
            return True
            
        else:
            print("错误：未知的API响应格式")
            print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return False
        
    except ImportError:
        print("错误：未安装requests库")
        print("请运行: pip install requests")
        return False
    except Exception as e:
        print(f"视频生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="调用视频生成API生成分镜视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用Runway API生成
  python generate_video.py \\
    --prompt "A professional product shot showing the smartwatch in a modern office setting, cinematic lighting" \\
    --product-image ./product_no_bg.png \\
    --duration 5 \\
    --output ./temp_output/videos/segment_01.mp4 \\
    --api-key YOUR_API_KEY \\
    --api-url https://api.runwayml.com/v1/generate

  # 使用Pika API生成
  python generate_video.py \\
    --prompt "Close-up of the dress, soft natural lighting, elegant movement" \\
    --product-image ./dress_no_bg.png \\
    --duration 4 \\
    --output ./temp_output/videos/segment_02.mp4 \\
    --api-key YOUR_API_KEY \\
    --api-url https://api.pika.art/v1/generate \\
    --model pika-1.0
        """
    )
    
    parser.add_argument(
        '--prompt',
        required=True,
        help='视频生成Prompt（详细描述商品、场景、风格、镜头等）'
    )
    
    parser.add_argument(
        '--product-image',
        required=True,
        help='商品扣图路径（透明背景PNG）'
    )
    
    parser.add_argument(
        '--duration',
        type=float,
        required=True,
        help='视频时长（秒）'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='视频输出路径（MP4格式）'
    )
    
    parser.add_argument(
        '--api-key',
        required=True,
        help='视频生成API密钥'
    )
    
    parser.add_argument(
        '--api-url',
        required=True,
        help='视频生成API端点'
    )
    
    parser.add_argument(
        '--model',
        default=None,
        help='模型名称（可选，根据API文档设置）'
    )
    
    args = parser.parse_args()
    
    # 执行视频生成
    success = generate_video_segment(
        prompt=args.prompt,
        product_image=args.product_image,
        duration=args.duration,
        output_path=args.output,
        api_key=args.api_key,
        api_url=args.api_url,
        model=args.model
    )
    
    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
