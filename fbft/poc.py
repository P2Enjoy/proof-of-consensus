"""
Dans cet exemple, je crée une classe FBA qui contient une liste de nœuds et un entier f qui représente le nombre 
maximum de nœuds défectueux que le système peut tolérer. Il divise ensuite les nœuds en quorums, chaque quorum 
contient f+1 nœuds. La méthode de diffusion envoie la valeur à tous les nœuds, et le vote est utilisé pour mettre à 
jour les valeurs reçues par un nœud

La méthode majority_agreement est utilisée pour s'assurer que la valeur convenue par la majorité des nœuds dans 
chaque quorum est utilisée, cela se fait en comptant le nombre d'occurrences de chaque valeur pour chaque quorum, 
si la majorité des nœuds dans un quorum ont le même valeur, la variable de classe valeur_convenue est mise à jour.

Enfin, la méthode decide est utilisée pour renvoyer la valeur finale convenue par les nœuds.

Comme les autres algorithmes de consensus discutés, il s'agit d'un simple algorithme FBA pour démontrer comment cela 
fonctionne et il n'est pas adapté à une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou 
protection supplémentaire. En pratique, l'algorithme FBA peut être implémenté de différentes manières, selon le cas 
d'utilisation, et doit inclure des mécanismes de sécurité supplémentaires, tels que des signatures numériques, 
pour se protéger contre les nœuds byzantins et d'autres problèmes de réseau tels que la perte de messages, 
la réorganisation et retards. Il est également important de noter que cet exemple n'est pas censé être un code prêt 
pour la production et qu'une analyse plus approfondie est nécessaire pour s'assurer qu'il est sécurisé et efficace 
pour des cas d'utilisation pratiques.
"""


class FBA:
    def __init__(self, nodes, f):
        self.values = None
        self.nodes = nodes
        self.f = f
        self.quorums = self.create_quorums()
        self.agreed_value = None

    def create_quorums(self):
        """Divide the nodes into quorums, each quorum contains f+1 nodes"""
        quorums = []
        for i in range(0, len(self.nodes), self.f + 1):
            quorums.append(self.nodes[i:i + self.f + 1])
        return quorums

    def broadcast(self, value):
        self.values = {node: value for node in self.nodes}

    def vote(self, node, value):
        self.values[node] = value

    def majority_agreement(self):
        """Check if a value has been agreed upon by a majority of nodes in each quorum"""
        for quorum in self.quorums:
            value_count = {}
            for node in quorum:
                if self.values[node] not in value_count:
                    value_count[self.values[node]] = 0
                value_count[self.values[node]] += 1
            for value, count in value_count.items():
                if count > self.f:
                    self.agreed_value = value
                    return True
        return False

    def decide(self):
        return self.agreed_value


# Example usage:
nodes = ["A", "B", "C", "D", "E", "F"]
fba = FBA(nodes, 2)
fba.broadcast("example value")
fba.vote("B", "wrong value")  # simulating a faulty node
fba.majority_agreement()
print(fba.decide())  # prints "example value"
