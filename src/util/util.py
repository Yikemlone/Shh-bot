import discord
from util.logger import logging, SHH_BOT

logger = logging.getLogger(SHH_BOT)


def is_in_dm(interaction : discord.Interaction):
    return isinstance(interaction.channel, discord.DMChannel) or isinstance(interaction.channel, discord.GroupChannel)


def is_guild_owner(interaction : discord.Interaction):
    """Decorator to check if the command user is the server owner."""
    if interaction.user.id != interaction.guild.owner_id: return 
    return True


def user_has_role(interaction : discord.Interaction, role_name: str):
    """Checks if the user has the role."""
    for role in interaction.user.roles:
        if role.name.lower() == role_name.lower():
            return True
    return False


def is_moderator(user: discord.Member) -> bool:
    """Checks if the user has moderation permissions."""
    mod_perms = ["manage_messages", "kick_members", "ban_members", "administrator"]
    return any(getattr(user.guild_permissions, perm, False) for perm in mod_perms)


def has_mod_role(user: discord.Member, role_name: str = "Moderator") -> bool:
    """Checks if the user has a specific moderator role."""
    return any(role.name.lower() == role_name.lower() for role in user.roles)
