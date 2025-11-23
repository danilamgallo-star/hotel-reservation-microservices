"""
Test suite para el módulo finance.py
Cobertura completa de funciones financieras
"""

import pytest
from finance import (
    calculate_compound_interest,
    calculate_annuity_payment,
    calculate_internal_rate_of_return
)


# ============================================================================
# Tests para calculate_compound_interest
# ============================================================================

def test_compound_interest_basic():
    """Caso básico: $1000 al 5% anual por 10 años"""
    result = calculate_compound_interest(1000, 0.05, 10)
    assert abs(result - 1628.89) < 0.01


def test_compound_interest_zero_periods():
    """Caso límite: cero períodos devuelve el principal"""
    result = calculate_compound_interest(1000, 0.05, 0)
    assert result == 1000


def test_compound_interest_zero_rate():
    """Caso límite: tasa cero devuelve el principal"""
    result = calculate_compound_interest(1000, 0, 10)
    assert result == 1000


def test_compound_interest_high_rate():
    """Caso extremo: tasa muy alta (100%)"""
    result = calculate_compound_interest(1000, 1.0, 5)
    assert result == 32000


def test_compound_interest_negative_principal():
    """Caso inválido: principal negativo debe lanzar error"""
    with pytest.raises(ValueError, match="capital principal no puede ser negativo"):
        calculate_compound_interest(-1000, 0.05, 10)


def test_compound_interest_negative_rate():
    """Caso inválido: tasa negativa debe lanzar error"""
    with pytest.raises(ValueError, match="tasa de interés no puede ser negativa"):
        calculate_compound_interest(1000, -0.05, 10)


def test_compound_interest_negative_periods():
    """Caso inválido: períodos negativos debe lanzar error"""
    with pytest.raises(ValueError, match="períodos no pueden ser negativos"):
        calculate_compound_interest(1000, 0.05, -10)


def test_compound_interest_non_integer_periods():
    """Caso inválido: períodos no enteros debe lanzar error"""
    with pytest.raises(ValueError, match="períodos deben ser un número entero"):
        calculate_compound_interest(1000, 0.05, 10.5)


# ============================================================================
# Tests para calculate_annuity_payment
# ============================================================================

def test_annuity_payment_basic():
    """Caso básico: préstamo de $10000 al 5% por 12 períodos"""
    result = calculate_annuity_payment(10000, 0.05, 12)
    assert abs(result - 1128.25) < 0.01


def test_annuity_payment_zero_rate():
    """Caso especial: tasa cero, el pago es principal/períodos"""
    result = calculate_annuity_payment(12000, 0, 12)
    assert result == 1000


def test_annuity_payment_single_period():
    """Caso límite: un solo período"""
    result = calculate_annuity_payment(1000, 0.05, 1)
    assert abs(result - 1050) < 0.01


def test_annuity_payment_high_rate():
    """Caso extremo: tasa muy alta"""
    result = calculate_annuity_payment(10000, 0.5, 10)
    assert result > 5000  # Con tasa del 50%, el pago debe ser significativo


def test_annuity_payment_negative_principal():
    """Caso inválido: principal negativo"""
    with pytest.raises(ValueError, match="capital principal no puede ser negativo"):
        calculate_annuity_payment(-10000, 0.05, 12)


def test_annuity_payment_negative_rate():
    """Caso inválido: tasa negativa"""
    with pytest.raises(ValueError, match="tasa de interés no puede ser negativa"):
        calculate_annuity_payment(10000, -0.05, 12)


def test_annuity_payment_zero_periods():
    """Caso inválido: cero períodos"""
    with pytest.raises(ValueError, match="períodos deben ser mayores a cero"):
        calculate_annuity_payment(10000, 0.05, 0)


def test_annuity_payment_negative_periods():
    """Caso inválido: períodos negativos"""
    with pytest.raises(ValueError, match="períodos deben ser mayores a cero"):
        calculate_annuity_payment(10000, 0.05, -12)


def test_annuity_payment_non_integer_periods():
    """Caso inválido: períodos no enteros"""
    with pytest.raises(ValueError, match="períodos deben ser un número entero"):
        calculate_annuity_payment(10000, 0.05, 12.5)


# ============================================================================
# Tests para calculate_internal_rate_of_return
# ============================================================================

def test_irr_basic():
    """Caso básico: proyecto simple con inversión inicial y retornos"""
    cash_flows = [-1000, 300, 300, 300, 300, 300]
    result = calculate_internal_rate_of_return(cash_flows)
    assert 0.15 < result < 0.16  # TIR aproximadamente 15.24%


def test_irr_breakeven():
    """Caso de punto de equilibrio: TIR cercana a 0"""
    cash_flows = [-1000, 500, 500]
    result = calculate_internal_rate_of_return(cash_flows)
    assert abs(result) < 0.01


def test_irr_high_return():
    """Caso de alto retorno"""
    cash_flows = [-1000, 2000, 1000]
    result = calculate_internal_rate_of_return(cash_flows)
    assert result > 0.5  # TIR mayor al 50%


def test_irr_custom_iterations():
    """Verificar que acepta iteraciones personalizadas"""
    cash_flows = [-1000, 300, 300, 300, 300]
    result = calculate_internal_rate_of_return(cash_flows, iterations=50)
    assert result > 0


def test_irr_empty_cash_flows():
    """Caso inválido: lista vacía"""
    with pytest.raises(ValueError, match="flujos de efectivo no pueden estar vacíos"):
        calculate_internal_rate_of_return([])


def test_irr_single_cash_flow():
    """Caso inválido: solo un flujo"""
    with pytest.raises(ValueError, match="Se necesitan al menos 2 flujos de efectivo"):
        calculate_internal_rate_of_return([-1000])


def test_irr_all_positive():
    """Caso inválido: todos los flujos positivos"""
    with pytest.raises(ValueError, match="al menos un flujo positivo y uno negativo"):
        calculate_internal_rate_of_return([100, 200, 300])


def test_irr_all_negative():
    """Caso inválido: todos los flujos negativos"""
    with pytest.raises(ValueError, match="al menos un flujo positivo y uno negativo"):
        calculate_internal_rate_of_return([-100, -200, -300])


def test_irr_zero_iterations():
    """Caso inválido: cero iteraciones"""
    with pytest.raises(ValueError, match="número de iteraciones debe ser mayor a cero"):
        calculate_internal_rate_of_return([-1000, 500, 600], iterations=0)


def test_irr_negative_iterations():
    """Caso inválido: iteraciones negativas"""
    with pytest.raises(ValueError, match="número de iteraciones debe ser mayor a cero"):
        calculate_internal_rate_of_return([-1000, 500, 600], iterations=-10)


def test_irr_non_integer_iterations():
    """Caso inválido: iteraciones no enteras"""
    with pytest.raises(ValueError, match="iteraciones deben ser un número entero"):
        calculate_internal_rate_of_return([-1000, 500, 600], iterations=10.5)


# ============================================================================
# Test adicional de integración
# ============================================================================

def test_integration_loan_scenario():
    """
    Escenario integrado: Calcular el retorno de un préstamo
    usando compound interest y annuity payment
    """
    principal = 10000
    rate = 0.06
    periods = 24
    
    # Calcular pago de anualidad
    payment = calculate_annuity_payment(principal, rate, periods)
    
    # Verificar que el pago sea razonable
    assert payment > 0
    assert payment * periods > principal  # Total pagado debe ser mayor al principal
    
    # Calcular el monto final con interés compuesto
    final_amount = calculate_compound_interest(principal, rate, periods)
    
    # Verificar crecimiento
    assert final_amount > principal
