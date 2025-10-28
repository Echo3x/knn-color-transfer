import streamlit as st
from PIL import Image
import numpy as np

from knn_color_transfer import color_transfer

# 支持 HEIC（需先 pip install pillow-heif）
try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    heic_support = True
except ImportError:
    heic_support = False

st.title("🎨 色彩风格迁移演示")

# 注意：Apple HEIF 照片的扩展名是 .heic
allowed_types = ["png", "jpg", "jpeg"]
if heic_support:
    allowed_types.append("heic")
else:
    st.info("（未安装 HEIC 支持，无法上传 Apple HEIF 照片）")

content_img = st.file_uploader("上传内容图", type=allowed_types)
style_img = st.file_uploader("上传风格图", type=allowed_types)
print(content_img)
print(style_img)

# button = st.button("Start")

# 按钮点击后才触发处理逻辑
if st.button("Start"):
    # 先检查是否上传了两个文件
    if not (content_img and style_img):
        st.warning("请先上传内容图和风格图！")
    else:
        try:
            content_pil = Image.open(content_img)
            style_pil = Image.open(style_img)
            print(content_pil.format)  # 若 content_pil 是 None，直接报错
            print(style_pil.format)  # 若 content_pil 是 None，直接报错

            result = color_transfer(content_pil, style_pil)
            print("color_transfer 返回值:", result)  # 看终端输出是否为 None

            st.image(result, caption="迁移结果")
            st.success("迁移完成！")
            st.image(content_pil, caption="内容图", width=300)
            st.image(style_pil, caption="风格图", width=300)

        except Exception as e:
            st.error(f"处理失败: {e}")