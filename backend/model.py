import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from config import MODEL_PATH
import pandas as pd
import numpy as np

# 设备配置
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 定义SLSTM单元
class SLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(SLSTMCell, self).__init__()
        self.s_gate = nn.Linear(input_size + hidden_size, 1)
        self.i2h = nn.Linear(input_size, 4 * hidden_size)
        self.h2h = nn.Linear(hidden_size, 4 * hidden_size)

    def forward(self, input, hidden):
        h, c = hidden
        combined = torch.cat((input, h), 1)
        s = torch.sigmoid(self.s_gate(combined))
        gates = self.i2h(input) + self.h2h(h)
        i, f, o, g = gates.chunk(4, 1)
        i = s * torch.sigmoid(i)
        f = s * torch.sigmoid(f)
        o = s * torch.sigmoid(o)
        g = torch.tanh(g)
        c = f * c + i * g
        h = o * torch.tanh(c)
        return h, c

# 定义GCN-LSTM-SLSTM模型
class GCN_LSTM_SLSTM(nn.Module):
    def __init__(self, gcn_input_dim, lstm_input_dim, hidden_dim=64, lstm_layers=3):
        super(GCN_LSTM_SLSTM, self).__init__()
        self.gcn_layers = nn.ModuleList()
        self.gcn_layers.append(GCNConv(gcn_input_dim, hidden_dim))
        self.gcn_layers.append(GCNConv(hidden_dim, hidden_dim))  # 2层GCN
        self.lstm = nn.LSTM(lstm_input_dim, 128, lstm_layers, batch_first=True)
        self.slstm_cell = SLSTMCell(hidden_dim + 128, hidden_dim)
        self.risk_head = nn.Linear(hidden_dim, 2)
        self.time_head = nn.Linear(hidden_dim, 1)

    def forward(self, data, time_series, pr_idx):
        x, edge_index = data.x, data.edge_index
        for gcn in self.gcn_layers:
            x = gcn(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=0.2, training=self.training)
        gcn_features = x[pr_idx:pr_idx + 1, :]
        lstm_out, (hn, cn) = self.lstm(time_series.unsqueeze(0))
        lstm_features = hn[-1]
        fusion_features = torch.cat((gcn_features, lstm_features), dim=1)
        slstm_h = torch.zeros_like(fusion_features[:, :64])
        slstm_c = torch.zeros_like(fusion_features[:, :64])
        slstm_h, slstm_c = self.slstm_cell(fusion_features, (slstm_h, slstm_c))
        risk_logits = self.risk_head(slstm_h)
        process_hours = self.time_head(slstm_h).squeeze()
        return risk_logits, process_hours

# 加载训练好的模型
def load_model(gcn_input_dim=4, lstm_input_dim=10):
    model = GCN_LSTM_SLSTM(gcn_input_dim, lstm_input_dim).to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()  # 预测模式
    return model

# 预测单个PR的风险与处理时长
def predict_pr(model, data, pr_idx, time_series):
    with torch.no_grad():
        risk_logits, pred_hours = model(data.to(DEVICE), time_series.unsqueeze(0).to(DEVICE), pr_idx)
        risk_pred = torch.argmax(risk_logits, dim=1).cpu().numpy()[0]
        risk_prob = torch.softmax(risk_logits, dim=1).cpu().numpy()[0]
    return {
        "risk_label": int(risk_pred),
        "risk_label_name": "高风险" if risk_pred == 1 else "低风险",
        "low_risk_prob": round(float(risk_prob[0]), 4),
        "high_risk_prob": round(float(risk_prob[1]), 4),
        "predict_hours": round(float(pred_hours.cpu().numpy()), 2)
    }
