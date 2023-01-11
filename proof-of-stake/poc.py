import random

"""
Dans cet exemple, je crée une classe Node qui représente un nœud dans le réseau, et elle a deux propriétés: enjeu et id.
Ensuite, je crée une classe PoS qui prend une liste de nœuds et implémente l'algorithme PoS.
Dans la fonction `select_validator`, je crée un pool de validateurs qui est rempli par chaque nœud, enjeu nombre de fois,
puis j'utilise la bibliothèque `random` en python pour choisir au hasard un validateur dans le pool.
Dans les dernières lignes du script, j'ai créé des instances de nœuds avec des enjeux différents, 
puis j'ai exécuté une boucle pour sélectionner au hasard un validateur dans le pool 10 fois, 
en imprimant l'identifiant du nœud sélectionné à chaque fois.

Veuillez noter qu'il s'agit d'un simple algorithme PoS pour démontrer son fonctionnement, et qu'il n'est pas sécurisé 
pour une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou protection supplémentaire. 
Vous devriez envisager des alternatives plus sûres pour implémenter l'algorithme PoS dans vos projets.
"""

class Node:
    def __init__(self, stake, id):
        self.stake = stake
        self.id = id

class PoS:
    def __init__(self, nodes):
        self.nodes = nodes

    def select_validator(self):
        validator_pool = []
        for node in self.nodes:
            # Add the node to the validator pool 'stake' number of times
            for _ in range(node.stake):
                validator_pool.append(node)
        # Select a random node from the validator pool
        return random.choice(validator_pool)

# Example usage:
nodes = [Node(3, "A"), Node(2, "B"), Node(5, "C")]
pos = PoS(nodes)

for _ in range(10):
    print(pos.select_validator().id)