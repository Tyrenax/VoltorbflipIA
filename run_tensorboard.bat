@echo off

REM Naviguer vers le répertoire de ton environnement virtuel (env)
cd /d D:\voltorbflip\env

REM Activer l'environnement virtuel
call Scripts\activate

REM Revenir au répertoire du projet
cd /d D:\voltorbflip\ai_agent\ai_renforcement

REM Lancer TensorBoard
tensorboard --logdir=D:\voltorbflip\ai_agent\ai_renforcement\voltorb_tensorboard --reload_interval=1
