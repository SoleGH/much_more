# django

<!-- TOC -->

- [django](#django)
    - [同步表结构](#同步表结构)
        - [建表](#建表)
        - [修改表](#修改表)
    - [数据库操作](#数据库操作)
        - [增](#增)
        - [删](#删)
        - [改](#改)
        - [查](#查)

<!-- /TOC -->

## 同步表结构
**所有操作需要在项目manage.py同目录下运行**
### 建表
```
$ python manage.py makemigrations appname
$ python manage.py migrate appname
```
###  修改表
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
```python
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

## 数据库操作

### 增
```python
table_obj = TableClass.objects.create([**columns_dict])
```

### 删
```python
table_obj = TableClass.objects.filter(**param_dict).first()
table_obj.delete()
```

### 改
```python
table_obj = TableClass.objects.filter(**param_dict).first()
table_obj.column1 = value1
table_obj.column2 = value2
table_obj.save()
```

### 查
* get:查询单条记录(且只能查询单条,否则报错)
```python
table_obj = TableClass.objects.get(**params_dict)
```

**注**: get查询不存在时报错(TableClass matching query does not exist),且get只适用于查询结果有且只有一条记录的情况(不一定根据id查询,只要查询是一条记录就正常,否则报错)
* `get`底层实现 django/db/models/query.py
```python
def get(self, *args, **kwargs):
        """
        Perform the query and return a single object matching the given
        keyword arguments.
        """
        clone = self.filter(*args, **kwargs)
        if self.query.can_filter() and not self.query.distinct_fields:
            clone = clone.order_by()
        num = len(clone)
        if num == 1:  # 有且只有一条记录时,返回记录
            return clone._result_cache[0]
        if not num:  # 未查询到记录,抛出异常 DoesNotExist
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        # 超过一条记录,抛出异常 MultipleObjectsReturned
        raise self.model.MultipleObjectsReturned(
            "get() returned more than one %s -- it returned %s!" %
            (self.model._meta.object_name, num)
        )
```

* `filter`查询  
```python
# 随意查啦
table_obj = TableClass.objects.filter(**params_dict).first()
table_obj_list = TableClass.objects.filter(**params_dict).all()
# 根据指定column排序查询'-' 倒序
table_obj_list = TableClass.objects.filter(**params_dict).order_by('-column').all()
# 分页 start_index:其实下标,0开始,   查询结果包括start_index数据,不包括end_index数据
table_obj_list = TableClass.objects.filter(**params_dict)[start_index:end_index]
```

* 另外一种分页,效率待测试 ,不知道底层实现
```python
obj_list = TableClass.objects.filter(**params_dict).order_by('-update_datetime')
paginator = Paginator(obj_list, page_size)  # page_size 每页记录条数
try:
    obj_list_part = paginator.page(page_num)  # page_num 页码,从1开始
except PageNotAnInteger:
    obj_list_part = paginator.page(1)
except EmptyPage:
    obj_list_part = paginator.page(paginator.num_pages)  # paginator.numpages 获取最后一页
```

* 模糊查询
```python
TableClass.objects.filter(Q(column__contains=keyword)).all()
```

* 范围查询
```python
result = TableClass.objects.filter(column__range=(start_datetime, end_datetime)).all()  ## 包含头尾
result = TableClass.objects.filter(column__lte=value).all()  # 小于等于
result = TableClass.objects.filter(column__gte=value).all()  # 大于等于
result = TableClass.objects.filter(column__in=value_list).all()
```

* 多条件 Q `'&'`和 `'|'`
```python
result = TableClass.objects.filter(Q(column1__gte=value) | Q(column2__lt=value)).all()
```