import pandas as pd

if __name__ == '__main__':
    # Load CSV file
    df = pd.read_csv("C:/temp/ssi.csv")

    # Step 1: Clean Data
    df.columns = df.columns.str.strip()
    df['Taxed Social Security Earnings'] = (
        df['Taxed Social Security Earnings'].replace('[\$,]', '', regex=True).astype(float)
    )

    # Step 2: Add indexing factors (using 2024 as the indexing year)
    indexing_year = 2030
    average_wage_index = {
        1991: 21081.66, 1992: 22229.79, 1993: 23132.67, 1994: 23753.53,
        1995: 24705.66, 1996: 25913.90, 1997: 27426.00, 1998: 28861.44,
        1999: 30469.84, 2000: 32154.82, 2001: 32921.92, 2002: 33252.09,
        2003: 34064.95, 2004: 35648.55, 2005: 36952.94, 2006: 38651.41,
        2007: 40405.48, 2008: 41334.97, 2009: 40711.61, 2010: 41673.83,
        2011: 42979.61, 2012: 44321.67, 2013: 44888.16, 2014: 46481.52,
        2015: 48098.63, 2016: 48642.15, 2017: 50321.89, 2018: 52145.80,
        2019: 54099.99, 2020: 55528.05, 2021: 60575.07, 2022: 61480.22,
        2023: 63574.19, 2024: 65350.00, 2025: 68574.19, 2026: 70350.00,   #  <== These are estimates
        2027: 72574.19, 2028: 75350.00, 2029: 77574.19, 2030: 79350.00,   #  <== These are estimates
    }

    df['AvgWageYear'] = df['Work Year'].map(average_wage_index)
    df['IndexingFactor'] = average_wage_index[indexing_year] / df['AvgWageYear']
    df['Indexed Earnings'] = df['Taxed Social Security Earnings'] * df['IndexingFactor']

    # Step 3: Compute AIME
    top_35_years = df.sort_values(by='Indexed Earnings', ascending=False).head(35)
    total_indexed_earnings = top_35_years['Indexed Earnings'].sum()
    aime = total_indexed_earnings / (35 * 12)

    # Step 4: Compute PIA using 2025 bend points (from https://www.ssa.gov/OACT/COLA/bendpoints.html)
    bend_point1 = 1426   #  <== These are estimates
    bend_point2 = 7891   #  <== These are estimates

    def compute_pia(aime):
        if aime <= bend_point1:
            return 0.90 * aime
        elif aime <= bend_point2:
            return 0.90 * bend_point1 + 0.32 * (aime - bend_point1)
        else:
            return (
                0.90 * bend_point1 +
                0.32 * (bend_point2 - bend_point1) +
                0.15 * (aime - bend_point2)
            )

    pia = compute_pia(aime)

    # Step 5: Adjust for claiming age
    pia_62 = pia * 0.70   # ~30% reduction at age 62
    pia_67 = pia * 1.00   # full retirement age (FRA)
    pia_70 = pia * 1.24   # ~8% annual increase after FRA

    # Output
    print(f"AIME:               ${aime:9,.2f}")
    print(f"PIA at age 62:      ${pia_62:9,.2f}")
    print(f"PIA at age 67 (FRA):${pia_67:9,.2f}")
    print(f"PIA at age 70:      ${pia_70:9,.2f}")
