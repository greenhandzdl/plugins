from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me


# 导入nonebot，markdown，imgkit，nonebot_plugin_saa，os和datetime模块
import markdown
import imgkit
import nonebot_plugin_saa
import os # new
import datetime # new

# 定义一个命令处理器，响应用户输入的"md_generate"指令，并且需要@机器人
md_generate_cmd = on_command("md_generate", rule=to_me(), priority=5)

# 定义命令处理函数，并回复给用户
@md_generate_cmd.handle()
async def handle_md_generate(bot: Bot, event: Event, state: T_State):
    # 获取用户输入的markdown文本
    md_text = event.get_plaintext().strip()
    md_text = md_text.replace("/md_generate", "").strip()
    # 如果没有输入文本，提示用户
    if not md_text:
        await bot.send(event, "请输入markdown文本")
        return
    # 调用markdown模块的markdown函数，将markdown文本转换为html文本
    html_text = markdown.markdown(md_text)
    # 获取发送者的id和当前时间，并拼接成一个文件名
    sender_id = event.sender.user_id # new
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # new
    file_name = f"{event.sender.nickname}_{sender_id}_{current_time}.png" # new
    # 检查并创建 ./cookie 文件夹
    if not os.path.exists("./cookie"):
        os.makedirs("./cookie")
    # 拼接一个文件路径，使用./cookie目录和文件名
    file_path = os.path.join("./cookie", file_name) # new
    # 调用imgkit模块的from_string函数，将html文本转换为png图片，并保存到文件路径中
    imgkit.from_string(html_text, file_path) # new
    # 使用MessageFactory类构建消息，使用文件路径作为图片源
    msg = nonebot_plugin_saa.MessageFactory(nonebot_plugin_saa.Image(file_path)) 
    # 使用bot对象发送消息给用户，回复原消息并@用户
    await bot.send( reply=True, at_sender=True)

    # 结束命令处理
    await md_generate_cmd.finish()