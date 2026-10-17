import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_to_dict():
    """Test converting a memento to a dictionary."""
    calculation = Calculation(
        operation="Addition",
        operand1=Decimal("3"),
        operand2=Decimal("4")
    )
    timestamp = datetime.datetime(2026, 1, 15, 12, 30, 0)

    memento = CalculatorMemento(
        history=[calculation],
        timestamp=timestamp
    )

    data = memento.to_dict()

    assert len(data["history"]) == 1
    assert data["history"][0]["operation"] == "Addition"
    assert data["timestamp"] == timestamp.isoformat()


def test_memento_from_dict():
    """Test restoring a memento from a dictionary."""
    timestamp = datetime.datetime(2026, 1, 15, 12, 30, 0)

    data = {
        "history": [
            {
                "operation": "Addition",
                "operand1": "3",
                "operand2": "4",
                "result": "7",
                "timestamp": timestamp.isoformat()
            }
        ],
        "timestamp": timestamp.isoformat()
    }

    memento = CalculatorMemento.from_dict(data)

    assert len(memento.history) == 1
    assert memento.history[0].operation == "Addition"
    assert memento.history[0].result == Decimal("7")
    assert memento.timestamp == timestamp