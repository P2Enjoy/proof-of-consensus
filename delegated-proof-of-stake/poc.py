import random

"""
Dans cet exemple, je crée une classe Node qui représente un nœud dans le réseau, elle a des propriétés d'enjeu, d'id et
de votes.  Ensuite, je crée une classe DPoS qui prend une liste de nœuds et implémente l'algorithme DPoS.
Tout d'abord, la méthode vote_validators est utilisée, où chaque nœud vote pour qu'un autre nœud devienne un validateur.
Dans la méthode select_validators, les nœuds sont triés en fonction de leurs votes, puis le tiers supérieur du réseau
sera sélectionné comme validateurs.
Enfin, la méthode create_block choisira au hasard un validateur parmi les validateurs sélectionnés pour créer un nouveau
bloc et l'ajouter à la chaîne, dans ce cas, il imprimera l'identifiant du validateur et les données qui ont été incluses
dans le bloc

Veuillez noter qu'il s'agit d'un simple algorithme DPoS pour démontrer son fonctionnement, et qu'il n'est pas sécurisé
pour une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou protection supplémentaire.
De plus, la méthode de sélection d'un validateur à l'aide de la bibliothèque aléatoire n'est pas sécurisée et ne
garantit pas l'équité du réseau. Vous devriez envisager des alternatives plus sécurisées pour implémenter l'algorithme
DPoS dans vos projets.
"""


class Node:
    def __init__(self, stake, id):
        self.stake = stake
        self.id = id
        self.votes = 0

    def vote(self, node):
        node.votes += self.stake


class DPoS:
    def __init__(self, nodes):
        self.nodes = nodes
        self.validators = []

    def vote_validators(self):
        for node in self.nodes:
            # Each node votes for another node to become a validator
            node.vote(random.choice(self.nodes))

    def select_validators(self):
        # Sort nodes by number of votes
        self.nodes.sort(key=lambda x: x.votes, reverse=True)
        # Select the top `num_validators` nodes as validators
        num_validators = len(self.nodes) // 3  # one third of the network
        self.validators = self.nodes[:num_validators]

    def create_block(self, data):
        # Select a random validator to create a new block
        validator = random.choice(self.validators)
        block = {"validator": validator.id, "data": data}
        return block


# Example usage:
nodes = [Node(3, "A"), Node(2, "B"), Node(5, "C"), Node(8, "D"), Node(1, "E")]
dpos = DPoS(nodes)
dpos.vote_validators()
dpos.select_validators()
print("Validators:")
for validator in dpos.validators:
    print(validator.id)
print("Block:")
print(dpos.create_block("example data"))
