from github import Github, Auth
import config
import time
from datetime import datetime, timedelta

def verify_connection():
    """Verifica si el token es válido conectando con GitHub."""
    try:
        auth = Auth.Token(config.GITHUB_TOKEN)
        g = Github(auth=auth)
        user = g.get_user(config.GITHUB_USERNAME)
        print(f"Conexión exitosa! Obteniendo datos de: {user.login}")
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

def get_repository_stats():
    """Descarga los repositorios y sus estadísticas básicas."""
    auth = Auth.Token(config.GITHUB_TOKEN)
    g = Github(auth=auth)
    user = g.get_user(config.GITHUB_USERNAME)
    
    print(f"Descargando repositorios de {config.GITHUB_USERNAME}...")
    repos_data = []
    
    repos = user.get_repos(sort="updated", direction="desc")
    
    one_year_ago = datetime.now() - timedelta(days=365)
    
    for repo in repos:
        total_commits = 0
        try:
             # METODO LENTO PERO EXACTO: Contar commits uno por uno
             # get_stats_participation() tiene caché y lag. get_commits() es real-time.
             commits = repo.get_commits(author=config.GITHUB_USERNAME, since=one_year_ago)
             total_commits = commits.totalCount
        except Exception as e:
             print(f"Warn: Error obteniendo commits reales de {repo.name}: {e}")
             total_commits = 0
             
        stats = {
            "name": repo.name,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "last_update": repo.updated_at,
            "weekly_commits": [], # Ya no usamos buckets semanales para la velocidad
            "total_commits": total_commits
        }
        
        # Solo incluir repos con algo de actividad en el año o muchas estrellas
        if stats["total_commits"] == 0 and stats["stars"] < 5:
             continue
             
        repos_data.append(stats)
        print(f" -> Encontrado: {repo.name} ({stats['language']}) - Commits año (Real-Time): {stats['total_commits']}")
        
        if len(repos_data) >= 20: 
            break
            
    return repos_data

if __name__ == "__main__":
    if verify_connection():
        stats = get_repository_stats()
        print(f"Total repos cargados: {len(stats)}")
