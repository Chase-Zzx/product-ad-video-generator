#!/usr/bin/env python3
"""
商品主体扣图脚本
使用rembg库去除图片背景
"""

import argparse
import os
from pathlib import Path
from PIL import Image
import sys


def remove_background(input_path: str, output_path: str) -> bool:
    """
    去除商品图片背景
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径（PNG格式，透明背景）
    
    Returns:
        bool: 处理是否成功
    """
    try:
        from rembg import remove
        
        # 检查输入文件
        if not os.path.exists(input_path):
            print(f"错误：输入文件不存在: {input_path}")
            return False
        
        # 读取图片
        print(f"正在读取图片: {input_path}")
        input_image = Image.open(input_path)
        
        # 去除背景
        print("正在去除背景...")
        output_image = remove(input_image)
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 保存结果
        print(f"正在保存到: {output_path}")
        output_image.save(output_path)
        
        # 输出信息
        width, height = output_image.size
        print(f"扣图完成！输出图片尺寸: {width}x{height}")
        print(f"输出文件: {output_path}")
        
        return True
        
    except ImportError:
        print("错误：未安装rembg库")
        print("请运行: pip install rembg==2.0.50")
        return False
    except Exception as e:
        print(f"扣图失败: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="去除商品图片背景",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python remove_background.py --input product.jpg --output product_no_bg.png
  python remove_background.py --input ./images/shirt.jpg --output ./output/shirt_no_bg.png
        """
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='输入商品图片路径（支持JPG、PNG等格式）'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='输出图片路径（自动使用PNG格式保存透明背景）'
    )
    
    args = parser.parse_args()
    
    # 执行扣图
    success = remove_background(args.input, args.output)
    
    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
