import hashlib

"""
Dans cet exemple, je crée une classe PoW qui possède une méthode mine qui prend en entrée une certaine donnée et extrait un nonce (un nombre aléatoire) qui satisfait la condition PoW en hachant répétitivement la donnée concaténée avec le nonce.
La difficulté d'extraction est définie par le paramètre de difficulté, qui détermine combien de zéros initiaux le hachage doit avoir.

Dans cet exemple, je modifie progressivement la difficulté à 6, de sorte que le hachage doit avoir jusqu'à 6 zéros initiaux.
La méthode mine utilise sha256 comme fonction de hachage, mais d'autres algorithmes pourraient également être utilisés.
Dans les dernières lignes du script, j'ai créé une instance de PoW avec une difficulté changeant de nulle à 6 et ensuite j'appelle
la méthode mine avec une chaîne "données d'exemple" et il imprimera le numéro (nonce) qui satisfait la difficulté avec le temps requis pour l'opération.

Veuillez noter que ceci est un algorithme PoW simple pour démontrer son fonctionnement et qu'il n'est pas sécurisé pour une utilisation en production,
car il ne prend pas en compte des mesures de sécurité ou protection supplémentaires.
"""
class PoW:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def mine(self, data):
        target = "0" * self.difficulty
        nonce = 0
        while True:
            # Create the hash of the data and the nonce
            h = hashlib.sha256()
            h.update(f"{data}{nonce}".encode())
            digest = h.hexdigest()
            if digest[:self.difficulty] == target:
                return nonce
            nonce += 1


# Example usage:
import time

data = "données d'exemple"
for i in range(7):
    pow = PoW(i)

    st = time.process_time_ns()
    print(pow.mine(data))
    et = time.process_time_ns()

    # get execution time
    res = et - st
    print('CPU Execution time:', res, 'nanoseconds', 'to mine with a difficulty of', i)
