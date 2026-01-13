# 数据导入说明

## 数据文件

项目包含两个CSV数据文件：
- `pr_prediction_results.csv` - PR预测结果数据
- `top_pre.csv` - PR关联的仓库日志数据

## 导入方法

### 方法1：使用MySQL命令行导入（推荐）

```bash
# 登录MySQL
mysql -u your_username -p your_database_name

# 导入数据
LOAD DATA LOCAL INFILE 'pr_prediction_results.csv'
INTO TABLE pr_prediction_results
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'top_pre.csv'
INTO TABLE top_pre
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### 方法2：使用Python脚本导入

```python
import pandas as pd
import pymysql
from config import DB_CONFIG

# 连接数据库
conn = pymysql.connect(**DB_CONFIG)

# 读取CSV文件
df_pr = pd.read_csv('pr_prediction_results.csv')
df_top = pd.read_csv('top_pre.csv')

# 导入数据（如果表已存在，使用INSERT IGNORE避免重复）
df_pr.to_sql('pr_prediction_results', conn, if_exists='append', index=False)
df_top.to_sql('top_pre', conn, if_exists='append', index=False)

conn.close()
```

## 注意事项

1. 确保CSV文件的编码为UTF-8
2. 确保CSV文件的第一行是列名（表头）
3. 导入前请先执行 `init_database.sql` 创建表结构
4. 如果数据量较大，建议分批导入或使用 `LOAD DATA INFILE` 命令

