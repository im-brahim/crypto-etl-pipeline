# Learning Log — Crypto ETL Pipeline
## Session 1 — April 9, 2026

### Lesson 1: Never use bare `except:`
**What I had:**
```python
except:
    logger.info("Can't fetch rate")
```
**Why it's dangerous:** Catches everything including memory errors and 
keyboard interrupts. You can never know what actually failed.

**What I learned:**

```python
# Use this when you need to log the full traceback:
except requests.exceptions.RequestException:
    logger.error("Failed to fetch rate", exc_info=True)

# Use this when you want to include the error in a custom message:
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to fetch rate {e}")

```
**Rule to remember:** Always catch the most specific exception possible.
`exc_info=True` prints the full stack trace automatically.

---
### Lesson 2: Never push .env file or hardcoder (passwords ...) to public repo in your github

**what i had:** I commit by mistake the .env file and i unclude some hardcode also in config.py file 

**Why it's dangerous:** your credential and passwords for database and acount will be visisble by any one open your repo.

**What I learned:**
***Step 1:*** I checked the history commits for the .env : 

```bash
git log --all --full-history -- .env
```
If it returns nothing — you're safe. If it returns commits we move to step 2.

***Step 2:*** Remove .env from git tracking
```bash
git rm --cached .env
```

***Step 3:***
Even after removal, the old commits still contain your passwords. Run this:
```bash
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch .env" \
--prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

### Lesson 3: I learn new proffesionel pattern *main()*
**what is it:** First i use the logic inside the process_data.py inside main() 

**Before**
```python
try:
    exch_api = os.getenv("EXCHANGE_API_URL")
    rate = get_rate(exch_api)
    rate_date = rate["datetime"][:10]
    rate_value = rate["rate"]
except requests.exceptions.RequestException as e:
    logger.error("Can't Fetch Rate", exc_info=True)
    spark.stop()

# THIS LINE RUNS EVEN IF THE TRY BLOCK FAILED:
enriched_df = flattened_df.withColumn(...)
```

**Solution:**
The fix is to add a sys.exit() after spark.stop(), or better — wrap the whole flow in a main() function and use return.

**After:**
```python
def main():
    logger = get_logger("Process Data")
    spark = create_spark_session("Extract and Process Crypto Data")
    
    try:
        exch_api = os.getenv("EXCHANGE_API_URL", EXCHANGE_API_URL)
        rate = get_rate(exch_api)
        rate_date = rate["datetime"][:10]
        rate_value = rate["rate"]
    except requests.exceptions.RequestException:
        logger.error("Failed to fetch exchange rate", exc_info=True)
        spark.stop()
        return          # ← exits main() cleanly, nothing else runs
    
    # ... rest of your code ...

if __name__ == "__main__":
    main()
```


### Lesson 4: Conventional commits

***Types:***
*feat:*     a new feature                               
*fix:*      a bug fix
*refactor:* code change that isn't a fix or feature
*docs:*     documentation only
*chore:*    maintenance tasks
*security:* security tips

***e.g:***
```bash
git commit -m "feat: add new feaure"
```

### Lesson 5: Branch Strategy
**Branches:**
***main***     → Production-ready code only
                Nobody commits directly here
                Only receives merges from dev when a feature is complete

***dev***      → Your active working branch
                This is where you code every day
                When a feature is done and tested → merge to main


### Lesson 6: os.getenv() — two patterns

```python
# Secrets — no default, fails loudly if missing:
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Non-secrets — safe default if .env not present:
SPARK_MASTER = os.getenv("SPARK_MASTER", "spark://master:7077")
```

**Rule to remember:** Secrets should never have defaults in code.
If the password is missing, the app should fail immediately 
and loudly — not connect with an empty password silently.