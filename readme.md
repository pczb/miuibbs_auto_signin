#miui论坛自动签到包括geek论坛
##使用方法
`python miui_login.py username password`

`username` 表示 `用户名` `password` 表示 `密码`

##新增weibo自动Key获取类oauth
oauth的参数分别为`appkey`, `redirect_url`, `app_secret`
如果要获取授权码`code` 请使用函数 `getToken(username, pwd)`


如果要获取`access_key` 请先获得 `code` 然后调用`get_access_token(code)`
