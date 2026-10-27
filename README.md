# Pump Reliability Dashboard - simple version

Finds anomalies in pump data, forecasts when each parameter will reach its alarm limit,
and explains the likely root cause and what to do. 

## Folders

```
pump_project/
├── .env                 your 3 secret keys (never share this file)
├── README.md            this file
│
├── supabase/            THE DATABASE
│   └── schema.sql       makes the "readings" table
│
├── backend/             PYTHON (the brain and the server)
│   ├── main.py          the server: lists what the frontend can ask for
│   ├── database.py      read / add / update / delete in Supabase
│   ├── settings.py      the pumps and the alarm limits  <- change these first
│   ├── fake_data.py     makes fake sensor readings
│   ├── seed.py          loads the first data into Supabase (run once)
│   ├── analysis.py      anomaly detection + time series forecast + status
│   ├── faults.py        the list of known faults (data only)
│   ├── rca.py           root cause analysis + insight sentences
│   ├── ai.py            asks the AI to write an insight
│   └── requirements.txt the libraries to install
│
└── frontend/            WHAT YOU SEE IN THE BROWSER
    ├── index.html       Dashboard page
    ├── manage.html      Manage readings page (create, read, update, delete)
    ├── style.css        colours and layout
    ├── api.js           talks to the backend + the pump drop-down
    ├── dashboard.js     the Dashboard page (calls the 3 files below)
    ├── pump-picture.js  draws the pump picture
    ├── charts.js        draws the 4 graphs
    ├── panels.js        tiles, cards, insight, root cause analysis
    └── manage.js        the Manage page
```

How the parts talk to each other:

    frontend (browser)  ->  backend (Python)  ->  Supabase (database)
                                   |
                                   +-> AI (OpenRouter)

## Setup (do these once)

1. **VS Code:** File > Open Folder > choose `pump_project`.

2. **Supabase (the database):**
   - Make a free project at supabase.com.
   - Open **SQL Editor** > **New query**, paste everything from `supabase/schema.sql`, click **Run**.
   - Open **Settings > API Keys**. Copy the **Project URL** and the **secret key** (starts with `sb_secret_`).

3. **Keys:** open `.env` and set `SUPABASE_URL`, `SUPABASE_KEY`, and `OPENROUTER_API_KEY`.
   Get an API key from OpenRouter. Keep the Supabase secret key and OpenRouter key out of the `frontend` folder.
   The default model is `openai/gpt-4o-mini`; optionally set `OPENROUTER_MODEL` in `.env` to another model slug available in your OpenRouter account.

4. **Install the libraries.** Open the terminal in VS Code (Ctrl + `) and run:

       cd backend
       pip install -r requirements.txt

5. **Load the first data (once):**

       python seed.py

   It adds 30 days of fake readings for each of the 4 pumps. Running it again deletes the old data first.

6. **Start the app:**

       python main.py

7. **Open** http://127.0.0.1:8000 in your browser.

Next time, you only need steps 6 and 7.

## Try it
- Pick a pump in the drop-down. P-102 is healthy. P-101 and P-104 have a bearing fault.
  P-103 has an impeller fault.
- Press **Ask AI** for a written insight.
- Open **Manage readings** to add, edit and delete readings.

## Make it your own

- Real alarm limits and pump names: `backend/settings.py`
- Your own faults, checks and actions: `backend/faults.py`
- Colours: the top of `frontend/style.css`

## If something goes wrong

- `ModuleNotFoundError`: run `pip install -r requirements.txt` again (inside the `backend` folder).
- `KeyError: 'SUPABASE_URL'`: the `.env` file is empty or in the wrong place. It must be in `pump_project`, next to `README.md`.
- Supabase says the key is invalid: run `pip install --upgrade supabase`.
- The AI box shows an error: check `OPENROUTER_API_KEY` in `.env`, then restart with `python main.py`.
- The AI request times out: check your internet connection and that your network allows requests to `openrouter.ai`.
- The graphs are empty: they need internet the first time the page opens (Chart.js).
- The Dashboard says "No readings": run `python seed.py`.
