import os
import cv2
import pytesseract
# os.environ['TESSDATA_PREFIX'] = './'


def ocr_img(path):
    # bw_h = (box[5] - box[1]) * 0.2
    # bw_w = (box[4] - box[0]) * 0.08
    # p_img = self.img[int(box[1] + bw_h):int(box[5] - bw_h), int(box[0] + bw_w):int(box[4] - bw_w)]
    # img_rgb = Image.frombytes('RGB', p_img.shape[:2], p_img, 'raw', 'BGR', 0, 0)
    # 将图片转为灰度图像
    p_img = cv2.imread(path)
    gray = cv2.cvtColor(p_img, cv2.COLOR_BGR2GRAY)

    # 对图像进行二值化处理
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # useless psm  8 9 10 11 12
    config = '--oem 3 --psm 6'  # can not recognize '29"'
    #  -c tessedit_char_whitelist=0123456789xXsSmMlL.cC/
    config = '--psm 7'

    # img_str = pytesseract.image_to_string(p_img, lang='eng', config=config)
    img_str = pytesseract.image_to_string(p_img, config=config)
    img_str = img_str.replace("\n", "")

    cv2.imshow(f'{img_str}', gray)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.imwrite(f'./ocr/{img_str}.jpg', p_img)


def extract_table(path):
    p_img = cv2.imread(path)
    gray = cv2.cvtColor(p_img, cv2.COLOR_BGR2GRAY)

    # 对图像进行二值化处理
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    config = ''

    img_str = pytesseract.image_to_string(p_img, config=config)
    print(img_str)


if __name__ == '__main__':
    import os
    # origin_dir = "./origin"
    #
    # for root, dirs, files in os.walk(origin_dir):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         ocr_img(file_path)

    # extract_table('./org_table/adidas_1_tb_1.jpg')
    """
    Product label 2XS (00) XS (0-2) M (8-10) L (12-14) XL (16-18) 2XL (20)

    BUST 28.5 - 29.5" 30 - 32° 32.5 - 34.5" 35 - 37" 37.5 - 40" 40.5 - 43" 43.5 - 46.5°
    
    Waist 22 - 23.5" 24 - 26° 26.5 - 28.5" 29 - 31° 31.5 - 33.5" 34 - 37 37.5 - 41"
    
    Hip 31.5 - 33° 33.5 - 35.5" 36 - 38" 38.5 - 40.5" 41-43" 43.5 - 46" 465-49"
    """

    extract_table('./org_table/adidas_2_tb_1.jpg')
    """
    Product label XL Tall 2XL Tall

    Waist 26.5 - 28.5" 29 - 31 31.5 - 33.5" 34 - 37 37.5 - 41°
    
    Hip 36 - 38" 38.5 - 40.5 41-43" 43.5 - 46° 46.5 - 49°
    
    Inseam 33” 33.5" 33.5" 33.5" 34"
    """

