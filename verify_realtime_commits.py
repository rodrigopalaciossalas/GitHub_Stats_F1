from github import Github, Auth
import config
from datetime import datetime, timedelta

def check_realtime_commits():
    auth = Auth.Token(config.GITHUB_TOKEN)
    g = Github(auth=auth)
    user = g.get_user(config.GITHUB_USERNAME)
    
    print(f"Checking real-time commits for user: {config.GITHUB_USERNAME}")
    
    # Check top 5 repos
    repos = user.get_repos(sort="updated", direction="desc")
    
    count = 0
    one_year_ago = datetime.now() - timedelta(days=365)
    
    for repo in repos:
        if count >= 5: break
        count += 1
        
        print(f"\nAnalyzing: {repo.name}")
        
        # 1. Fast Method (Stats)
        try:
            stats = repo.get_stats_participation()
            fast_count = sum(stats.owner) if stats else 0
        except:
            fast_count = 0
            
        # 2. Slow Method (Real-time Iteration)
        real_count = 0
        try:
            # Fetch commits authored by the user in the last year
            commits = repo.get_commits(author=config.GITHUB_USERNAME, since=one_year_ago)
            real_count = commits.totalCount
        except Exception as e:
            print(f"Error counting real commits: {e}")
            
        print(f"  -> Cached Stats API: {fast_count}")
        print(f"  -> Real-time Count:  {real_count}")
        
        if real_count > fast_count:
            print(f"  !!! DISCREPANCY FOUND: {real_count - fast_count} missing commits in stats.")

if __name__ == "__main__":
    check_realtime_commits()
