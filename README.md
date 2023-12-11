# Tournament setup using siilicams



my path for the gsi is at

`D:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\cfg\gamestate_integration`

spectator setup
```
"Dota 2 GSI Configuration"
"Dota 2 GSI Configuration"
{
    "uri" "http://127.0.0.1:6043/spectator"
    "timeout" "5.0"
    "buffer"  "0.1"
    "throttle" "0.1"
    "heartbeat" "30.0"
    "data"
    {
        "hero"              "1"
	      "player"	          "1"
    }
}
```

pc setup

```
"Dota 2 GSI Configuration"
{
    "uri" "http://127.0.0.1:6043/spectator"
    "timeout" "5.0"
    "buffer"  "0.1"
    "throttle" "0.1"
    "heartbeat" "30.0"
    "data"
    {
        "hero"              "1"
        "player"              "1"
    }
}
```
where `x` is the pc id, for our setup it ranges from [0,9]