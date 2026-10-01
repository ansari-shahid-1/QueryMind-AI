
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.services.query_pipeline import QueryPipeline
from backend.services.insight_service import InsightService


st.set_page_config(
    page_title="QueryMind AI",
    page_icon="🔍",
    layout="wide"
)

st.title("QueryMind AI")
st.subheader("Ask questions. Get insights from your data.")

st.markdown(
    "Explore the Brazilian E-Commerce dataset using natural language."
)

st.divider()


if "response" not in st.session_state:
    st.session_state.response = None

if "insight" not in st.session_state:
    st.session_state.insight = None


question = st.text_input(
    "Ask a question about your data",
    placeholder="e.g. What are the top 5 product categories by sales?"
)


if st.button("Generate Insights"):
    if question.strip():
        try:
            with st.spinner("Analyzing your question..."):
                pipeline = QueryPipeline()
                response = pipeline.run(question)

                insight_service = InsightService()
                insight = insight_service.generate_insight(
                    question,
                    response["sql"],
                    response["result"]
                )

            st.session_state.response = response
            st.session_state.insight = insight

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    else:
        st.warning("Please enter a question first.")


if st.session_state.response is not None:

    response = st.session_state.response
    result = response["result"]

    st.success("Query executed successfully!")

    st.subheader("Generated SQL")
    st.code(response["sql"], language="sql")

    df = pd.DataFrame(
        result["rows"],
        columns=result["columns"]
    )

    st.subheader("Query Results")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    numeric_columns = []

    for column in df.columns:
        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if converted.notna().all():
            df[column] = converted
            numeric_columns.append(column)

    category_columns = [
        column
        for column in df.columns
        if column not in numeric_columns
    ]

    if numeric_columns and category_columns and len(df) > 1:

        value_column = numeric_columns[0]
        category_column = category_columns[0]

        category_count = df[category_column].nunique()

        date_keywords = [
            "date",
            "month",
            "year",
            "time",
            "period"
        ]

        is_time_column = any(
            keyword in category_column.lower()
            for keyword in date_keywords
        )

        if is_time_column:
            recommended_chart = "Line Chart"

        elif category_count <= 5:
            recommended_chart = "Pie Chart"

        else:
            recommended_chart = "Bar Chart"

        st.subheader("Data Visualization")

        st.caption(
            f"Recommended visualization: {recommended_chart}"
        )

        chart_options = [
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Scatter Plot"
        ]

        if "chart_type" not in st.session_state:
            st.session_state.chart_type = recommended_chart

        chart_type = st.selectbox(
            "Choose visualization",
            chart_options,
            index=chart_options.index(
                st.session_state.chart_type
            ),
            key="chart_type"
        )

        chart_df = df.copy()

        if chart_type == "Bar Chart":

            fig = px.bar(
                chart_df,
                x=value_column,
                y=category_column,
                orientation="h",
                title=(
                    f"{value_column.replace('_', ' ').title()} "
                    f"by {category_column.replace('_', ' ').title()}"
                ),
                text=value_column
            )

            fig.update_layout(
                xaxis_title=value_column.replace("_", " ").title(),
                yaxis_title=category_column.replace("_", " ").title(),
                yaxis=dict(autorange="reversed"),
                margin=dict(l=20, r=100, t=80, b=50)
            )

            fig.update_traces(
                texttemplate="%{text:,.2f}",
                textposition="outside",
                cliponaxis=False
            )

        elif chart_type == "Line Chart":

            fig = px.line(
                chart_df,
                x=category_column,
                y=value_column,
                title=(
                    f"{value_column.replace('_', ' ').title()} "
                    f"by {category_column.replace('_', ' ').title()}"
                ),
                markers=True
            )

        elif chart_type == "Pie Chart":

            fig = px.pie(
                chart_df,
                names=category_column,
                values=value_column,
                title=(
                    f"{value_column.replace('_', ' ').title()} "
                    f"by {category_column.replace('_', ' ').title()}"
                )
            )

        else:

            fig = px.scatter(
                chart_df,
                x=category_column,
                y=value_column,
                title=(
                    f"{value_column.replace('_', ' ').title()} "
                    f"by {category_column.replace('_', ' ').title()}"
                )
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif len(df) == 1 and numeric_columns:

        st.subheader("Key Metric")

        metric_column = numeric_columns[0]
        metric_value = df[metric_column].iloc[0]

        st.metric(
            label=metric_column.replace("_", " ").title(),
            value=(
                f"{metric_value:,.2f}"
                if isinstance(metric_value, float)
                else f"{metric_value:,}"
            )
        )

    st.subheader("Key Insight")
    st.info(st.session_state.insight)
