"""The tests for WebOS TV automation triggers."""
from homeassistant.components import automation
from homeassistant.components.webostv import DOMAIN
from homeassistant.helpers.device_registry import async_get as get_dev_reg
from homeassistant.setup import async_setup_component

from . import ENTITY_ID, setup_webostv


async def test_webostv_turn_on_trigger_device_id(hass, calls, client):
    """Test for turn_on triggers by device_id firing."""
    await setup_webostv(hass, "fake-uuid")

    device_reg = get_dev_reg(hass)
    device = device_reg.async_get_device(identifiers={(DOMAIN, "fake-uuid")})

    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        "platform": "webostv.turn_on",
                        "device_id": device.id,
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {
                            "some": device.id,
                            "id": "{{ trigger.id }}",
                        },
                    },
                },
            ],
        },
    )

    await hass.services.async_call(
        "media_player",
        "turn_on",
        {"entity_id": ENTITY_ID},
        blocking=True,
    )

    await hass.async_block_till_done()
    assert len(calls) == 1
    assert calls[0].data["some"] == device.id
    assert calls[0].data["id"] == 0


async def test_webostv_turn_on_trigger_entity_id(hass, calls, client):
    """Test for turn_on triggers by entity_id firing."""
    await setup_webostv(hass, "fake-uuid")

    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        "platform": "webostv.turn_on",
                        "entity_id": ENTITY_ID,
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {
                            "some": ENTITY_ID,
                            "id": "{{ trigger.id }}",
                        },
                    },
                },
            ],
        },
    )

    await hass.services.async_call(
        "media_player",
        "turn_on",
        {"entity_id": ENTITY_ID},
        blocking=True,
    )

    await hass.async_block_till_done()
    assert len(calls) == 1
    assert calls[0].data["some"] == ENTITY_ID
    assert calls[0].data["id"] == 0


async def test_wrong_trigger_platform_type(hass, caplog, client):
    """Test wrong trigger platform type."""
    await setup_webostv(hass, "fake-uuid")

    await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        "platform": "webostv.wrong_type",
                        "entity_id": ENTITY_ID,
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {
                            "some": ENTITY_ID,
                            "id": "{{ trigger.id }}",
                        },
                    },
                },
            ],
        },
    )

    assert (
        "ValueError: Unknown webOS Smart TV trigger platform webostv.wrong_type"
        in caplog.text
    )
