#ChatGPT
import csv, os, pyxel

class Save():
    def __init__(self, nom, score):
        self.DATA_FILE = "scores.csv"
        self.nom = nom
        self.score = score

    def save_score(self):

        file_exists = os.path.exists(self.DATA_FILE)

        with open(self.DATA_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["nom_joueur", "score"])

            writer.writerow([self.nom, self.score])


def load_leaderboard():
    leaderboard = []
    DATA_FILE = "scores.csv"
    try:
        with open(DATA_FILE, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                leaderboard.append({
                    "nom_joueur": row["nom_joueur"],
                    "score": int(row["score"])
                })
    except FileNotFoundError:
        return []
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard[:5]
    
def draw_leaderboard(game):
    leaderboard = load_leaderboard()
    pyxel.text(85, 20, "🏆 LEADERBOARD 🏆", 10)
    y = 40
    for i, entry in enumerate(leaderboard):
        pyxel.text(70, y, f"{i+1}. {entry['nom_joueur']} - {entry['score']}", 7)
        y += 10
    pyxel.text(70, y+10, "'A' to go back to the menu", 8)