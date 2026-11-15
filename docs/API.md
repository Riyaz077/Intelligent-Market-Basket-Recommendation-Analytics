# API

Start the service:
```bash
uvicorn api.main:app --reload
```

- `GET /health` — service status.
- `GET /summary` — transaction and product summary.
- `GET /rules?limit=20` — top association rules.
- `POST /recommend` — body: `{"basket":["Coffee","Milk"],"limit":5}`.

Interactive documentation is available at `/docs`.
