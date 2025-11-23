"""
Módulo de funciones financieras
"""

def calculate_compound_interest(principal, rate, periods):
    """
    Calcula el interés compuesto.
    
    Args:
        principal (float): Capital inicial
        rate (float): Tasa de interés (ej: 0.05 para 5%)
        periods (int): Número de períodos
    
    Returns:
        float: Monto final con interés compuesto
    
    Raises:
        ValueError: Si los parámetros son inválidos
    """
    if principal < 0:
        raise ValueError("El capital principal no puede ser negativo")
    if rate < 0:
        raise ValueError("La tasa de interés no puede ser negativa")
    if periods < 0:
        raise ValueError("Los períodos no pueden ser negativos")
    if not isinstance(periods, int):
        raise ValueError("Los períodos deben ser un número entero")
    
    return principal * (1 + rate) ** periods


def calculate_annuity_payment(principal, rate, periods):
    """
    Calcula el pago de una anualidad.
    
    Args:
        principal (float): Capital inicial del préstamo
        rate (float): Tasa de interés por período
        periods (int): Número de períodos
    
    Returns:
        float: Pago periódico de la anualidad
    
    Raises:
        ValueError: Si los parámetros son inválidos
    """
    if principal < 0:
        raise ValueError("El capital principal no puede ser negativo")
    if rate < 0:
        raise ValueError("La tasa de interés no puede ser negativa")
    if periods <= 0:
        raise ValueError("Los períodos deben ser mayores a cero")
    if not isinstance(periods, int):
        raise ValueError("Los períodos deben ser un número entero")
    
    # Caso especial: tasa de interés cero
    if rate == 0:
        return principal / periods
    
    # Fórmula de anualidad
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)


def calculate_internal_rate_of_return(cash_flows, iterations=100):
    """
    Calcula la tasa interna de retorno (TIR/IRR) usando el método de Newton-Raphson.
    
    Args:
        cash_flows (list): Lista de flujos de efectivo, donde el primer elemento
                          es típicamente negativo (inversión inicial)
        iterations (int): Número máximo de iteraciones (default: 100)
    
    Returns:
        float: Tasa interna de retorno
    
    Raises:
        ValueError: Si los parámetros son inválidos
    """
    if not cash_flows:
        raise ValueError("Los flujos de efectivo no pueden estar vacíos")
    if len(cash_flows) < 2:
        raise ValueError("Se necesitan al menos 2 flujos de efectivo")
    if iterations <= 0:
        raise ValueError("El número de iteraciones debe ser mayor a cero")
    if not isinstance(iterations, int):
        raise ValueError("Las iteraciones deben ser un número entero")
    
    # Verificar que haya al menos un flujo positivo y uno negativo
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    
    if not (has_positive and has_negative):
        raise ValueError("Debe haber al menos un flujo positivo y uno negativo")
    
    # Método de Newton-Raphson
    rate = 0.1  # Tasa inicial de 10%
    epsilon = 1e-6  # Tolerancia
    
    for _ in range(iterations):
        # Calcular NPV (Valor Presente Neto)
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
        
        # Calcular derivada del NPV
        dnpv = sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows))
        
        # Evitar división por cero
        if abs(dnpv) < epsilon:
            break
        
        # Actualizar tasa
        new_rate = rate - npv / dnpv
        
        # Verificar convergencia
        if abs(new_rate - rate) < epsilon:
            return new_rate
        
        rate = new_rate
    
    return rate
