#!/bin/bash
# Fix Cloudflare Stream URLs by fetching correct playback subdomain

export CLOUDFLARE_API_TOKEN='vNBgUDi8KEBvgZFxC-HmFBgTYkmm2pbtkyovrLdT'
python3 update_channels_with_stream.py
