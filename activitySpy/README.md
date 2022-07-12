# activitySpy
Simple Discord bot that keeps a historical log of target's activity (game, music) on a channel. Requieres a bot token with the "presence intent" enabled.

Reads token, target user, target channel and admin (for sending commands, still TODO) on a settings.json in the same directory. Example:

```json
{
    "token": "secret_token",
    "userstospy": [11111, 22222],
    "channel": 00000,
    "admin": 98765
}
```

## Stuff planed
- [X] Use a JSON for settings
- [ ] \(Toggeable?) Update message when the same user changes activity 
- [ ] Allow custom timezones
- [ ] Allow reloading of .json file, via commands sent via DM by admin
