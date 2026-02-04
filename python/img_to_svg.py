import cv2
import numpy as np
import sys
import os

def image_to_svg(input_path, output_path=None, k_colors=8, min_area=10, transparent_background=False):
    """
    将图片转换为 SVG (矢量化)，并尝试保留颜色。
    
    :param input_path: 输入图片路径
    :param output_path: 输出 SVG 路径
    :param k_colors: 颜色聚类数量，决定了最终 SVG 中的颜色丰富度
    :param min_area: 忽略小于此面积的微小噪点区域
    :param transparent_background: 是否移除背景色（假设角落颜色为背景）
    """
    try:
        # 读取图片
        img = cv2.imread(input_path)
        if img is None:
            print(f"无法读取图片: {input_path}")
            return

        height, width = img.shape[:2]
        
        # 预处理：轻微模糊以减少噪点
        img_blur = cv2.medianBlur(img, 3)

        # -----------------------------------------------------------
        # 1. 颜色量化 (Color Quantization) 使用 K-Means
        # -----------------------------------------------------------
        # 将图像重塑为像素列表 (Height * Width, 3)
        data = img_blur.reshape((-1, 3))
        data = np.float32(data)

        # 定义 K-Means 标准 (type, max_iter, epsilon)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # 执行 K-Means
        # ret: 紧密度
        # label: 每个像素所属的中心索引
        # center: 中心点（即聚类后的颜色）
        ret, label, center = cv2.kmeans(data, k_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # 将中心点转换回 uint8
        center = np.uint8(center)
        
        # 重塑 label 以匹配图像尺寸
        label_img = label.reshape((height, width))
        
        # 确定背景颜色索引（如果需要）
        bg_label_idx = -1
        if transparent_background:
            # 简单策略：取四个角的颜色出现频率最高的作为背景色
            corners = [
                label_img[0, 0],
                label_img[0, width-1],
                label_img[height-1, 0],
                label_img[height-1, width-1]
            ]
            # 找到众数
            bg_label_idx = max(set(corners), key=corners.count)
            print(f"检测到背景颜色索引: {bg_label_idx} (将被移除)")

        # -----------------------------------------------------------
        # 2. 生成 SVG
        # -----------------------------------------------------------
        svg_content = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" version="1.1">',
            # f'<rect width="{width}" height="{height}" fill="white"/>' # 可选背景
        ]

        # 遍历每种颜色，提取对应的轮廓
        for i in range(k_colors):
            # 如果启用了透明背景，且当前颜色是背景色，则跳过
            if transparent_background and i == bg_label_idx:
                continue

            # 获取当前颜色的 BGR 值
            color = center[i]
            # 转换为 Hex 颜色字符串或 RGB 字符串
            # OpenCV 是 BGR，SVG 需要 RGB
            hex_color = "#{:02x}{:02x}{:02x}".format(color[2], color[1], color[0])
            
            # 创建当前颜色的掩膜 (mask)
            # label_img == i 会得到一个 boolean 矩阵，转换为 uint8 (0 或 255)
            mask = np.uint8(label_img == i) * 255
            
            # 查找轮廓
            # RETR_LIST: 检索所有轮廓
            # CHAIN_APPROX_SIMPLE: 压缩点
            contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            # 收集该颜色的所有路径数据
            color_paths = []
            
            for contour in contours:
                # 过滤太小的区域
                if cv2.contourArea(contour) < min_area:
                    continue
                    
                if len(contour) < 3:
                    continue
                
                # 构建路径数据
                path_data = []
                start_point = contour[0][0]
                path_data.append(f"M {start_point[0]},{start_point[1]}")
                
                for point in contour[1:]:
                    p = point[0]
                    path_data.append(f"L {p[0]},{p[1]}")
                
                path_data.append("Z")
                color_paths.append(" ".join(path_data))
                
            # 将该颜色的所有轮廓合并到一个 path 元素中
            # 使用 fill-rule="evenodd" 可以正确处理孔洞（挖空）
            if color_paths:
                full_path_str = " ".join(color_paths)
                svg_content.append(f'<path d="{full_path_str}" fill="{hex_color}" stroke="none" fill-rule="evenodd" />')

        svg_content.append('</svg>')

        # -----------------------------------------------------------
        # 3. 保存文件
        # -----------------------------------------------------------
        if output_path is None:
            filename, _ = os.path.splitext(input_path)
            output_path = f"{filename}.svg"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(svg_content))
            
        print(f"转换完成！SVG 已保存至: {output_path}")
        print(f"使用的颜色数量: {k_colors}")

    except ImportError:
        print("错误：缺少必要的库。请运行: pip install opencv-python numpy")
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        import cv2
    except ImportError:
        print("错误：未安装 opencv-python。")
        print("请在终端运行: pip install opencv-python")
        sys.exit(1)

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        k = 8
        transparent = False
        
        # 解析额外参数
        if len(sys.argv) > 2:
            # 简单的参数解析逻辑
            for arg in sys.argv[2:]:
                if arg.isdigit():
                    k = int(arg)
                elif arg.lower() in ['--transparent', '-t', 'transparent']:
                    transparent = True
        
        # 去除两端的引号
        input_file = input_file.strip('"').strip("'")
        
        if os.path.exists(input_file):
            image_to_svg(input_file, k_colors=k, transparent_background=transparent)
        else:
            print(f"找不到文件: {input_file}")
            
    else:
        print("请输入要转换的图片文件名（支持 jpg, png 等）：")
        input_file = input("文件名: ").strip()
        print("请输入颜色数量 (默认 8): ")
        k_input = input("颜色数量: ").strip()
        k = int(k_input) if k_input.isdigit() else 8
        
        print("是否移除背景（透明）？(y/n, 默认 n): ")
        t_input = input("选择: ").strip().lower()
        transparent = t_input == 'y' or t_input == 'yes'

        # 去除两端的引号
        input_file = input_file.strip('"').strip("'")

        if os.path.exists(input_file):
            image_to_svg(input_file, k_colors=k, transparent_background=transparent)
        else:
            print(f"找不到文件: {input_file}")
