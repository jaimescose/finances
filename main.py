import typer
import pandas as pd
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytz

app = typer.Typer()

DEFAULT_CSV_PATH = Path("/mnt/g/My Drive/life/finance/movimientos/actividades.csv")

# This dictionary maps the categories given by the expenses tracker app that I use to the categories used in my Expenses.ghseet
ZUMMA_TO_TEMPLATE = {
    'Ahorro': 'Ahorro/Inversión',
    'Comida': 'Comidas por fuera',
    'Cuidado personal': 'Otro',
    'Deudas': 'Deudas',
    'Diversión': 'Otro',
    'Educación': 'Educación',
    'Ejercicio': 'Salud',
    'Emprendimiento': 'Ahorro/Inversión',
    'Familia': 'Familia',
    'Gastos Administrativos': 'Servicios',
    'Gastos Operativos': 'Servicios',
    'Hijos': 'Familia',
    'Hogar': 'Vivienda',
    'Impuestos': 'Impuestos',
    'Intereses': 'Deudas',
    'Inversión': 'Ahorro/Inversión',
    'Marketing': 'Ahorro/Inversión',
    'Mascotas': 'Otro',
    'Materia Prima': 'Otro',
    'Oficina': 'Servicios',
    'Otros gastos': 'Otro',
    'Regalos': 'Otro',
    'Renta': 'Vivienda',
    'Restaurantes': 'Comidas por fuera',
    'Salud': 'Salud',
    'Seguros': 'Servicios',
    'Servicios': 'Servicios',
    'Shopping': 'Otro',
    'Supermercados': 'Mercado',
    'Suscripciones': 'Suscripciones',
    'Transporte': 'Transporte',
    'Viajes': 'Viajes'
}

OTROS_GASTOS = [k for k, v in ZUMMA_TO_TEMPLATE.items() if v == 'Otro']

TEMPLATE_TO_BUDGET = {
    'Mercado': 'needs',
    'Transporte': 'needs',
    'Salud': 'needs',
    'Educación': 'needs',
    'Suscripciones': 'wants',
    'Servicios': 'needs',
    'Deudas': 'needs',
    'Vivienda': 'needs',
    'Familia': 'needs',
    'Ahorro/Inversión': 'savings/investments',
    'Comidas por fuera': 'wants',
    'Otro': 'wants',
    'Viajes': 'wants',
    'Impuestos': 'needs'
}


@app.command()
def process_transactions(csv_path: Path = typer.Option(DEFAULT_CSV_PATH, "--csv", "-c", help="Path to the CSV file containing financial transactions")):
    if not csv_path.exists():
        typer.echo(f"The file {csv_path} does not exist.")
        raise typer.Exit(code=1)

    # Read the CSV file with date parsing
    df = pd.read_csv(csv_path, parse_dates=['fecha'], dayfirst=True)
    df['fecha'] = pd.to_datetime(df['fecha'], utc=True)

    # Convert 'fecha' to local time zone
    local_tz = pytz.timezone('America/Chicago')  # Replace with your local time zone
    df['fecha'] = df['fecha'].dt.tz_convert(local_tz)

    # Make 'fecha' timezone-unaware
    df['fecha'] = df['fecha'].dt.tz_localize(None)

    # Get the current date in the local time zone
    current_date = datetime.now()

    one_year_ago = current_date - timedelta(days=365)
    df = df[(df['fecha'] <= current_date) & (df['fecha'] > one_year_ago)]

    # Create new column 'month_year'
    df['month_year'] = df['fecha'].dt.strftime('%Y-%m')

    # Create new "template_category" column mapping "categoría" with ZUMMA_TO_TEMPLATE
    # Fill unmapped values with "Otro"
    df['template_category'] = df['categoría'].map(ZUMMA_TO_TEMPLATE).fillna('Otro')
    # Create new "budget_category" column mapping "template_category" with TEMPLATE_TO_BUDGET
    df['budget_category'] = df['template_category'].map(TEMPLATE_TO_BUDGET).fillna('wants')

    # Sort the DataFrame by date in descending order (most recent to oldest)
    df = df.sort_values('fecha', ascending=False)

    # Create expenses DataFrame
    expenses_df = df[df['tipo'] == 'gasto']
    expenses_output = csv_path.with_name('expenses.xlsx')
    expenses_df.to_excel(expenses_output, index=False)
    typer.echo(f"Expenses saved to {expenses_output}")

    # Create income DataFrame
    income_df = df[df['tipo'] == 'ingreso']
    income_output = csv_path.with_name('income.xlsx')
    income_df.to_excel(income_output, index=False)
    typer.echo(f"Income saved to {income_output}")

if __name__ == "__main__":
    app()
