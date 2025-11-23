def calculate_compound_interest(principal, rate, periods):
    """
    Calcula el valor futuro usando interés compuesto.
    principal: monto inicial (float)
    rate: tasa de interés anual en decimal (float)
    periods: número de períodos (int)
    """
    return principal * ((1 + rate) ** periods)

def calculate_annuity_payment(principal, rate, periods):
    """
    Calcula el pago periódico de una anualidad con tasa de interés compuesta.
    """
    if rate == 0:
        return principal / periods
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)

def calculate_internal_rate_of_return(cash_flows, iterations=100):
    """
    Calcula la TIR usando el método de Newton–Raphson.
    cash_flows: lista de flujos donde el primero es negativo (inversión) y los siguientes positivos.
    iterations: número máximo de iteraciones.
    """
    guess = 0.1
    for _ in range(iterations):
        npv = sum(cf / (1 + guess) ** i for i, cf in enumerate(cash_flows))
        derivative = sum(-i * cf / (1 + guess) ** (i + 1) for i, cf in enumerate(cash_flows))
        if derivative == 0:
            break
        guess -= npv / derivative
    return guess
