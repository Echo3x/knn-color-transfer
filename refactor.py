from PIL import Image


def deal(content, style):
    # 打开image， 并且统一转换为RGB
    # c_img = Image.open(content)
    c_img = content
    c_img_rgb = c_img.convert("RGB")
    # s_img = Image.open(style)
    s_img = style
    s_img_rgb = s_img.convert("RGB")

    # resize to 256x256 ， avoid dimensionality explosion
    handled_content = c_img_rgb.resize((256, 256))
    handled_style = s_img_rgb.resize((256, 256))


    return handled_content, handled_style





