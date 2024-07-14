from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'calculate_squares_and_cubes',
    default_args=default_args,
    description='A simple Airflow DAG to calculate the sum of squares and cubes of a list of numbers',
    schedule_interval=None
)


def generate_numbers():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

generate_numbers_task = PythonOperator(
    task_id='generate_numbers_task',
    python_callable=generate_numbers,
    dag=dag,
)


def calculate_square_and_cube(numbers):
    square_and_cube_pairs = [(num, num ** 2, num ** 3) for num in numbers]
    return square_and_cube_pairs

calculate_square_and_cube_task = PythonOperator(
    task_id='calculate_square_and_cube_task',
    python_callable=calculate_square_and_cube,
    op_args=[],
    provide_context=True,
    trigger_rule='all_success',
    dag=dag
)


def sum_and_print(square_and_cube_pairs):
    sums = [(num, square + cube) for num, square, cube in square_and_cube_pairs]
    print(f"List of Sums: {sums}")

sum_and_print_task = PythonOperator(
    task_id='sum_and_print_task',
    python_callable=sum_and_print,
    provide_context=True,
    trigger_rule='all_success',
    dag=dag
)


generate_numbers_task >> calculate_square_and_cube_task >> sum_and_print_task

if __name__ == "__main__":
    dag.cli()