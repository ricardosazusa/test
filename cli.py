import urllib.request
import click
import string
import random
import time
from datetime import datetime
import json
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


@click.group()
def cli():
    """dev-helper: 程序员/学生日常效率命令行工具箱"""
    pass

@cli.command()
def version():
    """查看当前版本号"""
    click.echo("dev-helper version 1.0.0")

@cli.command()
@click.option('-l', '--length', default=12, type=int, help='密码长度，默认为 12 位')
def pass_gen(length):
    """生成随机强密码/Token工具"""
    # 定义密码包含的字符集：大小写字母 + 数字 + 特殊符号
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # 随机抽取 length 个字符并拼接成字符串
    password = ''.join(random.choice(chars) for _ in range(length))
    
    click.echo(f"生成的随机密码 ({length} 位): {password}")
def run():
    """公网IP查询主逻辑，调用无追踪开源免费API获取IP和归属地"""
    try:
        # 1. 获取当前公网IP（无埋点开源API，DigitalOcean维护）
        public_ip = urlopen("https://api.ipify.org", timeout=5).read().decode("utf-8").strip()
        # 2. 获取IP地理位置信息（无追踪免费教育向API）
        res = urlopen(f"https://ipapi.co/{public_ip}/json/", timeout=8).read().decode("utf-8")
        geo = json.loads(res)

        # 3. 格式化友好终端输出
        print("🌐 公网IP查询结果")
        print(f" IP地址:    {public_ip}")
        print(f" 国家:      {geo.get('country_name', '未知')}")
        print(f" 城市:      {geo.get('city', '未知')}")
        print(f" 时区:      {geo.get('timezone', '未知')}")
        print(f" 运营商:    {geo.get('org', '未知')}")

    except (URLError, HTTPError):
        print("❌ 网络请求失败，请检查网络连接", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ API返回数据异常", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


@cli.command(name="ip", help="查询本机公网IP及归属地信息")
def ip_cmd():
    run()
@cli.command()
@click.option('--ts', type=int, help='需要转换的时间戳 (秒)')
def time_conv(ts):
    """时间戳转换工具"""
    if ts:
        dt = datetime.fromtimestamp(ts)
        click.echo(f"转换结果:{dt.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        click.echo(f"当前时间戳: {int(time.time())}")    
if __name__ == '__main__':
    cli()
