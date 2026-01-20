#streamlit run 002_Initialization_Process_App.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Initialization Process Analysis",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Initialization Process Analysis Tool")
st.markdown("Upload your data files to compare Market Characterization vs Utility Forecast for Electric (kWh) and Gas (MMBTU)")

# Helper functions
def clean_column_names(df):
    """Standardize column names to snake_case"""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('$', 'usd').str.replace('/', 'per').str.replace('&', 'and').str.replace('.', '')
    return df

def disagg_to_percentage(df):
    """Convert actual energy use to percentage distribution"""
    df_perc = df.copy()
    for col in df_perc.columns:
        if col not in ['condition_name', 'sector', 'electric_utility', 'gas_utility', 'building_type', 'end_use']:
            total = df_perc[col].sum()
            if total > 0:
                df_perc[col] = df_perc[col] / total
            else:
                df_perc[col] = 0
    return df_perc

def format_label(text):
    """Convert snake_case to Title Case for display"""
    if pd.isna(text):
        return text
    return str(text).replace('_', ' ').title()

# File upload section
st.header("📁 Upload Data Files")

col1, col2, col3 = st.columns(3)

with col1:
    utility_forecast_file = st.file_uploader(
        "Utility Forecast Disaggregation",
        type=['xlsx', 'xls'],
        help="Upload the utility forecast file with Sector_Forecast, Building_Type_Disagg, Electric_Enduse_Disagg, and Gas_Enduse_Disagg sheets"
    )

with col2:
    market_char_file = st.file_uploader(
        "Market Characterization (Year 1)",
        type=['xlsx', 'xls'],
        help="Upload the df_yr1 market characterization output file"
    )

with col3:
    condition_energy_file = st.file_uploader(
        "Condition Energy Usage Template",
        type=['xlsx', 'xls'],
        help="Upload the condition energy usage template file"
    )

# Check if all files are uploaded
if utility_forecast_file and market_char_file and condition_energy_file:
    
    try:
        # Progress bar
        progress_bar = st.progress(0, text="Processing data...")
        
        # ========== LOAD AND PROCESS UTILITY FORECAST DATA ==========
        progress_bar.progress(10, text="Loading utility forecast data...")
        
        # Load utility forecast sheets
        df_utility_forecast = pd.read_excel(utility_forecast_file, sheet_name="Sector_Forecast")
        df_utility_forecast = clean_column_names(df_utility_forecast).iloc[:1]
        
        res_stock_building_type_disagg = pd.read_excel(utility_forecast_file, sheet_name="Building_Type_Disagg")
        res_stock_building_type_disagg = clean_column_names(res_stock_building_type_disagg)
        
        res_stock_electric_disagg = pd.read_excel(utility_forecast_file, sheet_name="Electric_Enduse_Disagg")
        res_stock_electric_disagg = clean_column_names(res_stock_electric_disagg)
        
        res_stock_gas_disagg = pd.read_excel(utility_forecast_file, sheet_name="Gas_Enduse_Disagg")
        res_stock_gas_disagg = clean_column_names(res_stock_gas_disagg)
        
        # Convert to percentages
        res_stock_electric_disagg_pct = disagg_to_percentage(res_stock_electric_disagg)
        res_stock_gas_disagg_pct = disagg_to_percentage(res_stock_gas_disagg)
        
        # ========== PROCESS ELECTRIC DATA ==========
        progress_bar.progress(25, text="Processing electric data...")
        
        if 'kwh_residential' not in df_utility_forecast.columns:
            st.error('Expected column `kwh_residential` in utility forecast file')
            st.stop()
        
        kwh_residential = float(df_utility_forecast['kwh_residential'].iloc[0]) if not pd.isna(df_utility_forecast['kwh_residential'].iloc[0]) else 0.0
        
        building_cols = ['single_family', 'multifamily', 'single_family_li', 'multifamily_li']
        missing = [c for c in building_cols if c not in res_stock_building_type_disagg.columns]
        if missing:
            st.error(f'Missing expected building-type columns: {missing}')
            st.stop()
        
        res_stock_building_type_disagg_residential_electric = res_stock_building_type_disagg[building_cols].iloc[:1]
        bvals = res_stock_building_type_disagg_residential_electric.iloc[0].fillna(0).astype(float)
        
        if bvals.sum() > 0:
            bfrac = bvals / bvals.sum()
        else:
            bfrac = pd.Series(1.0 / len(bvals), index=bvals.index)
        
        by_building_energy = (bfrac * kwh_residential).to_frame().T
        by_building_energy.index = ['allocated_kwh_residential']
        
        # Disaggregate by end use for electric
        if 'end_use' in res_stock_electric_disagg_pct.columns:
            enduse_pct = res_stock_electric_disagg_pct.set_index('end_use').copy()
        else:
            enduse_pct = res_stock_electric_disagg_pct.copy()
        
        enduse_pct_building = enduse_pct[building_cols].astype(float).fillna(0)
        
        if 'allocated_kwh_residential' in by_building_energy.index:
            by_building_series = by_building_energy.loc['allocated_kwh_residential']
        else:
            by_building_series = by_building_energy.iloc[0]
        
        by_building_series = by_building_series.reindex(building_cols).astype(float).fillna(0)
        allocated_kwh = enduse_pct_building.multiply(by_building_series, axis=1)
        
        # ========== PROCESS GAS DATA ==========
        progress_bar.progress(40, text="Processing gas data...")
        
        if 'mmbtu_residential' not in df_utility_forecast.columns:
            st.error('Expected column `mmbtu_residential` in utility forecast file')
            st.stop()
        
        mmbtu_residential = float(df_utility_forecast['mmbtu_residential'].iloc[0]) if not pd.isna(df_utility_forecast['mmbtu_residential'].iloc[0]) else 0.0
        
        res_stock_building_type_disagg_residential_gas = res_stock_building_type_disagg[building_cols].iloc[:1]
        bvals_gas = res_stock_building_type_disagg_residential_gas.iloc[0].fillna(0).astype(float)
        
        if bvals_gas.sum() > 0:
            bfrac_gas = bvals_gas / bvals_gas.sum()
        else:
            bfrac_gas = pd.Series(1.0 / len(bvals_gas), index=bvals_gas.index)
        
        by_building_energy_gas = (bfrac_gas * mmbtu_residential).to_frame().T
        by_building_energy_gas.index = ['allocated_mmbtu_residential']
        
        # Disaggregate by end use for gas
        if 'end_use' in res_stock_gas_disagg_pct.columns:
            enduse_pct_gas = res_stock_gas_disagg_pct.set_index('end_use').copy()
        else:
            enduse_pct_gas = res_stock_gas_disagg_pct.copy()
        
        enduse_pct_building_gas = enduse_pct_gas[building_cols].astype(float).fillna(0)
        
        if 'allocated_mmbtu_residential' in by_building_energy_gas.index:
            by_building_series_gas = by_building_energy_gas.loc['allocated_mmbtu_residential']
        else:
            by_building_series_gas = by_building_energy_gas.iloc[0]
        
        by_building_series_gas = by_building_series_gas.reindex(building_cols).astype(float).fillna(0)
        allocated_mmbtu = enduse_pct_building_gas.multiply(by_building_series_gas, axis=1)
        
        # ========== LOAD AND PROCESS MARKET CHARACTERIZATION DATA ==========
        progress_bar.progress(55, text="Loading market characterization data...")
        
        df_yr1 = pd.read_excel(market_char_file)
        df_yr1 = df_yr1.rename(columns={'condition': 'condition_name'})
        
        # Unpivot building type columns
        building_type_cols = [col for col in df_yr1.columns if col.endswith('_year_one')]
        id_cols = [col for col in df_yr1.columns if not col.endswith('_year_one')]
        
        df_yr1 = df_yr1.melt(
            id_vars=id_cols,
            value_vars=building_type_cols,
            var_name='building_type_raw',
            value_name='count'
        )
        
        df_yr1['building_type'] = df_yr1['building_type_raw'].str.replace('_year_one', '')
        df_yr1 = df_yr1.drop(columns=['building_type_raw'])
        df_yr1 = df_yr1[df_yr1['count'] > 0].reset_index(drop=True)
        
        # ========== LOAD CONDITION ENERGY USAGE ==========
        progress_bar.progress(70, text="Loading condition energy usage data...")
        
        condition_input = pd.read_excel(condition_energy_file, sheet_name="Sheet1")
        condition_input = clean_column_names(condition_input)
        
        # ========== MERGE AND CALCULATE TOTALS ==========
        progress_bar.progress(80, text="Calculating total market energy...")
        
        THERMS_TO_MMBTU = 0.1
        
        combined_df = df_yr1.merge(
            condition_input,
            on=['condition_name', 'building_type'],
            how='inner'
        )
        
        combined_df['total_market_energy_kwh'] = combined_df['annual_electric_energy_kwh'] * combined_df['count']
        combined_df['annual_natural_gas_mmbtu'] = combined_df['annual_natural_gas_therms'] * THERMS_TO_MMBTU
        combined_df['total_market_energy_mmbtu'] = combined_df['annual_natural_gas_mmbtu'] * combined_df['count']
        combined_df['total_market_energy'] = combined_df['total_market_energy_kwh']
        
        progress_bar.progress(100, text="Complete!")
        progress_bar.empty()
        
        # ========== DISPLAY RESULTS ==========
        st.success("✅ Data processed successfully!")
        
        # Summary metrics
        st.header("📊 Summary Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Utility Forecast (kWh)", f"{kwh_residential:,.0f}")
        with col2:
            st.metric("Total Market Energy (kWh)", f"{combined_df['total_market_energy_kwh'].sum():,.0f}")
        with col3:
            st.metric("Total Utility Forecast (MMBTU)", f"{mmbtu_residential:,.0f}")
        with col4:
            st.metric("Total Market Energy (MMBTU)", f"{combined_df['total_market_energy_mmbtu'].sum():,.0f}")
        
        # ========== MARKET CHARACTERIZATION VISUALIZATION ==========
        st.header("🏠 Market Characterization Energy by End Use and Building Type")
        
        agg_df = combined_df.groupby(['end_use', 'building_type'])['total_market_energy'].sum().reset_index()
        agg_df['end_use_display'] = agg_df['end_use'].apply(format_label)
        agg_df['building_type_display'] = agg_df['building_type'].apply(format_label)
        
        fig_market = px.bar(
            agg_df,
            x='end_use_display',
            y='total_market_energy',
            color='building_type_display',
            barmode='stack',
            title='Total Market Energy by End Use and Building Type',
            labels={'total_market_energy': 'Total Market Energy (kWh)', 'end_use_display': 'End Use', 'building_type_display': 'Building Type'}
        )
        
        st.plotly_chart(fig_market, use_container_width=True)
        
        # ========== UTILITY FORECAST VISUALIZATION ==========
        st.header("⚡ Utility Forecast Energy by End Use and Building Type")
        
        allocated_kwh_long = allocated_kwh.reset_index().melt(
            id_vars='end_use',
            var_name='building_type',
            value_name='allocated_kwh'
        )
        
        fig_forecast = px.bar(
            allocated_kwh_long,
            x='end_use',
            y='allocated_kwh',
            color='building_type',
            barmode='stack',
            title='Allocated kWh by End Use and Building Type',
            labels={'allocated_kwh': 'Allocated kWh', 'end_use': 'End Use'}
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # ========== COMPARISON VISUALIZATIONS ==========
        st.header("🔄 Comparison: Market Characterization vs Utility Forecast")
        
        # Prepare comparison data for electric
        market_data_electric = combined_df.groupby(['end_use', 'building_type'])['total_market_energy_kwh'].sum().reset_index()
        market_data_electric['source'] = 'Market Characterization'
        market_data_electric = market_data_electric.rename(columns={'total_market_energy_kwh': 'energy_kwh'})
        
        forecast_data_electric = allocated_kwh.reset_index().melt(
            id_vars='end_use',
            var_name='building_type',
            value_name='energy_kwh'
        )
        forecast_data_electric['source'] = 'Utility Forecast'
        
        comparison_df_electric = pd.concat([market_data_electric, forecast_data_electric], ignore_index=True)
        comparison_df_electric['end_use_display'] = comparison_df_electric['end_use'].apply(format_label)
        comparison_df_electric['building_type_display'] = comparison_df_electric['building_type'].apply(format_label)
        
        # Prepare comparison data for gas
        market_data_gas = combined_df.groupby(['end_use', 'building_type'])['total_market_energy_mmbtu'].sum().reset_index()
        market_data_gas['source'] = 'Market Characterization'
        market_data_gas = market_data_gas.rename(columns={'total_market_energy_mmbtu': 'energy_mmbtu'})
        
        forecast_data_gas = allocated_mmbtu.reset_index().melt(
            id_vars='end_use',
            var_name='building_type',
            value_name='energy_mmbtu'
        )
        forecast_data_gas['source'] = 'Utility Forecast'
        
        comparison_df_gas = pd.concat([market_data_gas, forecast_data_gas], ignore_index=True)
        comparison_df_gas['end_use_display'] = comparison_df_gas['end_use'].apply(format_label)
        comparison_df_gas['building_type_display'] = comparison_df_gas['building_type'].apply(format_label)
        
        # Tabs for Electric and Gas comparisons
        tab1, tab2 = st.tabs(["⚡ Electric (kWh)", "🔥 Gas (MMBTU)"])
        
        with tab1:
            st.subheader("Electric Comparison")
            
            fig_electric = px.bar(
                comparison_df_electric,
                x='end_use_display',
                y='energy_kwh',
                color='building_type_display',
                facet_col='source',
                barmode='stack',
                title='Electric Comparison: Market Characterization vs Utility Forecast (kWh)',
                labels={'energy_kwh': 'Energy (kWh)', 'end_use_display': 'End Use', 'building_type_display': 'Building Type', 'source': 'Data Source'},
                height=500
            )
            
            fig_electric.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(size=14, weight='bold')))
            st.plotly_chart(fig_electric, use_container_width=True)
            
            # Percentage difference heatmap for electric
            st.subheader("Electric Percentage Difference Heatmap")
            
            pivot_market_electric = market_data_electric.pivot(index='end_use', columns='building_type', values='energy_kwh').fillna(0)
            pivot_forecast_electric = forecast_data_electric.pivot(index='end_use', columns='building_type', values='energy_kwh').fillna(0)
            
            all_end_uses_electric = sorted(set(pivot_market_electric.index) | set(pivot_forecast_electric.index))
            all_building_types_electric = sorted(set(pivot_market_electric.columns) | set(pivot_forecast_electric.columns))
            
            pivot_market_electric = pivot_market_electric.reindex(index=all_end_uses_electric, columns=all_building_types_electric, fill_value=0)
            pivot_forecast_electric = pivot_forecast_electric.reindex(index=all_end_uses_electric, columns=all_building_types_electric, fill_value=0)
            
            pct_diff_electric = pd.DataFrame(index=pivot_market_electric.index, columns=pivot_market_electric.columns)
            for col in pivot_market_electric.columns:
                for idx in pivot_market_electric.index:
                    forecast_val = pivot_forecast_electric.loc[idx, col]
                    market_val = pivot_market_electric.loc[idx, col]
                    if forecast_val != 0:
                        pct_diff_electric.loc[idx, col] = ((market_val - forecast_val) / forecast_val) * 100
                    elif market_val != 0:
                        pct_diff_electric.loc[idx, col] = 100
                    else:
                        pct_diff_electric.loc[idx, col] = 0
            
            pct_diff_electric = pct_diff_electric.astype(float)
            pct_diff_electric_formatted = pct_diff_electric.copy()
            pct_diff_electric_formatted.index = pct_diff_electric_formatted.index.map(format_label)
            pct_diff_electric_formatted.columns = pct_diff_electric_formatted.columns.map(format_label)
            
            fig_electric_heatmap = px.imshow(
                pct_diff_electric_formatted,
                labels=dict(x='Building Type', y='End Use', color='% Difference'),
                x=pct_diff_electric_formatted.columns,
                y=pct_diff_electric_formatted.index,
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title='Electric % Difference: (Market - Forecast) / Forecast × 100%',
                aspect='auto',
                text_auto='.1f'
            )
            
            fig_electric_heatmap.update_layout(height=500)
            st.plotly_chart(fig_electric_heatmap, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min % Difference", f"{pct_diff_electric.min().min():.2f}%")
            with col2:
                st.metric("Mean % Difference", f"{pct_diff_electric.mean().mean():.2f}%")
            with col3:
                st.metric("Max % Difference", f"{pct_diff_electric.max().max():.2f}%")
        
        with tab2:
            st.subheader("Gas Comparison")
            
            fig_gas = px.bar(
                comparison_df_gas,
                x='end_use_display',
                y='energy_mmbtu',
                color='building_type_display',
                facet_col='source',
                barmode='stack',
                title='Gas Comparison: Market Characterization vs Utility Forecast (MMBTU)',
                labels={'energy_mmbtu': 'Energy (MMBTU)', 'end_use_display': 'End Use', 'building_type_display': 'Building Type', 'source': 'Data Source'},
                height=500
            )
            
            fig_gas.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(size=14, weight='bold')))
            st.plotly_chart(fig_gas, use_container_width=True)
            
            # Percentage difference heatmap for gas
            st.subheader("Gas Percentage Difference Heatmap")
            
            pivot_market_gas = market_data_gas.pivot(index='end_use', columns='building_type', values='energy_mmbtu').fillna(0)
            pivot_forecast_gas = forecast_data_gas.pivot(index='end_use', columns='building_type', values='energy_mmbtu').fillna(0)
            
            all_end_uses_gas = sorted(set(pivot_market_gas.index) | set(pivot_forecast_gas.index))
            all_building_types_gas = sorted(set(pivot_market_gas.columns) | set(pivot_forecast_gas.columns))
            
            pivot_market_gas = pivot_market_gas.reindex(index=all_end_uses_gas, columns=all_building_types_gas, fill_value=0)
            pivot_forecast_gas = pivot_forecast_gas.reindex(index=all_end_uses_gas, columns=all_building_types_gas, fill_value=0)
            
            pct_diff_gas = pd.DataFrame(index=pivot_market_gas.index, columns=pivot_market_gas.columns)
            for col in pivot_market_gas.columns:
                for idx in pivot_market_gas.index:
                    forecast_val = pivot_forecast_gas.loc[idx, col]
                    market_val = pivot_market_gas.loc[idx, col]
                    if forecast_val != 0:
                        pct_diff_gas.loc[idx, col] = ((market_val - forecast_val) / forecast_val) * 100
                    elif market_val != 0:
                        pct_diff_gas.loc[idx, col] = 100
                    else:
                        pct_diff_gas.loc[idx, col] = 0
            
            pct_diff_gas = pct_diff_gas.astype(float)
            pct_diff_gas_formatted = pct_diff_gas.copy()
            pct_diff_gas_formatted.index = pct_diff_gas_formatted.index.map(format_label)
            pct_diff_gas_formatted.columns = pct_diff_gas_formatted.columns.map(format_label)
            
            fig_gas_heatmap = px.imshow(
                pct_diff_gas_formatted,
                labels=dict(x='Building Type', y='End Use', color='% Difference'),
                x=pct_diff_gas_formatted.columns,
                y=pct_diff_gas_formatted.index,
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title='Gas % Difference: (Market - Forecast) / Forecast × 100%',
                aspect='auto',
                text_auto='.1f'
            )
            
            fig_gas_heatmap.update_layout(height=500)
            st.plotly_chart(fig_gas_heatmap, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min % Difference", f"{pct_diff_gas.min().min():.2f}%")
            with col2:
                st.metric("Mean % Difference", f"{pct_diff_gas.mean().mean():.2f}%")
            with col3:
                st.metric("Max % Difference", f"{pct_diff_gas.max().max():.2f}%")
        
        # ========== DATA TABLES ==========
        st.header("📋 Data Tables")
        
        with st.expander("View Combined Data"):
            st.dataframe(combined_df, use_container_width=True)
        
        with st.expander("View Allocated kWh by End Use and Building Type"):
            st.dataframe(allocated_kwh, use_container_width=True)
        
        with st.expander("View Allocated MMBTU by End Use and Building Type"):
            st.dataframe(allocated_mmbtu, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.exception(e)

else:
    # Instructions when files are not uploaded
    st.info("👆 Please upload all three required files to begin the analysis")
    
    with st.expander("ℹ️ File Requirements"):
        st.markdown("""
        **1. Utility Forecast Disaggregation File**
        - Must contain sheets: `Sector_Forecast`, `Building_Type_Disagg`, `Electric_Enduse_Disagg`, `Gas_Enduse_Disagg`
        - `Sector_Forecast` should have columns: `kwh_residential`, `mmbtu_residential`
        - `Building_Type_Disagg` should have columns: `single_family`, `multifamily`, `single_family_li`, `multifamily_li`
        
        **2. Market Characterization File (Year 1)**
        - Output from Market Characterization process (df_yr1)
        - Should contain equipment counts by building type
        - Must have a `condition` column (will be renamed to `condition_name`)
        
        **3. Condition Energy Usage Template**
        - Must have Sheet1 with condition energy data
        - Should contain columns: `condition_name`, `building_type`, `annual_electric_energy_kwh`, `annual_natural_gas_therms`
        """)

# Footer
st.markdown("---")
st.markdown("**Initialization Process Analysis Tool** | Compare Market Characterization against Utility Forecasts")
