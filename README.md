# PR预测风险大屏系统

一个基于机器学习的PR（Pull Request）风险预测和可视化大屏系统，用于实时监控和分析代码仓库的PR风险情况。

## 项目简介

本项目是一个前后端分离的Web应用，通过分析PR的历史数据，预测PR的合并风险和处理时长，并通过可视化大屏实时展示关键指标。

### 主要功能

- **风险统计**：实时展示低风险和高风险PR的分布情况
- **Top10高风险PR**：展示风险概率最高的10个PR
- **PR风险概率**：随机展示10个PR的风险概率分布
- **时序趋势分析**：展示PR风险和效率的时间趋势
- **仓库效率排行**：按平均处理时长排序的仓库效率排行
- **PR详情查看**：点击PR可查看详细的风险归因信息

## 技术栈

### 后端
- **Python 3.9+**
- **Flask** - Web框架
- **PyMySQL** - MySQL数据库连接
- **Flask-CORS** - 跨域支持
- **Pandas** - 数据处理

### 前端
- **Vue 3** - 前端框架
- **Vite** - 构建工具
- **ECharts** - 数据可视化
- **Axios** - HTTP客户端
- **Vue Router** - 路由管理

## 项目结构

```
openrank/
├── backend/                    # 后端代码
│   ├── app.py                 # Flask应用主文件
│   ├── model.py               # 机器学习模型
│   ├── config.example.py      # 配置文件示例
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # Python依赖
│   ├── init_database.sql      # 数据库初始化脚本
│   ├── import_data.md         # 数据导入说明
│   ├── pr_prediction_results.csv  # PR预测结果数据
│   └── top_pre.csv            # PR关联的仓库日志数据
├── web/                       # 前端代码
│   ├── src/
│   │   ├── api/               # API接口
│   │   │   └── screenApi.js
│   │   ├── components/        # Vue组件
│   │   │   ├── EfficiencyPanel.vue
│   │   │   ├── PrDetailModal.vue
│   │   │   ├── RiskBoard.vue
│   │   │   └── TimeTrendChart.vue
│   │   ├── router/            # 路由配置
│   │   │   └── index.js
│   │   ├── App.vue            # 主组件
│   │   └── main.js            # 入口文件
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
└── README.md                   # 项目说明文档
```

## 安装与运行

### 环境要求

- Python 3.9+
- Node.js 16+
- MySQL 8.0+

### 后端部署

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd openrank
   ```

2. **安装Python依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **配置数据库**
   ```bash
   # 复制配置文件示例
   cp config.example.py config.py
   
   # 编辑 config.py，填入你的数据库配置
   # 包括：host, user, password, db, port
   ```

4. **初始化数据库**
   ```bash
   # 登录MySQL并执行初始化脚本
   mysql -u your_username -p your_database_name < init_database.sql
   ```

5. **导入数据**
   
   参考 `backend/import_data.md` 文件中的说明，将CSV数据文件导入到数据库：
   - `pr_prediction_results.csv` → `pr_prediction_results` 表
   - `top_pre.csv` → `top_pre` 表

6. **启动后端服务**
   ```bash
   python app.py
   ```
   后端服务将在 `http://localhost:5000` 启动

### 前端部署

1. **进入前端目录**
   ```bash
   cd web
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```
   前端服务将在 `http://localhost:8080` 启动

4. **构建生产版本**
   ```bash
   npm run build
   ```
   构建文件将输出到 `dist/` 目录


## 数据文件

项目包含两个CSV数据文件，位于 `backend/` 目录：

- **pr_prediction_results.csv** - PR预测结果数据，需要导入到 `pr_prediction_results` 表
- **top_pre.csv** - PR关联的仓库日志数据，需要导入到 `top_pre` 表

详细的数据导入方法请参考 `backend/import_data.md` 文件。

## 配置说明

### 后端配置

编辑 `backend/config.py`（从 `config.example.py` 复制）：

```python
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "your_username",
    "password": "your_password",
    "db": "your_database",
    "port": 3306,
    "charset": "utf8mb4"
}

FLASK_CONFIG = {
    "DEBUG": True,
    "JSON_AS_ASCII": False  # 支持中文
}
```

### 前端配置

如需修改后端API地址，编辑 `web/vite.config.js`：

```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:5000',  // 修改为你的后端地址
    changeOrigin: true,
    rewrite: (path) => path
  }
}
```

## 注意事项

**端口**：
   - 默认后端端口：5000
   - 默认前端端口：8080
   - 可在配置文件中修改


## 文件说明

### 需要提交到GitHub的文件

**后端：**
- ✅ `app.py` - 主应用文件
- ✅ `model.py` - 模型文件（如果使用）
- ✅ `config.example.py` - 配置示例
- ✅ `requirements.txt` - Python依赖
- ✅ `init_database.sql` - 数据库初始化脚本
- ✅ `import_data.md` - 数据导入说明
- ✅ `README.md` - 后端说明文档
- ✅ `pr_prediction_results.csv` - 数据文件（如果文件不大）
- ✅ `top_pre.csv` - 数据文件（如果文件不大）

**前端：**
- ✅ `src/` - 所有源代码
- ✅ `index.html` - 入口HTML
- ✅ `package.json` - 依赖配置
- ✅ `vite.config.js` - Vite配置
- ✅ `README.md` - 前端说明文档

