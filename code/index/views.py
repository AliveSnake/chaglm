from django.shortcuts import render, HttpResponse


# Create your views here.


# Create your views here.
def index(request):
    return HttpResponse('''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Serverless Devs - Powered By Serverless Devs</title>
    <link href="https://example-static.oss-cn-beijing.aliyuncs.com/web-framework/style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="website">
    <div class="ri-t">
        <h1>Chatgml</h1>
        <h2>这是一个 Django 项目</h2>
        <span>自豪地通过Serverless Devs进行部署</span>
        <br/>
        <p>快速体验： <br/>
            • 下载Serverless Devs工具：npm install @serverless-devs/s<br/>
            • 初始化项目：s init start-django-v3<br/>

            • 项目部署：s deploy<br/>
            <br/>
            Serverless Devs Coming soon...
        </p>
    </div>
</div>
</body>
</html>''')
