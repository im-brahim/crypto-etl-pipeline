# Learning Log — Crypto ETL Pipeline
> A personal journal of lessons learned while building 
> a production-style ETL pipeline.
> Each lesson includes: what went wrong, why it matters, 
> and the correct pattern.

---

# 📚 LESSONS

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
    logger.error(f"Failed to fetch rate: {e}")
```
**Rule to remember:** Always catch the most specific exception possible.
`exc_info=True` prints the full stack trace automatically.

---

### Lesson 2: Never commit `.env` or hardcode credentials
**What happened:** Committed `.env` by mistake and hardcoded 
passwords in `config.py`.

**Why it's dangerous:** Your credentials are visible to everyone
who opens your repo. Bots scan GitHub 24/7 for this.

**What I learned:**
```bash
# Step 1 — Check if .env was ever committed
git log --all --full-history -- .env

# Step 2 — Remove from tracking
git rm --cached .env

# Step 3 — Clean full history (use git-filter-repo, not filter-branch)
pip install git-filter-repo
git filter-repo --path .env --invert-paths --force
git remote add origin <your-repo-url>
git push origin --force --all
```
**Rule to remember:** Add `.env` to `.gitignore` BEFORE your 
first commit. Use `.env.example` to document required variables.

---

### Lesson 3: The `main()` pattern
**Why it matters:** Code at module level runs even after a failure.
Wrapping in `main()` lets you use `return` to exit cleanly.
It also makes your script importable without executing it.

**Before — dangerous:**
```python
# If this fails, the code below still runs and crashes with NameError
try:
    rate = get_rate(api_url)
except requests.exceptions.RequestException:
    logger.error("Failed", exc_info=True)
    spark.stop()

enriched_df = flattened_df.withColumn(...)  # ← crashes here
```

**After — professional:**
```python
def main():
    try:
        rate = get_rate(api_url)
    except requests.exceptions.RequestException:
        logger.error("Failed to fetch rate", exc_info=True)
        spark.stop()
        return  # ← exits cleanly, nothing else runs

if __name__ == "__main__":
    main()
```

---

### Lesson 4: `os.getenv()` — two patterns
```python
# Secrets — no default, fails loudly if missing:
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Non-secrets — safe default if .env not present:
SPARK_MASTER = os.getenv("SPARK_MASTER", "spark://master:7077")
```
**Rule to remember:** If a secret is missing, the app should 
crash immediately — not connect silently with wrong credentials.

---

### Lesson 5: Avoid recomputation in Spark
**Why it matters:** Every `count()` triggers a full data scan.
```python
# ❌ Scans data 3 times
if df.count() > 0:
    save(df)
    logger.info(f"{df.count()} rows saved")

# ✅ Scans data once
row_count = df.count()
if row_count > 0:
    save(df)
    logger.info(f"{row_count} rows saved")
```

---

# 🗂️ GIT REFERENCE

### Conventional Commits
```bash
feat:      new feature
fix:       bug fix
refactor:  code change that isn't a fix or feature
docs:      documentation only
chore:     maintenance tasks
security:  security fix

# Example:
git commit -m "feat: add data validation module"
```

### Branch Strategy

main  → production only, never commit directly here
dev   → daily work, merge to main when feature is complete

### Useful Commands
```bash
# History
git log --oneline -10
git log --oneline --graph --decorate -10
git show HEAD

# Branches
git checkout -b new-branch        # create and switch
git branch -d branch_name         # delete locally
git push origin --delete name     # delete from GitHub

# Stash (save work temporarily)
git stash push -u -m "description"
git stash pop                      # restore and delete stash
git stash apply                    # restore but keep stash

# Copy file from another branch
git restore --source=branch_name path/to/file

# Fix upstream tracking
git push --set-upstream origin dev

# Remove file from git tracking
git rm --cached filename
```

---

# 🔮 SESSION 2 — Pre-work Notes

### Data Quality Questions to Think About:
1. What if Bitcoin price comes back as `0.0`?
   → Need validation: reject prices outside realistic range

2. What if the same timestamp is inserted twice?
   → Database UNIQUE constraint on timestamp column
   → `compare_data.py` filters by max timestamp but 
      can't protect against race conditions

3. What if `rate_value` is `None`?
   → Spark stores `null` silently — no error, no warning
   → BTC_MAD and ETH_MAD become null, data is corrupted
   → Need null check before applying calculations