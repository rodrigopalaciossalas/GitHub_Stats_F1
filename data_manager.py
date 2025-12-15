from github import Github, Auth
import config

def verify_connection():
    """Verifica si el token es válido conectando con GitHub."""
    try:
        auth = Auth.Token(config.GITHUB_TOKEN)
        g = Github(auth=auth)
        user = g.get_user()
        print(f"Conexión exitosa! Autenticado como: {user.login}")
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
    
    # Ordenar por fecha de actualización para coger los más activos "Coches líderes"
    repos = user.get_repos(sort="updated", direction="desc")
    
    for repo in repos:
        # Obtener stats de participación semanal (último año)
        try:
             participation = repo.get_stats_participation()
             # 'owner' son los commits del dueño, 'all' de todos. Usamos del dueño.
             # get_stats_participation a veces devuelve None si github está calculando
             weekly_commits = participation.owner if participation else [0]*52
        except Exception:
             weekly_commits = [0]*52
             
        stats = {
            "name": repo.name,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "last_update": repo.updated_at,
            "weekly_commits": weekly_commits, 
            "total_commits": sum(weekly_commits)
        }
        
        # Solo incluir repos con algo de actividad en el año o muchas estrellas
        if stats["total_commits"] == 0 and stats["stars"] < 5:
             continue
             
        repos_data.append(stats)
        print(f" -> Encontrado: {repo.name} ({stats['language']}) - Commits año: {stats['total_commits']}")
        
        if len(repos_data) >= 20: 
            break
            
    return repos_data

if __name__ == "__main__":
    if verify_connection():
        stats = get_repository_stats()
        print(f"Total repos cargados: {len(stats)}")
