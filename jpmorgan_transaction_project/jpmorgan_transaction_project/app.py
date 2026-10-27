"""Local Streamlit dashboard for saved synthetic transaction experiments."""
import plotly.express as px
import streamlit as st
from dashboard_data import load_saved, filter_transactions, confusion_counts, load_robustness
from dashboard_evaluation import render_independent

st.set_page_config(page_title='Transaction Intelligence', page_icon='🏦', layout='wide')
st.markdown('<style>.block-container{padding-top:4rem} [data-testid="stMetric"]{background:rgba(100,150,220,.12);padding:16px;border-radius:12px} [data-testid="stMetricValue"]{font-size:1.3rem}</style>', unsafe_allow_html=True)
st.caption('BANKING ANALYTICS / PORTFOLIO LAB')
st.title('Transaction Intelligence')
st.warning('SYNTHETIC DATA ONLY · Anomaly alerts are unusual transactions for review, not verified fraud. Synthetic injection metrics do not establish real-world fraud detection quality.')
try:
    saved = load_saved()
except (OSError, ValueError, KeyError) as exc:
    st.error(f'Saved experiment files are missing or unreadable: {exc}')
    st.info('Restore the reviewed saved evidence files from the repository. Launching this viewer does not require regenerating historical experiments.')
    st.stop()

raw, cleaned = saved['raw'], saved['cleaned']
st.sidebar.header('Transaction filters')
st.sidebar.caption('Legacy explorer filters affect overview, customer analysis and ranking. Final independent evaluation always uses all 40 saved cases.')
categories = st.sidebar.multiselect('Merchant categories', sorted(cleaned.merchant_category.unique()), default=sorted(cleaned.merchant_category.unique()))
customer = st.sidebar.selectbox('Customer', ['All customers'] + [str(x) for x in sorted(cleaned.customer_id.unique())])
dates = st.sidebar.date_input('Date range', value=(cleaned.date.min().date(), cleaned.date.max().date()), min_value=cleaned.date.min().date(), max_value=cleaned.date.max().date())
amount_range = st.sidebar.slider('Amount range ($)', min_value=0.0, max_value=float(cleaned.amount.max()), value=(0.0, float(cleaned.amount.max())))
if len(dates) != 2:
    st.info('Select both a start and end date.')
    st.stop()
filtered = filter_transactions(cleaned, categories, customer, *dates, amount_range)
st.sidebar.caption(f'{len(filtered):,} of {len(cleaned):,} cleaned transactions selected')
independent, overview, quality, customers, ranking, evaluation, robustness = st.tabs(['Independent evaluation', 'Overview', 'Data quality', 'Customer spending', 'Anomaly ranking', 'Historical development evidence', 'Historical robustness'])

with independent:
    render_independent()

with overview:
    st.subheader('Transaction overview')
    st.caption('Saved Phase 1 synthetic dataset · date-only records · selected transaction filters apply')
    cols = st.columns(4)
    for col, label, value in zip(cols, ['Transactions', 'Total volume', 'Customers', 'Median amount'],
        [f'{len(filtered):,}', f'${filtered.amount.sum():,.2f}', f'{filtered.customer_id.nunique():,}', f'${filtered.amount.median():,.2f}' if len(filtered) else '—']):
        col.metric(label, value)
    if filtered.empty:
        st.info('No transactions match the filters. Widen the range or select a category.')
    else:
        daily = filtered.groupby('date', as_index=False).amount.sum()
        st.plotly_chart(px.line(daily, x='date', y='amount', markers=True, title='Daily transaction volume', labels={'amount': 'Volume ($)', 'date': 'Date'}), key='daily')
        left, right = st.columns(2)
        left.plotly_chart(px.histogram(filtered, x='amount', nbins=35, title='Transaction amount distribution', labels={'amount': 'Amount ($)'}), key='hist')
        grouped = filtered.groupby('merchant_category', as_index=False).amount.sum()
        right.plotly_chart(px.bar(grouped, x='merchant_category', y='amount', title='Volume by merchant category', labels={'merchant_category': 'Category', 'amount': 'Volume ($)'}), key='category')
    st.dataframe(filtered, hide_index=True)
    st.download_button('Download filtered transactions', filtered.to_csv(index=False).encode(), 'filtered_synthetic_transactions.csv', 'text/csv')

with quality:
    st.subheader('Data quality audit')
    st.caption('Full saved raw and cleaned datasets; transaction filters do not apply here.')
    cols = st.columns(4)
    values = [len(raw), int(raw.amount.isna().sum()), len(raw)-len(cleaned), int(raw.transaction_id.duplicated().sum())]
    for col, label, value in zip(cols, ['Raw rows', 'Missing amounts', 'Rows excluded', 'Duplicate IDs'], values):
        col.metric(label, f'{value:,}')
    st.dataframe(raw.isna().sum().rename('missing_values').rename_axis('column').reset_index(), hide_index=True)
    st.write(f"Known raw injections: {int(raw.is_injected_anomaly.sum())}; cleaned injections: {int(cleaned.is_injected_anomaly.sum())}.")
    st.info('Missing amounts are excluded from numerical analysis. Dates have day resolution; same-day order is unknown. Merchant categories are present. Injection labels are evaluation-only fields.')
    st.caption(f"Development cold-start rows: {saved['phase2_metrics']['cold_start_rows']}. Prior averages use only earlier dates.")

with customers:
    st.subheader('Customer spending')
    st.caption('Computed from the filtered saved transactions. These descriptive totals are not historical model features.')
    if filtered.empty:
        st.info('No customer spending to display for these filters.')
    else:
        spending = filtered.groupby('customer_id', as_index=False).agg(transaction_count=('amount','size'), total_spent=('amount','sum'), average_amount=('amount','mean')).sort_values('total_spent', ascending=False)
        chart_data = spending.head(10).copy()
        chart_data['customer_id'] = chart_data.customer_id.astype(str)
        st.plotly_chart(px.bar(chart_data, x='customer_id', y='total_spent', title='Top 10 customers in current selection', labels={'customer_id':'Customer', 'total_spent':'Total spent ($)'}), key='customers')
        st.dataframe(spending, hide_index=True)

with ranking:
    st.subheader('Transactions ranked for review')
    ranking_scope = st.selectbox('Ranking experiment', ['Phase 2 selected features · validation', 'Phase 1 · historical test'], key='ranking_experiment')
    ranked = saved['validation'] if ranking_scope.startswith('Phase 2') else saved['historical']
    st.caption('Saved scores and saved thresholds only. Larger scores mean more unusual transactions. Experiments have different models and score scales.')
    only_alerts = st.checkbox('Show saved alerts only')
    ranked = ranked.loc[ranked.transaction_id.isin(filtered.transaction_id)].copy()
    if only_alerts:
        ranked = ranked.loc[ranked.anomaly_flag]
    ranked = ranked.sort_values('anomaly_score', ascending=False)
    if ranked.empty:
        st.info('No scored transactions match this selection. Phase 2 ranks validation dates only; Phase 1 ranks historical test dates only.')
    else:
        st.plotly_chart(px.scatter(ranked, x='date', y='amount', color=ranked.anomaly_flag.map({True:'Alert', False:'Not alerted'}), hover_data=['transaction_id','customer_id','anomaly_score','is_injected_anomaly'], title='Saved review decisions', labels={'amount':'Amount ($)', 'color':'Decision'}), key='ranking')
        columns = ['transaction_id','customer_id','date','merchant_category','amount','anomaly_score','anomaly_flag','is_injected_anomaly']
        st.dataframe(ranked[columns], hide_index=True)
    st.download_button('Download ranked selection', ranked.to_csv(index=False).encode(), 'ranked_synthetic_transactions.csv', 'text/csv')

with evaluation:
    st.subheader('Historical development evidence')
    st.warning('Earlier failed Phase 2 independent study: 0 of 3,000 injected rows detected; 6 non-injected rows alerted across 300,000 scored rows. Phase 6 development audit: 16 of 670 injected rows detected (2.39% recall). These separate historical studies remain unchanged; the final paired comparison is the first tab.')
    st.caption('Full saved experiment splits. Sidebar transaction filters do not change these metrics.')
    scope = st.selectbox('Evaluation experiment', ['Phase 2 selected features · validation', 'Phase 1 · historical test'], key='evaluation_experiment')
    phase2 = scope.startswith('Phase 2')
    if phase2:
        st.markdown('### Model Selection Only — Two Injected Anomalies')
        metadata = saved['phase2_metrics']
        selected = next(item for item in metadata['results'] if item['feature_set'] == metadata['selected_feature_set'])
        metrics, predictions = selected, saved['validation']
        st.info(f"Threshold and features were chosen on this validation set. These are selection results, not independent test performance. Known validation injections: {metadata['validation_injections']}.")
        st.caption('Features: ' + ', '.join(metadata['feature_columns']))
    else:
        metrics, predictions = saved['phase1_metrics'], saved['historical']
        st.warning('Historical Phase 1 test: previously inspected baseline outcomes. These are not the final independent Phase 2 results; see the first tab for the accepted Stage 5 comparison.')
    cols = st.columns(4)
    alerts = int(predictions.anomaly_flag.sum())
    for col, label, value in zip(cols, ['Precision', 'Recall', 'F1', 'Saved alerts'], [f"{metrics['precision']:.1%}" if alerts else 'N/A', f"{metrics['recall']:.1%}", f"{metrics['f1']:.1%}", str(alerts)]):
        col.metric(label, value)
    st.caption(f"Rows: {len(predictions):,} · Known injections: {int(predictions.is_injected_anomaly.sum())} · Precision is undefined when there are no alerts (saved code convention: zero).")
    matrix = confusion_counts(predictions)
    st.plotly_chart(px.imshow(matrix, x=['Not alerted', 'Alerted'], y=['Not injected','Injected'], text_auto=True, color_continuous_scale='Blues', title='Confusion matrix against known synthetic injections', labels={'x':'Predicted review decision','y':'Synthetic label','color':'Transactions'}), key='confusion')
    if phase2:
        st.markdown('#### Validation threshold comparison')
        st.caption('Explore saved validation operating points. This control does not change the selected model, saved alerts or test results.')
        thresholds = saved['thresholds'].sort_values('threshold').reset_index(drop=True)
        chosen_index = int((thresholds.threshold-selected['threshold']).abs().idxmin())
        index = st.select_slider('Validation operating point', options=list(range(len(thresholds))), value=chosen_index, format_func=lambda i: f"{thresholds.iloc[i].threshold:.6f}")
        point = thresholds.iloc[index]
        st.write(f"Explored validation point: {int(point.alerts)} alerts · precision {point.precision:.1%} · recall {point.recall:.1%} · F1 {point.f1:.1%}")
        long = thresholds.melt(id_vars=['threshold','alerts'], value_vars=['precision','recall','f1'], var_name='metric', value_name='value')
        fig = px.line(long.sort_values('threshold'), x='threshold', y='value', color='metric', hover_data=['alerts'], title='Validation precision–recall tradeoff')
        fig.add_vline(x=float(selected['threshold']), line_dash='dash')
        st.plotly_chart(fig, key='thresholds')
        st.markdown('#### Feature comparison · validation only')
        st.dataframe(saved['comparison'], hide_index=True)
        st.caption('The Phase 1 reference is ineligible for selection because its training averages include later training records. Equal validation F1 favored the simpler prior-only feature set.')
    else:
        st.caption(f"Saved Phase 1 threshold: {metrics['selected_threshold']['threshold']:.6f} · precision@10: {metrics['precision_at_10']:.1%}. Ranking quality and threshold alert quality are different measures.")


with robustness:
    st.subheader('Historical development robustness experiments')
    st.caption('Prior robustness evidence is historical development context, not the final independent comparison. See the first tab for Stage 5.')
    try:
        robust = load_robustness()
    except (OSError, ValueError, KeyError) as exc:
        st.error(f'Unable to read the completed robustness experiment: {exc}')
        robust = None
    if robust is None:
        st.info('No completed robustness experiment found. Run main.py --phase 4 locally to create saved results.')
    else:
        st.caption(f"Completed run: {robust['run']} | Full experiment results; sidebar transaction filters do not apply.")
        st.info(f"Validation-selected algorithm: {robust['freeze']['selected_model']}. Models and thresholds were frozen before October synthetic periods were generated. Future results did not change this choice.")
        st.warning('Few synthetic injections, five seeds and three related scenarios cannot establish real-world fraud detection quality. Mean plus/minus sample standard deviation describes variation across seeds, not a confidence interval.')
        metric = st.selectbox('Robustness metric', ['precision', 'recall', 'f1', 'alerts'], key='robustness_metric')
        summary = robust['summary']
        fig = px.bar(summary, x='scenario', y=f'{metric}_mean', color='model',
            error_y=f'{metric}_std', barmode='group',
            labels={f'{metric}_mean': f'Mean {metric}', 'scenario':'Synthetic scenario', 'model':'Detector'},
            title=f'Future synthetic {metric}: mean and sample SD across seeds')
        st.plotly_chart(fig, key='robustness_chart')
        st.dataframe(summary, hide_index=True)
        with st.expander('Per-run evidence and evaluation conventions'):
            st.write('Precision and recall use zero_division=0 for summary averages; precision_defined and recall_defined identify undefined observations. Non-injected alerts are not confirmed legitimate transactions: they can still be unusual.')
            st.write('Scenarios share seed-controlled base transactions, so the scenario groups are related. LOF is deterministic for a fixed dataset; variation comes from generated data. Isolation Forest also varies its random seed.')
            st.dataframe(robust['future'], hide_index=True)
            st.caption('Validation results used for algorithm selection:')
            st.dataframe(robust['validation'], hide_index=True)
        st.download_button('Download future experiment results', robust['future'].to_csv(index=False).encode(), 'future_synthetic_experiments.csv', 'text/csv')

st.divider()
st.caption('Read-only experiment viewer · saved CSV/JSON artifacts · no training or threshold changes are written by the dashboard')
