from discord import Interaction
from discord.app_commands import (AppCommandError, CommandInvokeError, TransformerError, 
                                  TranslationError, CheckFailure, NoPrivateMessage, 
                                  MissingRole, MissingAnyRole, MissingPermissions, 
                                  BotMissingPermissions, CommandOnCooldown, 
                                  CommandLimitReached, CommandAlreadyRegistered, 
                                  CommandSignatureMismatch, CommandNotFound, 
                                  MissingApplicationID, CommandSyncFailure)

from util.logger import logging, SHH_BOT 


logger = logging.getLogger(SHH_BOT)


async def on_command_errors(interaction: Interaction, error: AppCommandError):
    logger.warning(f"Command '{interaction.command.name.upper()}' raised an error: {error}")

    # if isinstance(error, NoPrivateMessage):
    #     await interaction.response.send_message(f"{interaction.user.mention} This command cannot be used in direct messages.", ephemeral=True)
    # elif isinstance(error, MissingRole):
    #     await interaction.response.send_message(f"{interaction.user.mention} You are missing the required role to use this command.", ephemeral=True)
    # elif isinstance(error, MissingAnyRole):
    #     await interaction.response.send_message(f"{interaction.user.mention} You need at least one of the required roles to use this command.", ephemeral=True)
    # elif isinstance(error, MissingPermissions):
    #     await interaction.response.send_message(f"{interaction.user.mention} You lack the necessary permissions to use this command.", ephemeral=True)
    # elif isinstance(error, BotMissingPermissions):
    #     await interaction.response.send_message(f"{interaction.user.mention} I lack the required permissions to execute this command.", ephemeral=True)
    # elif isinstance(error, CommandOnCooldown):
    #     await interaction.response.send_message(f"{interaction.user.mention} This command is on cooldown. Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    # elif isinstance(error, TransformerError):
    #     await interaction.response.send_message(f"{interaction.user.mention} Invalid input provided. Please check your arguments.", ephemeral=True)
    # elif isinstance(error, TranslationError):
    #     await interaction.response.send_message(f"{interaction.user.mention} There was an error translating the command.", ephemeral=True)
    # elif isinstance(error, CheckFailure):
    #     await interaction.response.send_message(f"{interaction.user.mention} You do not meet the requirements to use this command.", ephemeral=True)
    # elif isinstance(error, CommandLimitReached):
    #     await interaction.response.send_message(f"{interaction.user.mention} The command limit has been reached. Try again later.", ephemeral=True)
    # elif isinstance(error, CommandAlreadyRegistered):
    #     await interaction.response.send_message(f"{interaction.user.mention} This command is already registered.", ephemeral=True)
    # elif isinstance(error, CommandSignatureMismatch):
    #     await interaction.response.send_message(f"{interaction.user.mention} Incorrect command usage. Check the command's signature and try again.", ephemeral=True)
    # elif isinstance(error, CommandNotFound):
    #     await interaction.response.send_message(f"{interaction.user.mention} That command does not exist.", ephemeral=True)
    # elif isinstance(error, MissingApplicationID):
    #     await interaction.response.send_message(f"{interaction.user.mention} The bot's application ID is missing. Please contact an administrator.", ephemeral=True)
    # elif isinstance(error, CommandSyncFailure):
    #     await interaction.response.send_message(f"{interaction.user.mention} Failed to sync commands. Please try again later.", ephemeral=True)
    # elif isinstance(error, CommandInvokeError):
    #     await interaction.response.send_message(f"{interaction.user.mention} There was an internal error while processing your command.", ephemeral=True)
    # elif isinstance(error, discord.HTTPException):
    #     await interaction.response.send_message(f"{interaction.user.mention} An HTTP error occurred while processing your request.", ephemeral=True)
    # elif isinstance(error, AppCommandError):
    #     await interaction.response.send_message(f"{interaction.user.mention} An application command error occurred.", ephemeral=True)
    # elif isinstance(error, discord.DiscordException):
    #     await interaction.response.send_message(f"{interaction.user.mention} An unexpected Discord error occurred.", ephemeral=True)
    # else:
    #     await interaction.response.send_message(f"{interaction.user.mention} An unknown error occurred. Please try again later.", ephemeral=True)