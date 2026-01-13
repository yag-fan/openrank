<template>
  <div class="risk-board">
    <div class="section-title">风险统计</div>
    <div class="risk-distribution">
      <div class="risk-item low-risk">
        <div class="risk-label">低风险</div>
        <div class="risk-count">{{ riskDistribution["低风险"] || 0 }}</div>
      </div>
      <div class="risk-item high-risk">
        <div class="risk-label">高风险</div>
        <div class="risk-count">{{ riskDistribution["高风险"] || 0 }}</div>
      </div>
    </div>
    
    <div class="section-title">待处理PR</div>
    <div class="pending-count">{{ pendingCount || 0 }}</div>
    
    <div class="section-title-with-tabs">
      <div class="tabs">
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'top10' }"
          @click="activeTab = 'top10'"
        >
          Top10 高风险PR
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'random' }"
          @click="activeTab = 'random'"
        >
          PR风险概率
        </div>
      </div>
    </div>
    <div class="high-risk-list">
      <div 
        v-for="pr in currentPrList" 
        :key="pr.pr_id"
        class="pr-item"
        @click="$emit('pr-click', pr.pr_id)"
      >
        <div class="pr-id">PR_id {{ pr.pr_id }}</div>
        <div class="pr-repo">{{ pr.repo_name }}</div>
        <div class="pr-risk">风险概率: {{ (pr.high_risk_prob * 100).toFixed(1) }}%</div>
      </div>
      <div v-if="!currentPrList || currentPrList.length === 0" class="empty-tip">
        暂无数据
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'RiskBoard',
  props: {
    riskDistribution: {
      type: Object,
      default: () => ({ "低风险": 0, "高风险": 0 })
    },
    topHighRiskPr: {
      type: Array,
      default: () => []
    },
    randomPrByRisk: {
      type: Array,
      default: () => []
    },
    pendingCount: {
      type: Number,
      default: 0
    }
  },
  emits: ['pr-click'],
  setup(props) {
    const activeTab = ref('top10')
    
    const currentPrList = computed(() => {
      return activeTab.value === 'top10' ? props.topHighRiskPr : props.randomPrByRisk
    })
    
    return {
      activeTab,
      currentPrList
    }
  }
}
</script>

<style scoped>
.risk-board {
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

.risk-distribution {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.risk-item {
  flex: 1;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid;
}

.risk-item.low-risk {
  background: rgba(0, 255, 0, 0.1);
  border-color: rgba(0, 255, 0, 0.3);
}

.risk-item.high-risk {
  background: rgba(255, 0, 0, 0.1);
  border-color: rgba(255, 0, 0, 0.3);
}

.risk-label {
  font-size: 14px;
  margin-bottom: 10px;
  opacity: 0.8;
}

.risk-count {
  font-size: 32px;
  font-weight: bold;
}

.pending-count {
  font-size: 48px;
  font-weight: bold;
  color: #ffaa00;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
}

.section-title-with-tabs {
  margin-bottom: 15px;
}

.tabs {
  display: flex;
  gap: 10px;
  border-bottom: 1px solid rgba(0, 212, 255, 0.3);
}

.tab-item {
  padding: 10px 15px;
  cursor: pointer;
  color: #aaa;
  font-size: 14px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
  margin-bottom: -1px;
}

.tab-item:hover {
  color: #00d4ff;
}

.tab-item.active {
  color: #00d4ff;
  font-weight: bold;
  border-bottom-color: #00d4ff;
}

.high-risk-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 5px;
}

.pr-item {
  padding: 15px;
  margin-bottom: 10px;
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.pr-item:hover {
  background: rgba(255, 0, 0, 0.2);
  border-color: rgba(255, 0, 0, 0.5);
  transform: translateX(5px);
}

.pr-id {
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 5px;
}

.pr-repo {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 5px;
}

.pr-risk {
  font-size: 14px;
  color: #ff6b6b;
}

.empty-tip {
  text-align: center;
  color: #666;
  padding: 20px;
}

/* 自定义滚动条样式 - 与整体风格一致 */
.high-risk-list::-webkit-scrollbar {
  width: 8px;
}

.high-risk-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.high-risk-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.6), rgba(0, 150, 255, 0.6));
  border-radius: 4px;
  border: 1px solid rgba(0, 212, 255, 0.3);
}

.high-risk-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.8), rgba(0, 150, 255, 0.8));
}
</style>

