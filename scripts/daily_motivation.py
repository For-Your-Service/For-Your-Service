#!/usr/bin/env python3
"""
Daily Motivation Dashboard
For Your Service | 7 Eagle Group | Free Hall

Run this script daily to see your contribution stats and stay motivated!

Usage:
    python scripts/daily_motivation.py
"""

import subprocess
import datetime
from datetime import datetime, timedelta

def run_git_command(cmd):
    """Execute git command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/Workspace/Users/whall4.wh@gmail.com/For-Your-Service')
    return result.stdout.strip()

def get_today_commits():
    """Get commits from today"""
    today = datetime.now().strftime('%Y-%m-%d')
    cmd = f'git log --since="{today} 00:00" --author="whall4.wh@gmail.com" --oneline'
    return run_git_command(cmd).split('\n') if run_git_command(cmd) else []

def get_week_commits():
    """Get commits from this week"""
    cmd = 'git log --since="7 days ago" --author="whall4.wh@gmail.com" --oneline'
    return run_git_command(cmd).split('\n') if run_git_command(cmd) else []

def get_lines_today():
    """Get lines added/removed today"""
    today = datetime.now().strftime('%Y-%m-%d')
    cmd = f'git log --since="{today} 00:00" --author="whall4.wh@gmail.com" --numstat --pretty=format:""'
    result = run_git_command(cmd)
    if not result:
        return 0, 0
    
    added = 0
    removed = 0
    for line in result.split('\n'):
        if line.strip():
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                added += int(parts[0])
                removed += int(parts[1])
    return added, removed

def get_streak():
    """Calculate current commit streak (workdays only)"""
    cmd = 'git log --author="whall4.wh@gmail.com" --date=short --pretty=format:"%ad" --since="30 days ago"'
    dates = run_git_command(cmd).split('\n')
    if not dates or not dates[0]:
        return 0
    
    unique_dates = sorted(set(dates), reverse=True)
    streak = 0
    current_date = datetime.now().date()
    
    for date_str in unique_dates:
        if not date_str:
            continue
        commit_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if it's a workday (Monday-Friday)
        if commit_date.weekday() >= 5:  # Skip weekends
            continue
            
        if commit_date == current_date or (current_date - commit_date).days == 1:
            streak += 1
            current_date = commit_date
        elif (current_date - commit_date).days > 1:
            break
    
    return streak

def main():
    print("="*80)
    print("🎖️  DAILY MOTIVATION DASHBOARD - FOR YOUR SERVICE")
    print("    Free Hall | 7 Eagle Group | Helping Veterans Find Employment")
    print("="*80)
    
    # Today's stats
    today = datetime.now().strftime('%A, %B %d, %Y')
    print(f"\n📅 {today}")
    print("-" * 80)
    
    today_commits = get_today_commits()
    today_count = len([c for c in today_commits if c])
    
    added, removed = get_lines_today()
    net_lines = added - removed
    
    print(f"✅ Commits Today: {today_count}")
    print(f"📝 Lines Added: +{added:,}")
    print(f"🗑️  Lines Removed: -{removed:,}")
    print(f"📊 Net Change: {net_lines:+,}")
    
    # Recent commits
    if today_count > 0:
        print(f"\n📋 Today's Commits:")
        for i, commit in enumerate(today_commits[:5], 1):
            if commit:
                parts = commit.split(' ', 1)
                if len(parts) == 2:
                    print(f"   {i}. {parts[1][:70]}")
    
    # Weekly stats
    print(f"\n📊 This Week (Last 7 Days)")
    print("-" * 80)
    week_commits = get_week_commits()
    week_count = len([c for c in week_commits if c])
    print(f"Total Commits: {week_count}")
    print(f"Average per Day: {week_count / 7:.1f}")
    
    # Streak
    streak = get_streak()
    print(f"\n🔥 Current Streak")
    print("-" * 80)
    print(f"Consecutive Workdays: {streak} days")
    
    streak_emoji = "🔥" * min(streak, 10)
    print(f"Visual: {streak_emoji}")
    
    # Goals
    print(f"\n🎯 Daily Goals")
    print("-" * 80)
    goal_commits = 3
    goal_lines = 500
    
    commits_progress = min(100, (today_count / goal_commits) * 100)
    lines_progress = min(100, (added / goal_lines) * 100)
    
    print(f"Commits: {today_count}/{goal_commits} {'✅' if today_count >= goal_commits else '❌'}")
    print(f"Progress: [{'█' * int(commits_progress / 10)}{' ' * (10 - int(commits_progress / 10))}] {commits_progress:.0f}%")
    
    print(f"\nLines: {added:,}/{goal_lines:,} {'✅' if added >= goal_lines else '❌'}")
    print(f"Progress: [{'█' * int(lines_progress / 10)}{' ' * (10 - int(lines_progress / 10))}] {lines_progress:.0f}%")
    
    # Motivation message
    print(f"\n💪 Motivation")
    print("-" * 80)
    
    if today_count == 0:
        print("⚡ Time to make your first commit! Every line of code helps veterans.")
    elif today_count < 3:
        print("👍 Good start! Keep the momentum going.")
    elif today_count < 5:
        print("🌟 Excellent work! You're making great progress.")
    else:
        print("🚀 OUTSTANDING! You're crushing it today!")
    
    # Mission reminder
    print(f"\n🎖️  Mission Reminder")
    print("-" * 80)
    print("Every commit brings us closer to helping veterans find meaningful")
    print("employment. Your work through 7 Eagle Group makes a real difference.")
    
    # GitHub link
    print(f"\n🔗 View Your Contributions")
    print("-" * 80)
    print("GitHub Profile: https://github.com/whall4.wh")
    print("Repository: https://github.com/For-Your-Service/For-Your-Service")
    
    print("\n" + "="*80)
    print("Keep up the great work, Free! 🎖️")
    print("="*80)

if __name__ == "__main__":
    main()
