import pytest
import sys
import json
from io import StringIO
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
# 关键补充导入
from urllib.error import URLError, HTTPError
from cli import cli, run, pass_gen, time_conv, version

runner = CliRunner()

# 测试 version 命令
def test_version_command():
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "dev-helper version 1.0.0" in result.output

# 测试密码生成：默认12位
def test_pass_gen_default_length():
    result = runner.invoke(cli, ["pass-gen"])
    pwd = result.output.split(": ")[-1].strip()
    assert len(pwd) == 12

# 测试密码生成：自定义长度16位
def test_pass_gen_custom_length():
    result = runner.invoke(cli, ["pass-gen", "-l", "16"])
    pwd = result.output.split(": ")[-1].strip()
    assert len(pwd) == 16

# 测试时间戳转换：无参数输出当前时间戳
def test_time_conv_no_ts():
    result = runner.invoke(cli, ["time-conv"])
    assert "当前时间戳:" in result.output
    ts_str = result.output.split(": ")[1].strip()
    assert ts_str.isdigit()

# 测试时间戳转换：指定时间戳转换
def test_time_conv_with_ts():
    test_ts = 1751385600
    result = runner.invoke(cli, ["time-conv", "--ts", str(test_ts)])
    from datetime import datetime
    target_time = datetime.fromtimestamp(test_ts).strftime("%Y-%m-%d %H:%M:%S")
    assert target_time in result.output

# 测试run()正常获取IP和地理信息
@patch("cli.urlopen")
def test_run_ip_success(mock_urlopen):
    mock_ip_resp = MagicMock()
    mock_ip_resp.read.return_value = b"1.1.1.1"
    mock_geo_resp = MagicMock()
    geo_info = {
        "country_name": "China",
        "city": "Beijing",
        "timezone": "Asia/Shanghai",
        "org": "China Unicom"
    }
    mock_geo_resp.read.return_value = json.dumps(geo_info).encode("utf-8")
    mock_urlopen.side_effect = [mock_ip_resp, mock_geo_resp]

    capture_stdout = StringIO()
    original_stdout = sys.stdout
    sys.stdout = capture_stdout
    run()
    sys.stdout = original_stdout

    output = capture_stdout.getvalue()
    assert "1.1.1.1" in output
    assert "China" in output
    assert "Beijing" in output
    assert "China Unicom" in output

# 测试网络异常（修复导入问题）
@patch("cli.urlopen", side_effect=URLError("connection timeout"))
def test_run_network_exception(mock_urlopen):
    with pytest.raises(SystemExit) as exit_info:
        run()
    assert exit_info.value.code == 1

# 测试API返回非法JSON解析失败
@patch("cli.urlopen")
def test_run_json_decode_error(mock_urlopen):
    mock_ip_resp = MagicMock()
    mock_ip_resp.read.return_value = b"1.1.1.1"
    mock_bad_json_resp = MagicMock()
    mock_bad_json_resp.read.return_value = b"{{invalid json data"
    mock_urlopen.side_effect = [mock_ip_resp, mock_bad_json_resp]

    with pytest.raises(SystemExit) as exit_info:
        run()
    assert exit_info.value.code == 1

# 测试ip子命令
def test_ip_command_invoke():
    with patch("cli.run") as mock_run_func:
        result = runner.invoke(cli, ["ip"])
        assert result.exit_code == 0
        mock_run_func.assert_called_once()