"""Hooking into the auth system"""

from allianceauth import hooks

from . import app_settings


@hooks.register("discord_cogs_hook")
def register_cogs():
    """
    Registering our discord cogs
    """

    return [
        "asmek_authcogs.cogs.about",
        "asmek_authcogs.cogs.auth",
        "asmek_authcogs.cogs.links",
        "asmek_authcogs.cogs.siege",
        "asmek_authcogs.cogs.hr",
    ]
