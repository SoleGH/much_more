## 使用manager生成/修改表结构
**所有操作需要在项目manage.py同目录下运行**
### 建表
```
$ python manage.py makemigrations appname
$ python manage.py migrate appname
```
#  修改表
* 有历史版本文件直接运行同步命令就可以
```
# 若appname下有migrations文件夹,并存在历史版本文件,这直接运行
$ python manage.py makemigrations appname
$ python manage.py migrate
```
* 若无法正常工作则需要删除历史文件重新
1. 将models修改为于数据库结构相同(注释修改部分就行);
2. 运行 `makemigrations`,在`appname/migrations`文件夹下生成原始结构文件;
3. 增加修改部分,再次运行`makemigrations`指令,生成第二个结构文件,
4. 执行`migrate`指令,即可同步表结构,若操作失败可以尝试删除第一个文件并,修改第二个文件对第一个文件的依赖
```
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone
class Migration(migrations.Migration):
    dependencies = [
        ('dzh', '0001_initial'),  # 删除此行,不依赖其他文件
    ]
    operations = [
        migrations.CreateModel(
            name='SaasLesseeIP',
            fields=[
                ('uid', models.CharField(primary_key=True, max_length=16, serialize=False)),
                ('ip', models.CharField(max_length=15, default='')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
```
