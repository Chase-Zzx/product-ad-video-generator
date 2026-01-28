#!/usr/bin/env python3
"""
视频拼接与音频合成脚本
将多个视频片段拼接为一个完整视频，并添加TTS配音和BGM
"""

import argparse
import os
import sys
import json
import tempfile
from pathlib import Path


def merge_videos_with_audio(
    video_segments: list,
    tts_audio_path: str,
    bgm_path: str = None,
    output_path: str = "final_video.mp4",
    bgm_volume: float = 0.3
) -> bool:
    """
    拼接视频片段并添加音频
    
    Args:
        video_segments: 视频片段路径列表（按顺序）
        tts_audio_path: TTS音频文件路径（单个整段音频文件）
        bgm_path: BGM文件路径（可选）
        output_path: 最终视频输出路径
        bgm_volume: BGM音量（0.1-1.0）
    
    Returns:
        bool: 合成是否成功
    """
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
        from moviepy.audio.fx import volumex
        
        print("正在加载视频片段...")
        
        # 验证输入
        if len(video_segments) == 0:
            print("错误：未提供视频片段")
            return False
        
        # 加载视频片段
        video_clips = []
        for i, video_path in enumerate(video_segments):
            if not os.path.exists(video_path):
                print(f"错误：视频片段不存在: {video_path}")
                return False
            
            print(f"  [{i+1}/{len(video_segments)}] 加载视频: {video_path}")
            clip = VideoFileClip(video_path)
            video_clips.append(clip)
        
        print(f"共加载 {len(video_clips)} 个视频片段")
        
        # 拼接视频片段
        print("正在拼接视频片段...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        print(f"拼接完成，总时长: {final_video.duration:.2f}秒")
        
        # 加载TTS音频（单个整段文件）
        print(f"正在加载TTS音频: {tts_audio_path}")
        if not os.path.exists(tts_audio_path):
            print(f"错误：TTS音频不存在: {tts_audio_path}")
            return False
        
        tts_audio = AudioFileClip(tts_audio_path)
        
        # 调整TTS音频长度以匹配视频总时长
        video_duration = final_video.duration
        tts_duration = tts_audio.duration
        
        if tts_duration < video_duration:
            # TTS较短，循环播放
            print(f"  TTS音频({tts_duration:.2f}s)短于视频({video_duration:.2f}s)，循环播放")
            tts_audio = tts_audio.loop(duration=video_duration)
        elif tts_duration > video_duration:
            # TTS较长，截断
            print(f"  TTS音频({tts_duration:.2f}s)长于视频({video_duration:.2f}s)，截断")
            tts_audio = tts_audio.subclip(0, video_duration)
        
        # 设置视频的音频轨道为TTS
        final_video = final_video.set_audio(tts_audio)
        
        # 添加BGM（如果提供）
        if bgm_path and os.path.exists(bgm_path):
            print(f"正在加载BGM: {bgm_path}")
            bgm = AudioFileClip(bgm_path)
            
            # 调整BGM长度以匹配视频
            video_duration = final_video.duration
            bgm_duration = bgm.duration
            
            if bgm_duration < video_duration:
                print(f"  BGM({bgm_duration:.2f}s)短于视频，循环播放")
                bgm = bgm.loop(duration=video_duration)
            elif bgm_duration > video_duration:
                print(f"  BGM({bgm_duration:.2f}s)长于视频，截断")
                bgm = bgm.subclip(0, video_duration)
            
            # 调整BGM音量
            print(f"  调整BGM音量: {bgm_volume}")
            bgm = bgm.fx(volumex, bgm_volume)
            
            # 混合音频
            print("正在混合音频...")
            final_audio = CompositeAudioClip([
                final_video.audio,
                bgm
            ])
            
            # 设置最终音频
            final_video = final_video.set_audio(final_audio)
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 导出最终视频
        print(f"正在导出最终视频: {output_path}")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        print(f"视频合成完成！")
        print(f"输出文件: {output_path}")
        print(f"总时长: {final_video.duration:.2f}秒")
        
        # 清理
        for clip in video_clips:
            clip.close()
        if 'tts_audio' in locals():
            tts_audio.close()
        if 'bgm' in locals():
            bgm.close()
        final_video.close()
        
        return True
        
    except ImportError:
        print("错误：未安装moviepy库")
        print("请运行: pip install moviepy==1.0.3")
        return False
    except Exception as e:
        print(f"视频合成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="拼接视频片段并添加TTS配音和BGM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础拼接（只有TTS）
  python merge_video.py \\
    --video-segments '["seg1.mp4", "seg2.mp4", "seg3.mp4"]' \\
    --tts-audio ./temp_output/audio/narration.wav \\
    --output ./temp_output/final/ad_video.mp4

  # 添加BGM
  python merge_video.py \\
    --video-segments '["seg1.mp4", "seg2.mp4", "seg3.mp4"]' \\
    --tts-audio ./temp_output/audio/narration.wav \\
    --bgm ./assets/bgm/upbeat.mp3 \\
    --bgm-volume 0.3 \\
    --output ./temp_output/final/ad_video.mp4

  # 使用JSON配置文件
  python merge_video.py \\
    --config ./config.json \\
    --output ./temp_output/final/ad_video.mp4
        """
    )
    
    parser.add_argument(
        '--video-segments',
        type=str,
        help='视频片段路径列表（JSON数组格式）'
    )
    
    parser.add_argument(
        '--tts-audio',
        type=str,
        help='TTS音频文件路径（单个整段音频文件）'
    )
    
    parser.add_argument(
        '--bgm',
        type=str,
        default=None,
        help='BGM文件路径（可选）'
    )
    
    parser.add_argument(
        '--output',
        default='final_video.mp4',
        help='最终视频输出路径（默认：final_video.mp4）'
    )
    
    parser.add_argument(
        '--bgm-volume',
        type=float,
        default=0.3,
        help='BGM音量（0.1-1.0，默认：0.3）'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='配置文件路径（JSON格式，包含所有参数）'
    )
    
    args = parser.parse_args()
    
    # 如果使用配置文件
    if args.config:
        if not os.path.exists(args.config):
            print(f"错误：配置文件不存在: {args.config}")
            sys.exit(1)
        
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        video_segments = config.get('video_segments', [])
        tts_audio_path = config.get('tts_audio')
        bgm_path = config.get('bgm')
        output_path = config.get('output', 'final_video.mp4')
        bgm_volume = config.get('bgm_volume', 0.3)
    else:
        # 从命令行参数读取
        if not args.video_segments or not args.tts_audio:
            print("错误：必须提供 --video-segments 和 --tts-audio，或使用 --config 配置文件")
            sys.exit(1)
        
        try:
            video_segments = json.loads(args.video_segments)
        except json.JSONDecodeError as e:
            print(f"错误：JSON解析失败: {e}")
            sys.exit(1)
        
        tts_audio_path = args.tts_audio
        bgm_path = args.bgm
        output_path = args.output
        bgm_volume = args.bgm_volume
    
    # 执行视频合成
    success = merge_videos_with_audio(
        video_segments=video_segments,
        tts_audio_path=tts_audio_path,
        bgm_path=bgm_path,
        output_path=output_path,
        bgm_volume=bgm_volume
    )
    
    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
