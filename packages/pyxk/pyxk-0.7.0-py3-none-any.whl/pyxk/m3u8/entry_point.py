import click
from pyxk import get_user_agent
from pyxk.m3u8 import load_url, load_content


@click.group(invoke_without_command=False, chain=False)
@click.option("-o", "--output", "output", type=str, default=None, help="M3U8存储路径")
@click.option("--reload", is_flag=True, help="重载m3u8资源")
@click.option("--reserve", is_flag=True, help="保留m3u8资源")
@click.option("-h", "--headers", "headers", type=(str, str), multiple=True, help="Request Headers")
@click.option("--no-verify", "verify", is_flag=True, default=True, help="Request Verify")
@click.option("-l", "--limit", "limit", type=int, default=16, help="下载并发量")
@click.option("-ua", "--user-agent", "user_agent", type=str, default=None, help="User-Agent")
@click.pass_context
def main(ctx, output, reload, reserve, headers, verify, limit, user_agent):
    """m3u8下载器"""
    ctx.obj = {}
    # 将参数传递给子命令
    if ctx.invoked_subcommand:
        ctx.obj.update(ctx.params)


@main.command
@click.pass_obj
@click.argument("content", type=str, metavar="<File>")
@click.option("-u", "--url", "_url", type=str, default=None, help="m3u8 url")
@click.option("-o", "--output", "output", type=str, default=None, help="M3U8存储路径")
@click.option("--reload", is_flag=True, help="重载m3u8资源")
@click.option("--reserve", is_flag=True, help="保留m3u8资源")
@click.option("-h", "--headers", "headers", type=(str, str), multiple=True, help="Request Headers")
@click.option("--no-verify", "verify", is_flag=True, default=True, help="Request Verify")
@click.option("-l", "--limit", "limit", type=int, default=None, help="下载并发量")
@click.option("-ua", "--user-agent", "user_agent", type=str, default=None, help="User-Agent")
def file(obj, content, _url, output, reload, reserve, headers, verify, limit, user_agent):
    """使用m3u8文件下载资源"""
    load_content(
        content=content,
        url=_url,
        output=output or obj["output"],
        reload=reload,
        reserve=reserve,
        headers=dict(headers or obj["headers"]),
        verify=verify,
        limit=limit or obj["limit"],
        user_agent=get_user_agent(user_agent or obj["user_agent"])
    )


@main.command
@click.pass_obj
@click.argument("_url", type=str, metavar="<Url>")
@click.option("-o", "--output", "output", type=str, default=None, help="M3U8存储路径")
@click.option("--reload", is_flag=True, help="重载m3u8资源")
@click.option("--reserve", is_flag=True, help="保留m3u8资源")
@click.option("-h", "--headers", "headers", type=(str, str), multiple=True, help="Request Headers")
@click.option("--no-verify", "verify", is_flag=True, default=True, help="Request Verify")
@click.option("-l", "--limit", "limit", type=int, default=None, help="下载并发量")
@click.option("-ua", "--user-agent", "user_agent", type=str, default=None, help="User-Agent")
def url(obj, _url, output, reload, reserve, headers, verify, limit, user_agent):
    """使用m3u8链接下载资源"""
    load_url(
        url=_url,
        output=output or obj["output"],
        reload=reload,
        reserve=reserve,
        headers=dict(headers or obj["headers"]),
        verify=verify,
        limit=limit or obj["limit"],
        user_agent=get_user_agent(user_agent or obj["user_agent"])
    )
