# Vanguard A/B Test – Digital Process Redesign

> Ironhack Data Analytics Bootcamp – Project 2 (Weeks 5–6)
> **Team:** Juliana Therezo · Raquel Marques · Lervin

## 📌 Project overview

Vanguard's Customer Experience (CX) team ran an A/B test from **15 Mar 2017 to 20 Jun 2017** to find out whether a more modern UI with in-context prompts helps more clients complete an online process
(`start → step_1 → step_2 → step_3 → confirm`).

- **Control group:** traditional online process
- **Test group:** new, redesigned digital interface

**Main question:** Did the new design lead to a higher completion rate, and is the increase large enough (≥ 5 %) to justify its cost?

## 🔗 Links

| What | Link |
|---|---|
| Kanban board (Trello) | https://trello.com/b/jXS0m9Dt/vanguard-a-b-test-project-2-juliana-raquel-lervin |
| Data sources (folder) | https://github.com/data-bootcamp-v4/lessons/tree/main/5_6_eda_inf_stats_tableau/project/files_for_project |
| Tableau Public dashboard | _TBD_ |
| Presentation slides | _TBD_ |

## 📂 Data sources

| # | Dataset | File | Description | Cleaning owner |
|---|---|---|---|---|
| 1 | Client Profiles | [df_final_demo.txt](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_demo.txt) | Demographics: age, gender, tenure, accounts, balance, calls, logons | Lervin |
| 2 | Digital Footprints | [df_final_web_data_pt_1.txt](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_1.txt) + [df_final_web_data_pt_2.txt](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_2.txt) | Every web interaction (visitor, visit, step, timestamp) | Raquel |
| 3 | Experiment Roster | [df_final_experiment_clients.txt](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_experiment_clients.txt) | Which clients were in the Test or Control group | Juliana |

## 🗂️ Repository structure

```
vanguard-ab-test/
├── data/
│   ├── raw/            # original files (not committed)
│   └── clean/          # cleaned outputs (not committed)
├── notebooks/
│   ├── Data cleaning 1.ipynb   # Client Profiles – Lervin
│   ├── Data cleaning 2.ipynb   # Digital Footprints – Raquel
│   └── Data cleaning 3.ipynb   # Experiment Roster – Juliana
├── src/
│   └── cleaning.py     # reusable cleaning functions
├── figures/            # charts exported from notebooks
├── tableau/            # Tableau workbook (.twbx)
├── slides/             # presentation
├── requirements.txt
└── README.md
```

## ⚙️ How to run

```bash
pip install -r requirements.txt
```

Open the notebooks in VS Code or Jupyter and run them top to bottom. They read the data straight from the source links above and save copies to `data/raw/` and `data/clean/`.

## 🧹 Data cleaning

- **Data cleaning 1 – Client Profiles:** (Lervin)
## 🧹 Data Cleaning & Client Profile (`df_final_demo`)

- We audited and cleaned the master customer dataset (totaling **70,609** clients.

### 🎯 Core Persona Highlights
* **Age:** Median age of **47 years** (middle 50% between 32.5 and 59).
* **Tenure:** Highly loyal base with a median tenure of **11 years** with Vanguard.
* **Wealth:** Median account balance of **$63,333** (skewed up to an average of $147,445 by a $16.3M outlier).
* **Digital Habits:** Active users averaging **5.57 logins** and **3.38 service calls** over the last 6 months.

> **💡 Takeaway:** Vanguard's online traffic is driven by loyal, financially established, middle-aged clients with long-standing accounts.

- **Data cleaning 2 – Digital Footprints:** _TBD (Raquel)_
- **Data cleaning 3 – Experiment Roster:** 70,609 clients, with no duplicates or invalid IDs. 20,109 clients (28.5 %) have no group (`NA`), so they were not part of the experiment and are removed. That leaves **50,500 clients: 26,968 Test (53.4 %) and 23,532 Control (46.6 %)**. The column was renamed `Variation → variation` and stored as a category. Output: `data/clean/experiment_clients_clean.csv`.

## 🔍 EDA – Client behaviour

_TBD_

## 📊 KPIs

_TBD: completion rate, time spent on each step, error rate (backward steps)._

## 🧪 Hypothesis testing

_TBD_
1. Completion rate, Test vs Control (two-proportion z-test)
2. Completion rate with the 5 % cost-effectiveness threshold
3. Additional hypothesis (age / tenure / gender)

## 🧭 Experiment evaluation

_TBD: design effectiveness, randomisation, biases, duration, extra data needs._

## ✅ Conclusions & recommendations

_TBD_

## 👥 Team & project management

Tasks are split and tracked on our [Trello board](https://trello.com/b/jXS0m9Dt/vanguard-a-b-test-project-2-juliana-raquel-lervin).
