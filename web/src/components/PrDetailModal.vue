<template>
  <div v-if="visible" class="modal-overlay" @click="handleClose">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>PR_id详情 {{ prId }}</h2>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="prDetail" class="modal-body">
        <div class="detail-section">
          <h3>基本信息</h3>
          <div class="detail-item">
            <span class="label">仓库名称:</span>
            <span class="value">{{ prDetail.repo_name || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">提交者:</span>
            <span class="value">{{ prDetail.actor_login || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">新增代码行数:</span>
            <span class="value">{{ prDetail.pull_additions || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="label">修改文件数:</span>
            <span class="value">{{ prDetail.pull_changed_files || 0 }}</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>风险预测</h3>
          <div class="detail-item">
            <span class="label">高风险概率:</span>
            <span class="value risk-value">{{ prDetail.high_risk_prob ? (prDetail.high_risk_prob * 100).toFixed(2) + '%' : '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">预计处理时长:</span>
            <span class="value">{{ prDetail.predict_hours ? prDetail.predict_hours.toFixed(2) + ' 小时' : '-' }}</span>
          </div>
          <div v-if="prDetail.risk_reason" class="detail-item">
            <span class="label">风险原因:</span>
            <span class="value">{{ prDetail.risk_reason }}</span>
          </div>
        </div>
        
        <div v-if="relatedNodes" class="detail-section">
          <h3>关联信息</h3>
          <div class="detail-item">
            <span class="label">贡献者ID:</span>
            <span class="value">{{ relatedNodes.actor_id || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">贡献者名称:</span>
            <span class="value">{{ relatedNodes.actor_name || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">仓库ID:</span>
            <span class="value">{{ relatedNodes.repo_id || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">事件类型:</span>
            <span class="value">{{ relatedNodes.event_type || '-' }}</span>
          </div>
        </div>
      </div>
      
      <div v-else class="error">加载失败，请稍后重试</div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { getPrDetail } from '../api/screenApi'

export default {
  name: 'PrDetailModal',
  props: {
    prId: {
      type: Number,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const prDetail = ref(null)
    const relatedNodes = ref(null)
    const loading = ref(false)
    
    const loadPrDetail = async () => {
      if (!props.prId || !props.visible) return
      
      loading.value = true
      try {
        const response = await getPrDetail(props.prId)
        if (response.data.code === 200) {
          prDetail.value = response.data.data.pr_detail
          relatedNodes.value = response.data.data.related_nodes
        }
      } catch (error) {
        console.error('加载PR详情失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleClose = () => {
      emit('close')
    }
    
    watch(() => [props.prId, props.visible], () => {
      if (props.visible && props.prId) {
        loadPrDetail()
      }
    }, { immediate: true })
    
    return {
      prDetail,
      relatedNodes,
      loading,
      handleClose
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #1a1f3a;
  border: 2px solid #00d4ff;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 212, 255, 0.3);
}

.modal-header h2 {
  color: #00d4ff;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 32px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  color: #ff6b6b;
}

.modal-body {
  padding: 20px;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  color: #00d4ff;
  margin-bottom: 15px;
  font-size: 16px;
}

.detail-item {
  display: flex;
  margin-bottom: 10px;
  padding: 10px;
  background: rgba(0, 212, 255, 0.05);
  border-radius: 5px;
}

.label {
  font-weight: bold;
  color: #aaa;
  min-width: 120px;
}

.value {
  color: #fff;
  flex: 1;
}

.risk-value {
  color: #ff6b6b;
  font-weight: bold;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  color: #aaa;
}

.error {
  color: #ff6b6b;
}
</style>

