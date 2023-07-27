from os import listdir, mkdir
from pyrogram import Client
from STAR import config
from STAR.tgcalls.queues import clear, get, is_empty, put, task_done
from STAR.tgcalls import queues
from STAR.tgcalls.youtube import download
from STAR.tgcalls.calls import run, pytgcalls
from STAR.tgcalls.calls import client

if "raw_files" not in listdir():
    mkdir("raw_files")

from STAR.tgcalls.convert import convert
