<template>
  <div class="time-trend-chart">
    <div class="section-title">PR风险趋势</div>
    <div ref="riskChartRef" class="chart-container"></div>
    
    <div class="section-title" style="margin-top: 30px;">PR效率趋势</div>
    <div ref="efficiencyChartRef" class="chart-container"></div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'TimeTrendChart',
  props: {
    riskTrend: {
      type: Array,
      default: () => []
    },
    efficiencyTrend: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const riskChartRef = ref(null)
    const efficiencyChartRef = ref(null)
    let riskChart = null
    let efficiencyChart = null

    // 将日期格式化为 YYYY.MM.DD 格式
    const formatDateLabel = (value) => {
      if (!value) return ''
      try {
        let dateStr = String(value)
        
        // 处理 GMT 格式：Fri,30 Oct 2020 00:00:00 GMT
        if (dateStr.includes('GMT') || dateStr.includes(',')) {
          const date = new Date(dateStr)
          if (!isNaN(date.getTime())) {
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            return `${year}.${month}.${day}`
          }
        }
        
        // 处理 YYYY-MM-DD 格式
        const datePart = dateStr.split(' ')[0]  // 取日期部分，去掉时间
        const [y, m, d] = datePart.split('-')
        if (y && m && d) {
          const year = parseInt(y, 10)
          const month = String(parseInt(m, 10)).padStart(2, '0')
          const day = String(parseInt(d, 10)).padStart(2, '0')
          return `${year}.${month}.${day}`
        }
        
        return dateStr
      } catch (e) {
        return String(value)
      }
    }
    
    const initCharts = () => {
      nextTick(() => {
        if (riskChartRef.value && !riskChart) {
          riskChart = echarts.init(riskChartRef.value)
        }
        if (efficiencyChartRef.value && !efficiencyChart) {
          efficiencyChart = echarts.init(efficiencyChartRef.value)
        }
        updateCharts()
      })
    }
    
    const updateCharts = () => {
      // 更新风险趋势图
      if (riskChart && props.riskTrend) {
        const dates = props.riskTrend.map(item => formatDateLabel(item.date))
        const highRiskCounts = props.riskTrend.map(item => item.high_risk_count || 0)
        const totalCounts = props.riskTrend.map(item => item.total_count || 0)
        
        riskChart.setOption({
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['高风险PR', '总PR数'],
            textStyle: { color: '#fff' }
          },
          xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
              color: '#aaa',
              formatter: (value) => value  // 确保使用格式化后的中文日期
            },
            axisLine: { lineStyle: { color: '#00d4ff' } }
          },
          yAxis: {
            type: 'value',
            axisLabel: { color: '#aaa' },
            axisLine: { lineStyle: { color: '#00d4ff' } }
          },
          series: [
            {
              name: '高风险PR',
              type: 'line',
              data: highRiskCounts,
              itemStyle: { color: '#ff6b6b' },
              areaStyle: { color: 'rgba(255, 107, 107, 0.2)' }
            },
            {
              name: '总PR数',
              type: 'line',
              data: totalCounts,
              itemStyle: { color: '#00d4ff' },
              areaStyle: { color: 'rgba(0, 212, 255, 0.2)' }
            }
          ],
          backgroundColor: 'transparent'
        })
      }
      
      // 更新效率趋势图
      if (efficiencyChart && props.efficiencyTrend) {
        const dates = props.efficiencyTrend.map(item => formatDateLabel(item.date))
        const avgHours = props.efficiencyTrend.map(item => item.avg_hours || 0)
        
        efficiencyChart.setOption({
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
              color: '#aaa',
              formatter: (value) => value  // 确保使用格式化后的中文日期
            },
            axisLine: { lineStyle: { color: '#00d4ff' } }
          },
          yAxis: {
            type: 'value',
            name: '小时',
            axisLabel: { color: '#aaa' },
            axisLine: { lineStyle: { color: '#00d4ff' } }
          },
          series: [
            {
              name: '平均处理时长',
              type: 'bar',
              data: avgHours,
              itemStyle: { color: '#00d4ff' }
            }
          ],
          backgroundColor: 'transparent'
        })
      }
    }
    
    watch(() => [props.riskTrend, props.efficiencyTrend], () => {
      updateCharts()
    }, { deep: true })
    
    onMounted(() => {
      initCharts()
      window.addEventListener('resize', () => {
        riskChart?.resize()
        efficiencyChart?.resize()
      })
    })
    
    return {
      riskChartRef,
      efficiencyChartRef
    }
  }
}
</script>

<style scoped>
.time-trend-chart {
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

.chart-container {
  width: 100%;
  height: 300px;
  min-height: 300px;
}
</style>

