## Demo For Using Reddit's Praw Lib

For ease of use, can be invoked with a `launch.json' from VSCode with the following example config:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "args": [
        "--subreddit",
        "All",
        "--numsubmissions",
        "22",
        "--numcomments",
        "11"
      ]
    }
  ]
}
```

Provide a `config.ini` at the root dir, as follows:

```ini
[REDDIT]
client_secret = <your-secret>
client_id = <your-client-id>
user_agent = <your-user-agent>
```
