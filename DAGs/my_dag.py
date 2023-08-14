import datetime

from airflow import models
from airflow.operators import bash_operator
from airflow.models import DAG, Variable
from airflow.operators import python_operator


# var = Variable.get("my_env_var")  
var = "Testing"

default_dag_args = {
    # The start_date describes when a DAG is valid / can be run. Set this to a
    # fixed point in time rather than dynamically, since it is evaluated every
    # time a DAG is parsed. See:
    # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
    "start_date": datetime.datetime(2018, 1, 1),
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
    "composer_sample_simple_greeting",
    schedule_interval=datetime.timedelta(days=1),
    default_args=default_dag_args,
) as dag:
    def greeting():
        import logging
        var = Variable.get("my_env_var")  
        logging.info("Hello World!!!")
        print(f"The value of 'my_env_var' is: {var}")

    # An instance of an operator is called a task. In this case, the
    # hello_python task calls the "greeting" Python function.
    hello_python = python_operator.PythonOperator(
        task_id="hello", python_callable=greeting
    )

    # Likewise, the goodbye_bash task calls a Bash script.
    goodbye_bash = bash_operator.BashOperator(
        task_id="bye", bash_command="echo Goodbye."
    )

    # Define the order in which the tasks complete by using the >> and <<
    # operators. In this example, hello_python executes before goodbye_bash.
    hello_python >> goodbye_bash
