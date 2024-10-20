# JuiceFS WebUI

这个项目基于 Flask + YAML 开发，让用户在本地浏览器中管理 JuiceFS 文件系统，并在浏览器中进行格式化操作。

对于一个已经格式化的 JuiceFS 文件系统来说，元数据引擎是不变的，对象存储的访问地址是不变的，AK、SK 也是不变的，所以我们可以将这些信息保存在一个本地的 YAML 配置文件中，在 Web 界面添加文件系统记录并进行统一管理。

⚠️ 需要注意的是，这是一个爱好者项目，不保证稳定性和安全性，请自行评估潜在的风险。

## 使用方法

```sh
# 克隆项目
git clone https://github.com/yuhr123/juicefs-webui.git

# 安装依赖
cd juicefs-webui
pipenv --python 3
pipenv install

# 下载 JuiceFS 客户端到当前目录
curl -sSL https://d.juicefs.com/install | sh -s .

# 启动 WebUI
pipenv shell
python app.py
```
