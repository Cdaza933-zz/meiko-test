from datetime import timedelta
from datetime import datetime


def daterange(start_date, end_date):
  """
  Retorna los días entre dos rangos de fechas.
  :param start_date: date fecha inicial.
  :param end_date: date fecha final.
  :return: date lista de dias entre fechas.
  """

  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  days = int((end_date - start_date).days) + 1
  if days != 0:
    for n in range(days):
      yield (start_date + timedelta(n)).strftime("%Y-%m-%d")
  else:
    yield start_date.strftime("%Y-%m-%d")
