import pytest
import uuid
from datetime import datetime, timedelta

from models import Invoice, UrgencyLevel, BankRate
from backend.reasoning_engine import ReasoningEngine
from backend.foundry_iq import FoundryIQClient

@pytest.mark.asyncio
async def test_reasoning_engine_end_to_end():
    # Setup mock data for testing the engine
    invoices = [
        Invoice(
            id=str(uuid.uuid4()),
            supplier_name="Test Supplier 1",
            currency="USD",
            amount_usd=50000.0,
            deadline=datetime.now() + timedelta(days=5),
            description="High urgency invoice",
            urgency=UrgencyLevel.HIGH
        ),
        Invoice(
            id=str(uuid.uuid4()),
            supplier_name="Test Supplier 2",
            currency="USD",
            amount_usd=100000.0,
            deadline=datetime.now() + timedelta(days=15),
            description="Medium urgency invoice",
            urgency=UrgencyLevel.MEDIUM
        )
    ]
    
    rates = [
        BankRate(
            bank_name="Equity Bank",
            bank_code="EQT",
            buy_rate=133.50,
            sell_rate=134.80,
            spread=1.30,
            liquidity_indicator="HIGH",
            swift_fee=25.0,
            commission_pct=0.125,
            timestamp=datetime.now(),
            trend_7d=[133.0, 133.5, 133.2, 133.8, 134.0, 134.5, 134.8]
        ),
        BankRate(
            bank_name="Stanbic Bank",
            bank_code="STB",
            buy_rate=133.90,
            sell_rate=134.75,
            spread=0.85,
            liquidity_indicator="HIGH",
            swift_fee=30.0,
            commission_pct=0.10,
            timestamp=datetime.now(),
            trend_7d=[133.2, 133.6, 133.4, 133.9, 134.1, 134.4, 134.75]
        ),
        BankRate(
            bank_name="Co-operative Bank",
            bank_code="COOP",
            buy_rate=132.50,
            sell_rate=135.00,
            spread=2.50,
            liquidity_indicator="LOW",
            swift_fee=40.0,
            commission_pct=0.175,
            timestamp=datetime.now(),
            trend_7d=[132.0, 132.5, 132.8, 133.5, 134.0, 134.5, 135.0]
        )
    ]
    
    # Initialize Foundry IQ client (mock mode defaults)
    iq_client = FoundryIQClient()
    
    # Initialize Reasoning Engine
    engine = ReasoningEngine(invoices=invoices, rates=rates, iq_client=iq_client)
    
    # Run the engine
    report = await engine.run()
    
    # Assertions
    assert report is not None
    assert len(report.reasoning_steps) == 6, "Expected exactly 6 reasoning steps"
    assert len(report.recommendations) > 0, "Expected at least one recommendation"
    assert report.total_savings_kes > 0, "Expected some savings compared to worst-case"
    
    # Check that recommendations point to the best bank (Stanbic has tightest spread and lowest commission)
    # The scoring mechanism should definitely favor Stanbic
    recommended_banks = [rec.bank_name for rec in report.recommendations]
    assert "Stanbic Bank" in recommended_banks, f"Expected Stanbic to be recommended, got: {recommended_banks}"
    
    # Verify citations are present
    assert len(report.recommendations[0].citations) > 0, "Expected citations from Foundry IQ"
    
    # Verify the reasoning steps have correct structure
    step1 = report.reasoning_steps[0]
    assert step1.step_number == 1
    assert step1.title == "Invoice Analysis"
    
    step6 = report.reasoning_steps[5]
    assert step6.step_number == 6
    assert step6.title == "Report Generation"
