-- PR合并风险预测系统数据库初始化脚本

-- 1. 创建PR预测结果表
CREATE TABLE IF NOT EXISTS `pr_prediction_results` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `pr_id` bigint DEFAULT NULL COMMENT 'PR ID',
  `repo_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属仓库名称',
  `actor_login` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '提交者登录名',
  `pull_additions` int DEFAULT NULL COMMENT '代码新增量',
  `pull_changed_files` int DEFAULT NULL COMMENT '修改文件数',
  `risk_label` tinyint DEFAULT NULL COMMENT '风险标签（0=低风险，1=高风险）',
  `low_risk_prob` float DEFAULT NULL COMMENT '低风险概率',
  `high_risk_prob` float DEFAULT NULL COMMENT '高风险概率',
  `predict_hours` float DEFAULT NULL COMMENT '预计处理时长（小时）',
  `risk_reason` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '风险归因原因',
  `merge_status` tinyint DEFAULT '0' COMMENT '合并状态（0=未合并，1=已合并）',
  `created_at` datetime DEFAULT NULL COMMENT 'PR提交时间',
  PRIMARY KEY (`id`),
  KEY `idx_pr_id` (`pr_id`),
  KEY `idx_repo_name` (`repo_name`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='PR合并风险预测结果表';

-- 2. 创建PR关联的仓库日志表
CREATE TABLE IF NOT EXISTS `top_pre` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `issue_id` bigint DEFAULT NULL COMMENT '关联pr_prediction_results的pr_id',
  `actor_id` bigint DEFAULT NULL COMMENT '用户ID',
  `actor_login` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户名',
  `repo_id` bigint DEFAULT NULL COMMENT '仓库ID',
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '事件类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2048 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='PR关联的仓库日志表';

