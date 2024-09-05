#!/bin/bash

# Aggiorna la lista dei pacchetti
echo "Aggiornamento lista dei pacchetti..."
# Installa pacchetti apt
echo "Installazione pacchetti apt..."
sudo apt install -y \
    git \
    python3-dev \
    build-essential \
    python3-tk

# Installa pacchetti pip
echo "Installazione pacchetti pip..."
pip install \
    supabase


echo "Installazione completata!"
