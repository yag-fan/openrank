<template>
  <div class="screen-container">
    <div class="screen-header">
      <h1>PR预测风险大屏</h1>
    </div>
    
    <div class="screen-content">
      <!-- 左侧：风险统计和Top10高风险PR -->
      <div class="left-panel">
        <RiskBoard 
          :risk-distribution="coreData.risk_distribution"
          :top-high-risk-pr="coreData.top_high_risk_pr"
          :random-pr-by-risk="coreData.random_pr_by_risk"
          :pending-count="coreData.pending_count"
          @pr-click="handlePrClick"
        />
      </div>
      
      <!-- 中间：时序趋势图表 -->
      <div class="center-panel">
        <TimeTrendChart 
          :risk-trend="timeTrend.risk_trend"
          :efficiency-trend="timeTrend.efficiency_trend"
        />
      </div>
      
      <!-- 右侧：效率统计 -->
      <div class="right-panel">
        <EfficiencyPanel :repo-efficiency="coreData.repo_efficiency" />
      </div>
    </div>
    
    <!-- PR详情弹窗 -->
    <PrDetailModal 
      v-if="selectedPrId"
      :pr-id="selectedPrId"
      :visible="showModal"
      @close="handleCloseModal"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import RiskBoard from './components/RiskBoard.vue'
import EfficiencyPanel from './components/EfficiencyPanel.vue'
import TimeTrendChart from './components/TimeTrendChart.vue'
import PrDetailModal from './components/PrDetailModal.vue'
import { getCoreData, getTimeTrend } from './api/screenApi'

export default {
  name: 'App',
  components: {
    RiskBoard,
    EfficiencyPanel,
    TimeTrendChart,
    PrDetailModal
  },
  setup() {
    const coreData = ref({
      risk_distribution: { "低风险": 0, "高风险": 0 },
      repo_efficiency: [],
      top_high_risk_pr: [],
      random_pr_by_risk: [],
      pending_count: 0
    })
    const coreDataLoading = ref(false)
    
    const timeTrend = ref({
      risk_trend: [],
      efficiency_trend: []
    })
    const timeTrendLoading = ref(false)
    
    const selectedPrId = ref(null)
    const showModal = ref(false)
    
    // 加载核心数据
    const loadCoreData = async () => {
      try {
        coreDataLoading.value = true
        const response = await getCoreData()
        console.log('[前端] 核心数据接口返回:', response.data)
        if (response.data.code === 200) {
          coreData.value = response.data.data
        } else {
          console.warn('[前端] 核心数据接口 code 非200:', response.data)
        }
      } catch (error) {
        console.error('加载核心数据失败:', error)
      } finally {
        coreDataLoading.value = false
      }
    }
    
    // 加载时序趋势数据
    const loadTimeTrend = async () => {
      try {
        timeTrendLoading.value = true
        const response = await getTimeTrend()
        console.log('[前端] 时序趋势接口返回:', response.data)
        if (response.data.code === 200) {
          timeTrend.value = response.data.data
        } else {
          console.warn('[前端] 时序趋势接口 code 非200:', response.data)
        }
      } catch (error) {
        console.error('加载时序趋势数据失败:', error)
      } finally {
        timeTrendLoading.value = false
      }
    }
    
    // 处理PR点击
    const handlePrClick = (prId) => {
      selectedPrId.value = prId
      showModal.value = true
    }
    
    // 关闭弹窗
    const handleCloseModal = () => {
      showModal.value = false
      selectedPrId.value = null
    }
    
    // 定时刷新数据
    onMounted(() => {
      loadCoreData()
      loadTimeTrend()
      
      // 每30秒刷新一次
      setInterval(() => {
        loadCoreData()
        loadTimeTrend()
      }, 30000)
    })
    
    return {
      coreData,
      timeTrend,
      coreDataLoading,
      timeTrendLoading,
      selectedPrId,
      showModal,
      handlePrClick,
      handleCloseModal
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  background: #0a0e27;
  color: #fff;
  overflow: hidden;
}

.screen-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
}

.screen-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 2px solid rgba(0, 150, 255, 0.3);
}

.screen-header h1 {
  font-size: 36px;
  font-weight: bold;
  background: linear-gradient(90deg, #00d4ff, #0099ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}

.screen-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.left-panel,
.center-panel,
.right-panel {
  background: rgba(15, 25, 45, 0.6);
  border-radius: 10px;
  border: 1px solid rgba(0, 150, 255, 0.2);
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
}

/* 自定义滚动条样式 - 与整体风格一致 */
.left-panel::-webkit-scrollbar,
.center-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar {
  width: 8px;
}

.left-panel::-webkit-scrollbar-track,
.center-panel::-webkit-scrollbar-track,
.right-panel::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.left-panel::-webkit-scrollbar-thumb,
.center-panel::-webkit-scrollbar-thumb,
.right-panel::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.6), rgba(0, 150, 255, 0.6));
  border-radius: 4px;
  border: 1px solid rgba(0, 212, 255, 0.3);
}

.left-panel::-webkit-scrollbar-thumb:hover,
.center-panel::-webkit-scrollbar-thumb:hover,
.right-panel::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(0, 212, 255, 0.8), rgba(0, 150, 255, 0.8));
}
</style>

