# 医院睡眠障碍（失眠）患者数据机器学习分析

> 真实临床数据驱动的端到端数据科学项目：从 PsychoPy 实验原始日志，到失眠（二分类）预测模型与 SHAP 可解释性分析。
>
> End-to-end ML pipeline on real hospital insomnia data: raw PsychoPy logs → feature engineering → classification (Logistic / Random Forest / XGBoost) → SHAP explainability.

---

## 项目背景 / Background

医院睡眠障碍门诊被试的行为实验数据（视听双通道注意任务 A/V/AV 三种条件）、医生填写的临床信息（性别 / 年龄 / 病史 / 用药）、PSQI / SAS / SDS 睡眠与情绪问卷数据，目标是根据行为表现与临床指标预测被试是否失眠（PSQI 总分 ≥ 9），并给出可解释的特征归因。

## 数据流 / Pipeline

```
PsychoPy 原始 CSV（按创建时间排序，正则提取）
        │  ① 整合医院被试原始数据.py
        ▼
原始数据 Excel（每个被试一个 sheet，缺失反应时均值填补）
        │  ② 形成新的excel总结文件.py
        ▼
汇总统计 Excel（按 A / V / AV 条件聚合 反应时 & 正确率）
        │  ③ 统计其他信息.py  （按姓名左连接 医生临床表）
        ▼
医生数据汇总 Excel
        │  ④ 问卷数据录入.py   （PSQI 手动录入，断点续录 + 自动备份）
        ▼
数据最终汇总 Excel
        │  ⑤ 数据预处理(新).py （剔除正确率<0.8被试、总分二分类、性别0/1编码）
        ▼
已预处理的数据.csv
        │
        ├── ⑥ 逻辑回归分析.py   （系数/OR/95%CI、VIF、StratifiedKFold ROC）
        ├── ⑦ 随机森林分析.py   （GridSearchCV + SHAP）
        └── ⑧ xgboost.py        （XGBoost + SHAP 概率空间解释）
```

## 文件说明 / Files

| 脚本 | 作用 |
| --- | --- |
| `1.整合医院被试原始数据.py` | 正则提取 + 按创建时间排序，将两次实验合并为 96 试次原始数据，均值填补缺失反应时 |
| `2.形成新的excel总结文件.py` | 按条件分组聚合，输出 反应时 / 正确率 / 汇总 三个 sheet |
| `3.统计其他信息.py` | 将医生填写的临床信息表按姓名 merge 进实验数据 |
| `4.问卷数据录入.py` | PSQI 问卷录入（断点续录、自动备份、防止重复录入） |
| `5.数据预处理(新).py` | 剔除正确率 < 0.8 的被试、PSQI 总分二分类、性别 0/1 编码、输出建模数据 |
| `6.逻辑回归分析.py` | 逻辑回归 + 标准化/OneHot 特征工程 + statsmodels 统计推断（p 值、OR、95%CI）+ VIF + 分层 K 折 ROC |
| `7.随机森林分析.py` | 随机森林（GridSearchCV 调参）+ SHAP 蜂群图/依赖图/单样本瀑布图 |
| `8.xgboost.py` | XGBoost + SHAP（概率空间 interventional 模式）全局与单样本解释 |
| `计分.py` | PSQI 量表 A–G 七部分计分规则实现（供录入脚本调用） |

## 技术栈 / Tech Stack

- **数据处理**：Python · Pandas / NumPy · openpyxl
- **机器学习**：Scikit-learn（LogisticRegression / RandomForest / ColumnTransformer / GridSearchCV / StratifiedKFold）
- **可解释性**：SHAP（TreeExplainer：summary / dependence / waterfall plot）
- **统计推断**：Statsmodels（Logit：系数显著性、OR 与 95% 置信区间）、VIF 多重共线性检验
- **可视化**：Matplotlib / Seaborn

## 核心方法亮点 / Highlights

1. **端到端数据工程**：PsychoPy 原始日志 → 清洗 → 多源合并（实验 + 临床 + 问卷）→ 建模数据，全流程自动化脚本。
2. **统计严谨性 + 机器学习结合**：不仅报告模型准确率 / ROC-AUC，还输出 OR、95% CI、p 值、VIF，符合医学研究规范（心理学背景的差异化优势）。
3. **模型可解释性**：用 SHAP 做全局归因（蜂群图）与单样本级解释（瀑布图），将"黑盒"预测还原为临床可读的特征贡献。
4. **三模型对比**：逻辑回归（基线、可解释）vs 随机森林 vs XGBoost，同一数据、同一评估协议。

## 运行说明 / Quick Start

```bash
pip install -r requirements.txt
# 脚本内 data 路径为医院内网环境，运行前请将 1~5 步的 os.chdir 路径改为本地数据目录
python "1.整合医院被试原始数据.py"
python "2.形成新的excel总结文件.py"
python "3.统计其他信息.py"
python "4.问卷数据录入.py"     # 交互式录入 PSQI
python "5.数据预处理(新).py"
python "6.逻辑回归分析.py"
python "7.随机森林分析.py"
python "8.xgboost.py"
```

> 注意：医院数据涉及患者隐私，仓库中不含原始数据与临床信息表；脚本中均为**硬编码内网路径**。

## 目录结构

```
hospital_statistics/
├── 1.整合医院被试原始数据.py
├── 2.形成新的excel总结文件.py
├── 3.统计其他信息.py
├── 4.问卷数据录入.py
├── 5.数据预处理(新).py
├── 6.逻辑回归分析.py
├── 7.随机森林分析.py
├── 8.xgboost.py
├── 计分.py
├── requirements.txt
└── README.md
```

## License
