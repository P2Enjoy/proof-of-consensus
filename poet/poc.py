import random
import hashlib
import hmac
import concurrent.futures

"""
Ce code est une implémentation simplifiée d'un système de preuve de temps écoulé (PoET) utilisant Intel SGX pour 
l'attestation. Il utilise un algorithme de consensus distribué pour permettre un processus électoral équitable basé 
sur la loterie.

La classe PoET prend en entrée une liste de nœuds et une clé secrète, qui seront utilisées pour vérifier les 
signatures des nœuds. La méthode `verify_node` vérifie la signature d'un nœud en utilisant l'algorithme HMAC. La 
méthode `get_winner` utilise un pool de threads pour vérifier les signatures de chaque nœud et pour sélectionner celui 
qui a pris le plus de temps à répondre, en utilisant la fonction wait_time.

La méthode `decide` utilise la propriété get_winner pour déterminer le nœud gagnant et pour définir la valeur acceptée 
par le réseau. Il est important de noter que cette implémentation n'est qu'une démonstration simplifiée de 
l'algorithme PoET et qu'elle n'est pas sécurisée pour une utilisation dans le monde réel. 
Il faut utiliser des  alternatives plus sécurisées pour implémenter PoET dans des projets réels.
"""


def verify_node_sgx(node):
    """Pseudo-verification of the node using Intel SGX"""
    # In a real implementation, this would involve securely
    # attesting to the node's identity and integrity
    # using the SGX platform.
    return True


def wait_time():
    """Return a random waiting time between 0 and 10 seconds"""
    return random.random() * 10


class PoET:
    def __init__(self, _nodes, _key):
        self.values = None
        self.nodes = _nodes
        self.agreed_value = None
        self.key = _key

    def verify_node(self, _node):
        """Verify a node's signature using HMAC"""
        (_nodeValue, _nodeSignature) = (self.values[_node][0], self.values[_node][1])
        if not verify_node_sgx(_node):
            raise Exception("Node failed SGX attestation")
        h = hmac.new(self.key, (_node + ":" + _nodeValue).encode('utf-8'), hashlib.sha256)
        return hmac.compare_digest(h.hexdigest(), _nodeSignature)

    @property
    def get_winner(self):
        """Return the node that waited the longest and has a valid signature"""
        winner = None
        max_time = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = {executor.submit(self.verify_node, _node): _node for _node in self.nodes}
            for future in concurrent.futures.as_completed(results):
                _node = results[future]
                if future.result():
                    _wait_time = executor.submit(wait_time).result()
                    if _wait_time > max_time:
                        max_time = _wait_time
                        winner = _node
        if winner is None:
            raise Exception("No valid node signatures found")
        return winner

    def decide(self, _values):
        self.values = _values
        winner = self.get_winner
        self.agreed_value, _signature = self.values[winner]
        return self.agreed_value


# Example usage:
nodes = ["A", "B", "C"]
key = b"secret_key"
poet = PoET(nodes, key)

# Each node signs the value they're broadcasting
values = {}
for node in nodes:
    value = "example value"
    values[node] = (value, hmac.new(key, (node + ":" + value).encode('utf-8'), hashlib.sha256).hexdigest())

print(poet.decide(values))
