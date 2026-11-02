import pytest

@pytest.mark.parametrize(
    "bad_eid",
    [
        "BAD"
        "BAD123"
        "E1234567"
        "E123"
        "E141415151"
    ],
)

def test_invalid_equipment_id_returns_422(client, bad_eid):
    response = client.post(
        "/api/loans",
        json=loan_payload(eid=bad_eid),
    )
    assert response.status_code == 422

def loan_payload(
    eid = 1,
    borrower_name = "John",
    loan_days = 5,
    purpose = "Just Because",
):
    return {
        "equipment_id" : eid,
        "borrower_name": borrower_name,
        "loan_days" : loan_days,
        "purpose" : purpose
}

def test_create_loan_returns_201(client):
    response = client.post(
    "/api/loans",
    json=loan_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data ["borrower_name"] == "John"




