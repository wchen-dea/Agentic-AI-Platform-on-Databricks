from pydantic_ai import Agent, RunContext

from .base import BaseSpecialistAgent, SpecialistDeps

_SYSTEM = """You are a senior data engineer specializing in data pipelines, warehousing, and infrastructure.

Your responsibilities:
- Design and implement ETL/ELT pipelines (Apache Spark, dbt, Airflow, Prefect, dlt)
- Build streaming pipelines (Kafka, Flink, Kinesis, Pub/Sub)
- Data warehouse modeling (star/snowflake schema, slowly changing dimensions)
- Write optimized SQL for analytics (window functions, CTEs, partitioning)
- Set up data lake architectures (Delta Lake, Iceberg, Hudi)
- Data quality checks and monitoring (Great Expectations, dbt tests, Soda)
- Orchestration (Apache Airflow DAGs, Prefect flows, Dagster assets)
- Implement CDC (Change Data Capture) patterns
- Cost optimization for cloud data platforms (BigQuery, Snowflake, Redshift)

When writing code:
- Write idempotent, restartable pipelines
- Partition and cluster data appropriately
- Include data quality assertions at each stage
- Log row counts, null rates, and schema changes
- Use incremental loading over full refreshes whenever possible
- Document data lineage and transformations
- Write SQL that is readable and maintainable with CTEs

Always produce working, production-ready data engineering code."""


class DataEngineerAgent(BaseSpecialistAgent):
    name = "data_engineer"
    role = "Data Engineer"
    system_prompt = _SYSTEM

    def _register_extra_tools(self, agent: Agent[SpecialistDeps, str]) -> None:
        from typing import Literal as _Literal

        @agent.tool
        def scaffold_pipeline(
            ctx: RunContext[SpecialistDeps],
            pipeline_name: str,
            framework: _Literal["prefect", "airflow", "python"],
            path: str,
        ) -> str:
            """Scaffold a data pipeline with source, transform, and sink stages.

            pipeline_name: Pipeline name.
            framework: Orchestration framework.
            path: Output file path.
            """
            pname = pipeline_name
            fw = framework
            if fw == "prefect":
                code = f'''"""Prefect pipeline: {pname}"""

from prefect import flow, task
from prefect.logging import get_run_logger
import pandas as pd
from datetime import datetime


@task(retries=3, retry_delay_seconds=60, name="extract")
def extract(run_date: str) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info(f"Extracting data for {{run_date}}")
    # TODO: replace with real source (DB query, API call, S3 read, etc.)
    df = pd.DataFrame({{"id": range(10), "value": range(10)}})
    logger.info(f"Extracted {{len(df)}} rows")
    return df


@task(name="transform")
def transform(df: pd.DataFrame) -> pd.DataFrame:
    logger = get_run_logger()
    # TODO: apply business logic transformations
    df = df.copy()
    df["processed_at"] = datetime.utcnow().isoformat()
    df = df.dropna()
    logger.info(f"Transformed {{len(df)}} rows")
    return df


@task(name="load")
def load(df: pd.DataFrame, run_date: str) -> int:
    logger = get_run_logger()
    # TODO: write to destination (DB, S3, warehouse, etc.)
    logger.info(f"Loading {{len(df)}} rows for {{run_date}}")
    return len(df)


@flow(name="{pname}", log_prints=True)
def {pname.lower().replace("-", "_")}_flow(run_date: str = "today") -> None:
    raw = extract(run_date)
    cleaned = transform(raw)
    n = load(cleaned, run_date)
    print(f"Pipeline complete: {{n}} rows loaded.")


if __name__ == "__main__":
    {pname.lower().replace("-", "_")}_flow()
'''
            elif fw == "airflow":
                code = f'''"""Airflow DAG: {pname}"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd


default_args = {{
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}}


def extract(**context) -> None:
    run_date = context["ds"]
    # TODO: extract from source
    df = pd.DataFrame({{"id": range(10)}})
    context["ti"].xcom_push(key="row_count", value=len(df))


def transform(**context) -> None:
    # TODO: transform data
    pass


def load(**context) -> None:
    # TODO: load to destination
    row_count = context["ti"].xcom_pull(key="row_count", task_ids="extract")
    print(f"Loaded {{row_count}} rows")


with DAG(
    dag_id="{pname}",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["etl"],
) as dag:
    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_load = PythonOperator(task_id="load", python_callable=load)

    t_extract >> t_transform >> t_load
'''
            else:
                code = f'''"""Plain Python ETL pipeline: {pname}"""

import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def extract(run_date: str) -> pd.DataFrame:
    log.info(f"Extracting for {{run_date}}")
    # TODO: implement extraction
    return pd.DataFrame({{"id": range(10), "value": range(10)}})


def transform(df: pd.DataFrame) -> pd.DataFrame:
    log.info(f"Transforming {{len(df)}} rows")
    df = df.copy().dropna()
    df["processed_at"] = datetime.utcnow().isoformat()
    return df


def load(df: pd.DataFrame) -> int:
    log.info(f"Loading {{len(df)}} rows")
    # TODO: write to destination
    return len(df)


def run(run_date: str = "today") -> None:
    raw = extract(run_date)
    cleaned = transform(raw)
    n = load(cleaned)
    log.info(f"Pipeline complete: {{n}} rows loaded.")


if __name__ == "__main__":
    run()
'''
            full = ctx.deps.project_root / path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(code, encoding="utf-8")
            ctx.deps.result.files_written.append(path)
            return f"Scaffolded {pname} pipeline ({fw}) \u2192 {path}"

        @agent.tool
        def scaffold_dbt_model(
            ctx: RunContext[SpecialistDeps],
            model_name: str,
            path: str,
            materialization: _Literal["table", "view", "incremental"] = "incremental",
        ) -> str:
            """Scaffold a dbt SQL model with tests.

            model_name: Model name (snake_case).
            path: Output SQL file path.
            materialization: dbt materialization strategy.
            """
            model = model_name
            mat = materialization
            incremental_clause = (
                "\n    {% if is_incremental() %}\n    where updated_at > (select max(updated_at) from {{ this }})\n    {% endif %}"
                if mat == "incremental" else ""
            )
            code = f'''{{{{
  config(
    materialized="{mat}",
    unique_key="id",
    on_schema_change="sync_all_columns"
  )
}}}}

with source as (
    select * from {{{{ source("raw", "{model}") }}}}{incremental_clause}
),

renamed as (
    select
        id,
        -- TODO: add and rename columns
        updated_at
    from source
),

final as (
    select * from renamed
    where id is not null  -- basic quality gate
)

select * from final
'''
            full = ctx.deps.project_root / path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(code, encoding="utf-8")
            ctx.deps.result.files_written.append(path)

            # Also write schema.yml test file
            schema_path = path.replace(".sql", "_schema.yml")
            schema = f'''version: 2

models:
  - name: {model}
    description: "TODO: describe this model"
    columns:
      - name: id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: updated_at
        tests:
          - not_null
'''
            schema_full = ctx.deps.project_root / schema_path
            schema_full.parent.mkdir(parents=True, exist_ok=True)
            schema_full.write_text(schema, encoding="utf-8")
            ctx.deps.result.files_written.append(schema_path)
            return f"Scaffolded dbt model \u2192 {path}\nTests \u2192 {schema_path}"
