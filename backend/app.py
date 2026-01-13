from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from config import FLASK_CONFIG, DB_CONFIG

# 初始化Flask应用
app = Flask(__name__)
app.config.update(FLASK_CONFIG)
CORS(app)  # 解决跨域问题

# 数据库连接函数
def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")
        raise

# 1. 接口1：获取大屏核心数据（风险统计、效率统计、Top10高风险PR）
@app.route("/api/screen/core-data", methods=["GET"])
def get_core_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 1. 风险统计（全量PR风险分布）
        cursor.execute("""
            SELECT risk_label, COUNT(*) as count 
            FROM pr_prediction_results  
            GROUP BY risk_label
        """)
        risk_stats = cursor.fetchall()
        risk_distribution = {
            "低风险": 0,
            "高风险": 1
        }
        for item in risk_stats:
            label_name = "高风险" if item["risk_label"] == 1 else "低风险"
            risk_distribution[label_name] = item["count"]

        # 2. 效率统计（按仓库维度的平均处理时长）
        cursor.execute("""
            SELECT repo_name, AVG(predict_hours) as avg_hours 
            FROM pr_prediction_results 
            GROUP BY repo_name 
            ORDER BY avg_hours ASC 
            LIMIT 10
        """)
        repo_efficiency = cursor.fetchall()

        # 3. Top10高风险PR
        cursor.execute("""
            SELECT pr_id, repo_name, actor_login, high_risk_prob, predict_hours 
            FROM pr_prediction_results 
            WHERE risk_label = 1 
            ORDER BY high_risk_prob DESC 
            LIMIT 10
        """)
        top_high_risk_pr = cursor.fetchall()

        # 4. PR风险概率：随机选择10条PR
        cursor.execute("""
            SELECT pr_id, repo_name, actor_login, high_risk_prob, predict_hours 
            FROM pr_prediction_results 
            ORDER BY RAND() 
            LIMIT 10
        """)
        random_pr_by_risk = cursor.fetchall()

        # 5. 实时待处理PR数量
        cursor.execute("""
            SELECT COUNT(*) as pending_count 
            FROM pr_prediction_results 
            WHERE merge_status = 0  -- 0=未合并，1=已合并
        """)
        pending_count = cursor.fetchone()["pending_count"]

        conn.close()

        # 构造返回数据
        resp = {
            "code": 200,
            "message": "success",
            "data": {
                "risk_distribution": risk_distribution,
                "repo_efficiency": repo_efficiency,
                "top_high_risk_pr": top_high_risk_pr,
                "random_pr_by_risk": random_pr_by_risk,
                "pending_count": pending_count
            }
        }
        return jsonify(resp)
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取数据失败：{str(e)}",
            "data": None
        })

# 2. 接口2：获取单个PR的风险归因详情
@app.route("/api/screen/pr-detail/<int:pr_id>", methods=["GET"])
def get_pr_detail(pr_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 查询PR详情（基础信息+风险归因）
        cursor.execute("""
            SELECT 
                p.pr_id, p.repo_name, p.actor_login, p.pull_additions, 
                p.pull_changed_files, p.high_risk_prob, p.predict_hours,
                p.risk_reason  -- 风险归因原因（如"修改核心模块+非OWNER提交"）
            FROM pr_prediction_results p
            WHERE p.pr_id = %s
        """, (pr_id,))
        pr_detail = cursor.fetchone()

        # 查询该PR的关联节点（贡献者、仓库模块）
        cursor.execute("""
            SELECT 
                actor_id, 
                actor_login as actor_name,
                repo_id,
                type as event_type
            FROM top_pre 
            WHERE issue_id = %s  -- issue_id即pr_id
            LIMIT 1
        """, (pr_id,))
        related_nodes = cursor.fetchone()

        conn.close()

        return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "pr_detail": pr_detail,
                "related_nodes": related_nodes
            }
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取PR详情失败：{str(e)}",
            "data": None
        })

# 3. 接口3：获取时序趋势数据（近7天PR风险趋势、效率趋势）
@app.route("/api/screen/time-trend", methods=["GET"])
def get_time_trend():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 数据只抽样了部分历史记录，日期并不连续， 因此这里取最近的7个有数据的日期
        # 1）按日期组合，按日期倒序取最近 7 个有数据的日期，再按日期正序返回
        cursor.execute("""
            SELECT *
            FROM (
                SELECT 
                    DATE(created_at) AS date,
                    SUM(CASE WHEN risk_label = 1 THEN 1 ELSE 0 END) AS high_risk_count,
                    COUNT(*) AS total_count
                FROM pr_prediction_results
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at) DESC
                LIMIT 7
            ) AS t
            ORDER BY t.date ASC
        """)
        risk_trend = cursor.fetchall()

        # 2）处理效率趋势：同样按日期组合，取最近 7 个有数据的日期
        cursor.execute("""
            SELECT *
            FROM (
                SELECT 
                    DATE(created_at) AS date,
                    AVG(predict_hours) AS avg_hours
                FROM pr_prediction_results
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at) DESC
                LIMIT 7
            ) AS t
            ORDER BY t.date ASC
        """)
        efficiency_trend = cursor.fetchall()

        conn.close()

        return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "risk_trend": risk_trend,
                "efficiency_trend": efficiency_trend
            }
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"获取时序趋势数据失败：{str(e)}",
            "data": None
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
