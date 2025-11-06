import pytest
from order_manager import Order   



@pytest.fixture
def sample_order():
    return Order(1, [
        {"name": "A", "price": 10, "quantity": 2},
        {"name": "B", "price": 5, "quantity": 4},
        {"name": "C", "price": 20, "quantity": 1},
    ])

@pytest.fixture
def empty_order():
    return Order(2, [])




def test_total_regular(sample_order):
    assert sample_order.total() == (10*2 + 5*4 + 20*1)

def test_total_empty(empty_order):
    assert empty_order.total() == 0

def test_total_extreme_values():
    order = Order(3, [{"name": "X", "price": 10**6, "quantity": 10**3}])
    assert order.total() == 10**9




def test_most_expensive_regular(sample_order):
    result = sample_order.most_expensive()
    assert result["name"] == "C"
    assert result["price"] == 20

def test_most_expensive_single_item():
    order = Order(4, [{"name": "Only", "price": 99, "quantity": 1}])
    assert order.most_expensive() == {"name": "Only", "price": 99, "quantity": 1}

def test_most_expensive_empty(empty_order):
    with pytest.raises(ValueError):
        empty_order.most_expensive()



@pytest.mark.parametrize("discount", [0, 10, 50, 100])
def test_apply_discount_valid(sample_order, discount):
    original_prices = [item["price"] for item in sample_order.items]
    sample_order.apply_discount(discount)
    for i, item in enumerate(sample_order.items):
        expected_price = original_prices[i] * (1 - discount / 100)
        assert item["price"] == pytest.approx(expected_price)


@pytest.mark.parametrize("invalid_discount", [-5, 101, 999])
def test_apply_discount_invalid(sample_order, invalid_discount):
    with pytest.raises(ValueError, match="Invalid discount"):
        sample_order.apply_discount(invalid_discount)


def test_apply_discount_on_empty(empty_order):
    empty_order.apply_discount(50)  
    assert empty_order.items == []



def test_repr_regular(sample_order):
    rep = repr(sample_order)
    assert f"<Order {sample_order.id}:" in rep
    assert "items>" in rep

def test_repr_empty(empty_order):
    assert repr(empty_order) == "<Order 2: 0 items>"



def test_multiple_operations_combined():
    items = [
        {"name": "item1", "price": 100, "quantity": 1},
        {"name": "item2", "price": 50, "quantity": 2},
    ]
    order = Order(10, items)
    assert order.total() == 200
    order.apply_discount(25)
    assert order.total() == pytest.approx(150)
    assert order.most_expensive()["name"] == "item1" 
    assert repr(order).startswith("<Order 10:")
