"""
Dans cet exemple, je crée une classe BFT qui prend une liste de nœuds et implémente l'algorithme BFT.

Le nombre de nœuds défectueux (nœuds pouvant agir de manière malveillante) que le système peut tolérer est donné par
la variable `f`, qui est calculée comme le nombre total de nœuds divisé par 3.

La méthode broadcast envoie la valeur à tous les nœuds, et `receive` est utilisée pour mettre à jour les valeurs
reçues par un nœud, elle va simuler un nœud défectueux en remplaçant la valeur reçue par un nœud spécifique par une
valeur erronée.

Ensuite, la méthode majority_agreement est utilisée pour s'assurer que la valeur convenue par la majorité des nœuds
est utilisée, elle est calculée en comptant le nombre d'occurrences de chaque valeur, si la majorité des nœuds ont la
même valeur, la variable de classe valeur_convenue est actualisé. Enfin, la méthode decide est utilisée pour renvoyer
la valeur finale convenue par les nœuds.

Veuillez noter qu'il s'agit d'un simple algorithme BFT pour démontrer son fonctionnement et qu'il ne convient pas à 
une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou protection supplémentaire.
De plus, en supposant que les nœuds enverront correctement les valeurs et les messages, dans le monde réel, vous devriez
envisager des alternatives plus sécurisées pour implémenter l'algorithme BFT dans vos projets, et vous devez 
également prendre en compte les problèmes de réseau tels que la perte de messages, la réorganisation et les retards.
"""


class BFT:
    def __init__(self, bft_nodes):
        self.values = None
        self.nodes = bft_nodes
        self.f = len(bft_nodes) // 3  # the number of faulty nodes the system can tolerate
        self.agreed_value = None

    def broadcast(self, value):
        # Send the value to all nodes
        self.values = {node: value for node in self.nodes}

    def receive(self, sender, value):
        self.values[sender] = value

    def majority_agreement(self):
        # Count the number of occurrences of each value
        value_count = {}
        for value in self.values.values():
            if value not in value_count:
                value_count[value] = 0
            value_count[value] += 1

        # Find the value that is agreed upon by a majority of the nodes
        for value, count in value_count.items():
            if count > len(self.nodes) - self.f:
                self.agreed_value = value
                return True
        return False

    def decide(self):
        return self.agreed_value


# Example usage:
nodes = ["A", "B", "C", "D", "E", "F"]
bft = BFT(nodes)
bft.broadcast("example value")
bft.receive("B", "wrong value")  # simulating a faulty node
# bft.receive("C", "wrong value")  # simulating a faulty node
# bft.receive("D", "wrong value")  # simulating a faulty node

bft.majority_agreement()
print(bft.decide())  # prints "example value"
