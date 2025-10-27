# Git Workflow Guide for SellerSuite

## Quick Commands

### 1. Check what files changed
```bash
git status
```

### 2. Stage all changes
```bash
git add .
```

### 3. Commit with message
```bash
git commit -m "Your descriptive message"
```

### 4. Push to GitHub
```bash
git push
```

## Complete Workflow Example

### Example 1: You edited the backend code
```bash
# 1. Check what changed
git status

# 2. Stage all changes
git add .

# 3. Commit
git commit -m "Add Flipkart support for B2CS reports"

# 4. Push to GitHub
git push
```

### Example 2: You modified multiple files
```bash
git status                              # See what changed
git add .                               # Stage everything
git commit -m "Update UI and add new feature"
git push                                # Push to GitHub
```

## Committing Specific Files Only

### If you only want to commit certain files:
```bash
# Stage specific files
git add backend/app.py
git add frontend/src/components/Dashboard.js

# Commit them
git commit -m "Update backend logic and dashboard UI"

# Push
git push
```

## Best Practices

### ✅ Good Commit Messages
```bash
git commit -m "Add GSTIN validation"
git commit -m "Fix B2B report parsing error"
git commit -m "Update documentation for new features"
git commit -m "Improve error messages for file upload"
```

### ❌ Bad Commit Messages (avoid these)
```bash
git commit -m "changes"
git commit -m "update"
git commit -m "fix"
```

## Common Situations

### Situation 1: You made changes and want to save them
```bash
git add .
git commit -m "Your descriptive message"
git push
```

### Situation 2: You want to see what changed
```bash
git status              # See list of changed files
git diff                # See actual code changes
```

### Situation 3: You made a mistake in last commit
```bash
git add .
git commit --amend -m "Corrected message"
git push --force
```

### Situation 4: Someone else made changes on GitHub
```bash
git pull               # Get latest changes first
git add .
git commit -m "Your message"
git push
```

## Daily Workflow

**Morning:**
```bash
git pull              # Get any updates from GitHub
```

**During work:**
- Make your changes
- Test your code

**End of day / Feature complete:**
```bash
git status            # Review what changed
git add .             # Stage changes
git commit -m "Completed feature X"   # Commit
git push              # Push to GitHub
```

## Quick Reference Card

| Task | Command |
|------|---------|
| See what changed | `git status` |
| Stage all changes | `git add .` |
| Commit | `git commit -m "message"` |
| Push to GitHub | `git push` |
| Get latest code | `git pull` |
| See recent commits | `git log --oneline` |

## Troubleshooting

### "Your branch is behind origin/main"
```bash
git pull              # Get latest changes
git push              # Then push yours
```

### "Nothing to commit"
- Either you haven't saved your files, OR
- You already committed everything

### "Please tell me who you are"
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Want to undo changes (before committing)
```bash
git restore filename.js        # Undo changes to specific file
git restore .                  # Undo ALL uncommitted changes
```

### Want to undo a commit (before pushing)
```bash
git reset --soft HEAD~1        # Undo last commit, keep changes
```

---

**Remember**: Commit often with clear messages! Your future self will thank you. 😊
