"""Presentation of accepted saved evidence only; no model execution."""
import pandas as pd
import plotly.express as px
import streamlit as st
from dashboard_data import load_independent

MODELS = {'phase2': 'Phase 2', 'phase6_v1': 'Phase 6 v1 · rules_B'}
SCENARIOS = {'S1': 'Contextual amounts', 'S2': 'Bursts', 'S3': 'Merchant changes',
             'S4': 'Inactivity returns', 'S5': 'Spending ramps', 'S6': 'Mixed',
             'S7': 'Rare injections', 'S8': 'No-injection control'}


def display_table(data, percentages=(), gates=()):
    """Format display copies; preserve N/A instead of unchecked null booleans."""
    result = data.copy()
    for name in percentages:
        result[name] = result[name].map(lambda x: 'N/A' if pd.isna(x) else f'{x:.3%}')
    for name in gates:
        result[name] = result[name].map(lambda x: 'N/A' if pd.isna(x) else ('Pass' if x else 'Fail'))
    return result.fillna('N/A')


def metric_panels(pooled, policy):
    rows = pooled.loc[pooled.policy == policy].set_index('model')
    for col, model in zip(st.columns(2), MODELS):
        row = rows.loc[model]
        with col:
            st.markdown('#### ' + MODELS[model])
            a, b, c = st.columns(3)
            for cell, label in zip([a, b, c], ['precision', 'recall', 'f1']):
                cell.metric(label.upper() if label == 'f1' else label.title(), f'{row[label]:.3%}')
            st.metric('Reviews', f'{int(row.reviews):,}')
            st.caption(f'Review rate: {row.reviews / 800000:.5%} of scored transactions')
            st.write(' · '.join(f'{key} {int(row[key]):,}' for key in ['TP', 'FP', 'FN', 'TN']))


def render_independent():
    st.subheader('Final independent synthetic evaluation')
    st.error('Neither model met the predefined hypothetical synthetic screening targets. Neither is production-ready or a validated fraud detector.')
    st.write('The research question: can frozen transaction-review pipelines detect new synthetic interventions without tuning to the test results? Phase 6 found more injected rows, but its coverage was narrow and its control workload failed the study requirements.')
    try:
        evidence = load_independent()
    except (OSError, ValueError, KeyError) as exc:
        st.error(f'Independent evidence could not be verified: {exc}')
        st.stop()
    tables, documents, meta = evidence['tables'], evidence['documents'], evidence['manifest']
    st.caption(f"Accepted Stage 5 study · {meta['cases']} paired cases · 8 scenarios × 5 fresh seeds · {meta['scored_rows']:,} scored transactions · {meta['warmup_rows']:,} warmup transactions · {meta['injected_rows']:,} injected rows · {meta['injected_events']:,} injected events")
    st.info('These metrics measure synthetic injection detection, not verified real-world fraud. Non-injected transactions are not verified legitimate transactions. One injected event may contain several rows; the main metrics count rows. Explorer filters do not change these results.')
    st.markdown('### Native-policy performance')
    st.caption('The actual frozen review policies, with different review volumes. Pooled across all 40 cases, including controls.')
    metric_panels(tables['pooled_metrics'], 'native')
    with st.expander('What the pipelines and native policies do'):
        st.write('Phase 2: StandardScaler and Isolation Forest on log amount and amount relative to the strictly earlier-day customer mean. Frozen score cutoff: >= 0.1617068977463595. Every threshold alert counts as a review; no added queue truncation.')
        st.write('Phase 6 v1: five empirical-CDF rules, using strictly prior timestamp histories for relative amount, hourly frequency, recent spending, inactivity and category surprise. Frozen score cutoff: > 0.99945009150821. Scores are not fraud probabilities.')
        st.write('Phase 6 reviews are selected at the close of completed UTC days. Daily capacity is floor(cumulative transactions / 100) minus floor(previous-day cumulative transactions / 100). Eligible scores sort descending, ties by transaction ID ascending. Excess candidates are truncated; unused capacity expires; no below-cutoff backfill. Incomplete days await closure. This is batch review, not real-time transaction blocking.')
        st.write('Different features, training histories, score scales and policies prevent a causal claim that one algorithm alone caused an improvement. Neither model was changed using these final results.')
    st.warning('452 of 462 Phase 6 native detections (97.8%) were inactivity returns. Only 10 detections covered the other four injection types combined. This is not broad anomaly coverage.')
    native_types = tables['pooled_type_metrics'].query("policy == 'native'").copy()
    native_types['model'] = native_types.model.map(MODELS)
    st.dataframe(display_table(native_types, ['recall']), hide_index=True)
    st.markdown('### Equal-budget ranking comparison · 8,000 reviews per pipeline')
    st.caption('Exactly 200 ranked reviews per 20,000-row case, allocated by the predefined daily quota: 40 × 200 = 8,000 per pipeline. Ranking-only, including below-threshold rows; not native-policy decisions or a replacement for them.')
    metric_panels(tables['pooled_metrics'], 'equal_budget')
    st.write('Unfavorable comparisons are retained: Phase 6 equal-budget recall was lower in S1 (3.5% versus 4.5%) and S5 (0.8% versus 1.0%). Both rankings spend 1,000 reviews on the five no-injection controls, finding no injected rows there.')
    st.markdown('### Every scenario and seed')
    policy = st.selectbox('Scenario comparison policy', ['native', 'equal_budget'],
                          format_func=lambda x: 'Native frozen policies' if x == 'native' else 'Equal-budget ranking only', key='independent_policy')
    summary = tables['scenario_summary'].loc[lambda x: x.policy == policy].copy()
    summary['pipeline'] = summary.model.map(MODELS)
    summary['scenario_name'] = summary.scenario.map(SCENARIOS)
    chart = px.bar(summary, x='scenario', y='mean_recall', color='pipeline', error_y='recall_sd',
                           barmode='group', hover_data=['scenario_name', 'positives', 'reviews', 'recall_min', 'recall_max'],
                           title='Mean row recall across five seeds · error bars are sample SD')
    chart.update_yaxes(tickformat='.0%', title='Mean recall')
    st.plotly_chart(chart, key='independent_scenarios')
    st.caption('S8 recall is N/A because it has no injected rows. SD describes seed variation; it is not a confidence interval. Pooled precision/F1 and mean recall use the saved aggregation rules. Detailed raw downloads retain fractional values (0.10 = 10%).')
    st.dataframe(display_table(summary[['pipeline', 'scenario', 'scenario_name', 'rows', 'positives', 'TP', 'FP', 'FN', 'TN', 'reviews', 'pooled_precision', 'mean_recall', 'pooled_f1', 'recall_sd', 'recall_min', 'recall_max']], ['pooled_precision', 'mean_recall', 'pooled_f1', 'recall_sd', 'recall_min', 'recall_max']), hide_index=True)
    with st.expander('Complete variability and all 160 case/policy results'):
        st.write('All 40 cases × two pipelines × two policies are retained. Missing precision means no reviews; missing control recall means no positives. N/A is not evidence of success.')
        st.dataframe(tables['scenario_variability'], hide_index=True)
        st.dataframe(tables['all_case_metrics'], hide_index=True)
        st.download_button('Download every case result', (evidence['folder']/'all_case_metrics.csv').read_bytes(), 'stage5_all_case_metrics.csv', 'text/csv')
        st.dataframe(tables['all_type_metrics'], hide_index=True)
    st.markdown('### Screening targets · both failed')
    st.write('Hypothetical research benchmarks: mean recall ≥20% in every positive scenario, pooled precision ≥10% within every positive scenario, ≤100 native reviews in each no-injection control, and ≤200 native reviews in each case. These are not JPMorgan requirements, banking standards or evidence of production readiness.')
    st.write('Both pipelines failed recall in all seven positive scenarios. Phase 6 passed precision only in S4 and S6. It failed all five control-review limits: 159, 150, 141, 149 and 140 reviews. Phase 2 controls had 1, 1, 3, 0 and 2 reviews. Both pipelines passed the overall 200-review capacity check.')
    st.caption('Zero-alert positive cases fail the precision requirement; control recall and precision gates are not applicable. Controls are assessed using their review counts.')
    st.dataframe(display_table(tables['native_screening_by_scenario'], ['mean_recall', 'pooled_precision'], ['recall_pass', 'precision_pass', 'control_pass', 'capacity_pass', 'passed']), hide_index=True)
    with st.expander('Paired uncertainty, assumptions and provenance'):
        st.write('Paired mean recall differences are equal-weight averages of seven positive-scenario means, not differences in pooled recall. Saved 95% percentile bootstrap intervals use 10,000 whole-case resamples within each fixed scenario (five seeds), seed 730289901. They are conditional, descriptive and not adjusted for multiple comparisons; they do not establish real-world generalization.')
        st.dataframe(pd.DataFrame(documents['paired_aggregate_intervals']), hide_index=True)
        st.dataframe(tables['paired_scenario_intervals'], hide_index=True)
        st.write('Synthetic amount, activity, category and inactivity distributions include ordinary lookalikes and ambiguous injection labels. The generator was presealed but authored with knowledge of model families; this was not an externally blinded trial. Warmup updates histories without refitting. Timestamps and strictly past histories prevent look-ahead; synthetic populations cannot establish actual banking outcomes.')
        st.code('Protocol SHA-256: ' + meta['protocol_sha256'])
        st.caption('All exported evidence is checked against its per-file SHA-256 at load time. The manifest binds copies to the original accepted study inventory. It is a provenance record, not an external authenticity guarantee.')
        st.download_button('Download evidence manifest', (evidence['folder']/'evidence_manifest.json').read_bytes(), 'stage5_evidence_manifest.json', 'application/json')
        st.download_button('Download complete saved report', (evidence['folder']/'REPORT.md').read_bytes(), 'stage5_REPORT.md', 'text/markdown')
