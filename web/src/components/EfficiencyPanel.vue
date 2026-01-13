<template>
  <div class="efficiency-panel">
    <div class="section-title">仓库效率排行</div>
    <div class="efficiency-list">
      <div 
        v-for="(repo, index) in repoEfficiency" 
        :key="repo.repo_name"
        class="repo-item"
      >
        <div class="repo-rank">{{ index + 1 }}</div>
        <div class="repo-info">
          <div class="repo-name">{{ repo.repo_name }}</div>
          <div class="repo-hours">平均处理时长: {{ repo.avg_hours ? repo.avg_hours.toFixed(2) : '0' }} 小时</div>
        </div>
      </div>
      <div v-if="!repoEfficiency || repoEfficiency.length === 0" class="empty-tip">
        暂无数据
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EfficiencyPanel',
  props: {
    repoEfficiency: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.efficiency-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 212, 255, 0.3);
}

.efficiency-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 5px;
}

.repo-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 6px;
  transition: all 0.3s;
}

.repo-item:hover {
  background: rgba(0, 212, 255, 0.2);
  border-color: rgba(0, 212, 255, 0.5);
}

.repo-rank {
  font-size: 24px;
  font-weight: bold;
  color: #00d4ff;
  margin-right: 15px;
  min-width: 40px;
  text-align: center;
}

.repo-info {
  flex: 1;
}

.repo-name {
  font-weight: bold;
  margin-bottom: 5px;
  color: #fff;
}

.repo-hours {
  font-size: 12px;
  color: #aaa;
}

.empty-tip {
  text-align: center;
  color: #666;
  padding: 20px;
}

/* 自定义滚动条样式 - 与整体风格一致 */
.efficiency-list::-webkit-scrollbar {
  width: 8px;
}

.efficiency-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.efficiency-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.6), rgba(0, 150, 255, 0.6));
  border-radius: 4px;
  border: 1px solid rgba(0, 212, 255, 0.3);
}

.efficiency-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.8), rgba(0, 150, 255, 0.8));
}
</style>

