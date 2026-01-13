# 前端应用

Vue 3 + Vite 构建的前端可视化大屏应用。

## 快速开始

1. 安装依赖
   ```bash
   npm install
   ```

2. 启动开发服务器
   ```bash
   npm run dev
   ```

3. 构建生产版本
   ```bash
   npm run build
   ```

## 技术栈

- Vue 3 - 渐进式JavaScript框架
- Vite - 下一代前端构建工具
- ECharts - 数据可视化图表库
- Axios - HTTP客户端

## 项目结构

```
src/
├── api/              # API接口封装
├── components/       # Vue组件
│   ├── RiskBoard.vue           # 风险统计面板
│   ├── EfficiencyPanel.vue     # 效率排行面板
│   ├── TimeTrendChart.vue      # 时序趋势图表
│   └── PrDetailModal.vue       # PR详情弹窗
├── router/           # 路由配置
├── App.vue           # 根组件
└── main.js           # 入口文件
```

## 开发说明

- 组件采用 Composition API
- 使用 ECharts 进行数据可视化
- 支持响应式布局
- 自定义滚动条样式

