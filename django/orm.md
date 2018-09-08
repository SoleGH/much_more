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

```
