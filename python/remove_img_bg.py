import os
import sys
from PIL import Image

def remove_white_background(input_path, output_path=None, threshold=250):
    """
    移除图片的白色背景并将其变为透明。
    
    :param input_path: 输入图片的路径
    :param output_path: 输出图片的路径（默认为原文件名+_transparent.png）
    :param threshold: 判定为白色的阈值（0-255），越高越严格。
                      这里指RGB三个通道的值都大于此阈值才会被认为是白色。
    """
    try:
        # 打开图片
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        # 获取图片数据
        datas = img.getdata()
        
        new_data = []
        for item in datas:
            # item 是一个元组 (R, G, B, A)
            # 检查 RGB 值是否都大于阈值（接近白色）
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                # 变为全透明
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        # 更新图片数据
        img.putdata(new_data)
        
        # 确定输出路径
        if output_path is None:
            filename, _ = os.path.splitext(input_path)
            output_path = f"{filename}_transparent.png"
            
        # 保存图片
        img.save(output_path, "PNG")
        print(f"处理完成！图片已保存至: {output_path}")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # 如果没有命令行参数，尝试寻找当前目录下的默认图片或提示输入
        print("请输入要处理的图片文件名（支持 jpg, png 等）：")
        input_file = input("文件名: ").strip()
        
    # 去除两端的引号（如果是从文件浏览器复制路径可能会带引号）
    input_file = input_file.strip('"').strip("'")
    
    if os.path.exists(input_file):
        remove_white_background(input_file, threshold=230)
    else:
        print(f"找不到文件: {input_file}")
