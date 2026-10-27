import sqlite3
import unittest
from contextlib import closing
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal

APP = Path(__file__).resolve().parents[1]
REPOSITORY = Path(__file__).resolve().parents[3]

class SqlExamplesTests(unittest.TestCase):
    def data(self):
        return pd.read_csv(APP/'outputs/phase1/cleaned_transactions.csv')

    def queries(self):
        return [query.strip() for query in (REPOSITORY/'sql/analysis.sql').read_text(encoding='utf-8').split(';') if query.strip()]

    def test_customer_sql_matches_pandas(self):
        data = self.data()
        with closing(sqlite3.connect(':memory:')) as con:
            data.to_sql('transactions', con, index=False)
            actual = pd.read_sql_query(self.queries()[0], con)
        expected = data.groupby('customer_id', as_index=False).agg(
            transaction_count=('amount','size'), total_spent=('amount','sum'))
        expected = expected.loc[expected.total_spent > 2000].sort_values('total_spent', ascending=False).head(5).reset_index(drop=True)
        expected.total_spent = expected.total_spent.round(2)
        assert_frame_equal(actual, expected)

    def test_daily_and_validation_queries_account_for_rows(self):
        data = self.data()
        with closing(sqlite3.connect(':memory:')) as con:
            data.to_sql('transactions', con, index=False)
            daily = pd.read_sql_query(self.queries()[1], con)
            validation = pd.read_sql_query(self.queries()[2], con)
        self.assertEqual(int(daily.transaction_count.sum()), len(data))
        period = data.loc[(data.date >= '2026-09-15') & (data.date < '2026-09-21')]
        counts = period.groupby('customer_id').size()
        expected = counts[counts >= 2].sort_index()
        actual = validation.set_index('customer_id').validation_transactions.sort_index()
        self.assertEqual(actual.to_dict(), expected.to_dict())

if __name__ == '__main__':
    unittest.main()
