# orm 用法
## 基本用法
### 增
```
table_obj = TableClass.objects.create([**columns_dict])
```
### 删
```
table_obj = TableClass.objects.filter(**param_dict).first()
table_obj.delete()
```
### 改
```
table_obj = TableClass.objects.filter(**param_dict).first()
table_obj.column1 = value1
table_obj.column2 = value2
table_obj.save()
```
### 查
```
# 查询单条记录
table_obj = TableClass.objects.get(**params_dict)
# 随意查啦
table_obj = TableClass.objects.filter(**params_dict).first()
table_obj_list = TableClass.objects.filter(**params_dict).all()

# 根据指定column排序查询'-' 倒序
table_obj_list = TableClass.objects.filter(**params_dict).order_by('-column').all()

# 分页 start_index:其实下标,0开始,   查询结果包括start_index数据,不包括end_index数据
table_obj_list = TableClass.objects.filter(**params_dict)[start_index:end_index]
```
**注**: get查询不存在时报错(TableClass matching query does not exist),且get只适用于查询结果有且只有一条记录的情况(不一定根据id查询,只要查询是一条记录就正常,否则报错)
* 另外一种分页,效率待测试 ,不知道底层实现
```
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
```
TableClass.objects.filter(Q(column__contains=keyword)).all()
```
* 范围查询
```
TableClass = SaasLessee.objects.filter(column__range=(start_datetime, end_datetime)).all()  ## 包含头尾
TableClass = SaasLessee.objects.filter(column__lte=value).all()  # 小于等于
TableClass = SaasLessee.objects.filter(column__gte=value).all()  # 大于等于
```
* 多条件 Q `'&'`和 `'|'`
```
TableClass = SaasLessee.objects.filter(Q(column1__gte=value) | Q(column2__lt=value)).all()
```
