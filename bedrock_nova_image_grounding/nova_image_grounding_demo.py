import base64
import boto3
import io
import json
import re
import os
import gradio as gr

from PIL import Image, ImageDraw, ImageFont

# 初始化Amazon Bedrock客户端
modelId = "us.amazon.nova-lite-v1:0"  # 默认使用nova-lite-v1模型
accept = "application/json"
contentType = "application/json"

try:
    bedrock_rt = boto3.client("bedrock-runtime", region_name="us-east-1")
except Exception as e:
    print(f"初始化Bedrock客户端时出错: {e}")
    print("请确保您已配置AWS凭证")

# 从notebook中复制的辅助函数
def safe_json_load(json_string):
    try:
        json_string = re.sub(r"\s", "", json_string)
        json_string = re.sub(r"\(", "[", json_string)
        json_string = re.sub(r"\)", "]", json_string)
        bbox_set = {}
        for b in re.finditer(r"\[\d+,\d+,\d+,\d+\]", json_string):
            if b.group(0) in bbox_set:
                json_string = json_string[:bbox_set[b.group(0)][1]] + "}]"
                break
            bbox_set[b.group(0)] = (b.start(), b.end())
        else:
            if bbox_set:  # 确保bbox_set不为空
                json_string = json_string[:bbox_set[b.group(0)][1]] + "}]"
        json_string = re.sub(r"\]\},\]$", "]}]", json_string)
        json_string = re.sub(r"\]\],\[\"", "]},{\"", json_string)
        json_string = re.sub(r"\]\],\[\{\"", "]},{\"", json_string)
        json_string = re.sub(r"\",\[", "\":[", json_string)
        return json.loads(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return []

# 修改后的检测函数，适应Gradio接口
def detection(image, category_input, model_choice, image_short_size=360):
    global modelId
    
    # 更新模型ID
    modelId = model_choice
    
    # 解析类别列表
    category_list = [cat.strip() for cat in category_input.split(",")]
    if not category_list or category_list[0] == "":
        return None, "请输入至少一个检测类别"
    
    try:
        # 处理图像
        if isinstance(image, str):  # 如果是文件路径
            image_pil = Image.open(image)
        elif isinstance(image, Image.Image):  # 如果是PIL Image对象
            image_pil = image
        elif image is not None:  # 如果是numpy数组
            image_pil = Image.fromarray(image)
        else:
            return None, "未提供有效的图像"
        
        width, height = image_pil.size
        
        ratio = image_short_size / min(width, height)
        width = round(ratio * width)
        height = round(ratio * height)
        
        image_pil = image_pil.resize((width, height), resample=Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image_pil.save(buffer, format="webp", quality=90)
        image_data = buffer.getvalue()
        
        # 构建提示
        category_str = ",".join([f'"{category.lower()}"' for category in category_list])
        
        prompts = f"""
Detect bounding box of objects in the image, only detect {category_str} category objects with high confidence, output in a list of bounding box format.
        
Output example:
        
[
    {{"{category_list[0].lower().replace(' ', '_')}": [x1, y1, x2, y2]}},
    ...
]
"""
        
        prefill="""
[
    {"
""".strip("\n")
        
        # 构建请求
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": 'webp',
                            "source": {
                                "bytes": image_data,
                            }
                        }
                    },
                    {
                        "text": prompts
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "text": prefill
                    },
                ],
            }
        ]
        
        # 调用模型
        response = bedrock_rt.converse(
            modelId=modelId, 
            messages=messages,
            inferenceConfig={
                "temperature": 0.0,
                "maxTokens": 1024,
            },
        )
        
        output = prefill + response.get('output')["message"]["content"][0]["text"]
        result = safe_json_load(output)
        
        # 绘制结果
        color_list = [
            'blue',
            'green',
            'yellow',
            'red',
            'orange',
            'pink',
            'purple',
        ]
        
        try:
            font = ImageFont.truetype("Arial", size=height // 20)
        except IOError:
            # 如果找不到Arial字体，使用默认字体
            font = ImageFont.load_default()
        
        log_output = []
        for idx, item in enumerate(result):
            label = next(iter(item))
            bbox = item[label]
            x1, y1, x2, y2 = bbox
            
            if x1 >= x2 or y1 >= y2:
                continue
                
            w, h = image_pil.size
            x1 = x1 / 1000 * w
            x2 = x2 / 1000 * w
            y1 = y1 / 1000 * h
            y2 = y2 / 1000 * h
            
            bbox = (x1, y1, x2, y2)
            bbox = list(map(round, bbox))
            
            log_message = f"检测到 <{label}> 在坐标 {bbox}"
            log_output.append(log_message)
            
            # 绘制边界框
            draw = ImageDraw.Draw(image_pil)
            color = color_list[idx % len(color_list)]
            draw.rectangle(bbox, outline=color, width=2)
            draw.text((x1 + 4, y1 + 2), label, fill=color, font=font)
        
        return image_pil, "\n".join(log_output)
    
    except Exception as e:
        return None, f"处理过程中出错: {str(e)}"

# 创建Gradio界面
def create_demo():
    with gr.Blocks(title="Amazon Nova 图像检测演示") as demo:
        gr.Markdown("# Amazon Nova 图像检测演示")
        gr.Markdown("使用Amazon Nova模型检测图像中的物体。上传图片并指定要检测的对象类别。")
        
        with gr.Row():
            with gr.Column():
                # 输入部分
                image_input = gr.Image(type="pil", label="上传图片")
                category_input = gr.Textbox(
                    label="检测类别（用逗号分隔多个类别）", 
                    placeholder="例如: car, dog, cat",
                    value="bottle"
                )
                model_choice = gr.Dropdown(
                    choices=["us.amazon.nova-lite-v1:0", "us.amazon.nova-pro-v1:0"],
                    value="us.amazon.nova-lite-v1:0",
                    label="选择模型"
                )
                image_size = gr.Slider(
                    minimum=360, 
                    maximum=1920, 
                    value=480, 
                    step=4, 
                    label="图像短边尺寸"
                )
                detect_button = gr.Button("开始检测")
                
            with gr.Column():
                # 输出部分
                image_output = gr.Image(label="检测结果")
                text_output = gr.Textbox(label="检测日志", lines=5)
        
        # 示例图片
        example_images = [
            ["./test_images/bottle.webp", "bottle"],
            ["./test_images/cat_dog_car.webp", "car, dog, cat"],
            ["./test_images/cakes.webp", "cake"],
            ["./test_images/unripe_strawberry.webp", "unripe strawberry"],
        ]
        
        gr.Examples(
            examples=example_images,
            inputs=[image_input, category_input],
        )
        
        # 设置事件处理
        detect_button.click(
            fn=detection,
            inputs=[image_input, category_input, model_choice, image_size],
            outputs=[image_output, text_output]
        )
        
        gr.Markdown("""
        ## 使用说明
        
        1. 上传一张图片或使用示例图片
        2. 输入要检测的对象类别，多个类别用逗号分隔
        3. 选择要使用的Amazon Nova模型版本
        4. 调整图像处理尺寸（较大的尺寸可能提高检测精度，但会增加处理时间）
        5. 点击"开始检测"按钮
        
        ## 注意事项
        
        - 此演示需要有效的AWS凭证配置，以访问Amazon Bedrock服务
        - Nova模型对于特定类别的检测效果可能会有所不同
        - 对于复杂场景，可以尝试使用更具体的类别描述
        """)
    
    return demo

# 启动Gradio应用
if __name__ == "__main__":
    demo = create_demo()
    demo.launch(share=False, server_name="0.0.0.0", server_port=8000, show_api=False) 
