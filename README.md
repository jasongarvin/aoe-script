# Simple Age of Empires 4 Script

A script that pulls data from the Age of Empires 4 API to retrieve ranked match results for a given player and graphs them.

Use it on [Replit](https://replit.com/@wearesilence/aoescript)!

## How It Works

Uses the API from [AoE World](htps://aoeworld.com) to retrieve match results by PLAYER_ID.

The PLAYER_ID gets passed to the rm_solo (ranked solo match) endpoint to retrieve recent match history, including match results, opponents, and rating changes.

The simple script then pulls only the player rating from the player whose ID matches PLAYER_ID and graphs it using matplotlib to display the change in player rating over time.
