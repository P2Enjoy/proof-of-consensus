import random
import hashlib


"""
La classe FilecoinNode que j'ai fournie dans l'exemple, simule un nœud dans le réseau Filecoin. 
Chaque nœud dispose d'un espace de stockage limité (storage_space) et peut stocker des données (stored_data). 
Lorsqu'un utilisateur souhaite stocker des données sur un nœud, ils peuvent proposer de stocker les données à l'aide de 
la méthode propose_storage. Si le nœud dispose de suffisamment d'espace de stockage, il stocke les données et génère une 
preuve de stockage (storage_proof) qui est un hachage des données stockées à l'aide du sha256 algorithme. Cette 
preuve peut ensuite être diffusée sur le réseau pour valider la transaction.

Cette implémentation est similaire à la classe PoW dans l'exemple précédent, mais au lieu de trouver une preuve en 
répétant en hachant les données avec un nonce, il utilise le hachage des données stockées comme preuve de stockage, 
et il enregistre la preuve dans l'exemple de classe.

Il est important de noter qu'il ne s'agit que d'un exemple simple qui illustre l'idée de base derrière la preuve de 
stockage, et il peut ne pas être sécurisé ou efficace dans les applications du monde réel. En pratique, 
Filecoin utilise des mécanismes de stockage pour générer la preuve de stockage et il utilise également un système de 
récompense pour inciter les utilisateurs à efficacement stocker des données.
"""


class FilecoinNode:
    def __init__(self, _id):
        self.stored_data = {}
        self.id = _id
        self.storage_space = random.choice([10, 20, 50])
        self.challenges = {}

    def propose_storage(self, _data):
        """Propose to store data on the node"""
        # check if node has enough storage space
        data_size = len(_data)
        if sum(self.stored_data.values()) + data_size > self.storage_space:
            return False

        # store the data and generate storage proof
        data_hash = hashlib.sha256(_data.encode()).hexdigest()
        self.stored_data[data_hash] = data_size

        # generate a challenge for the stored data
        self.challenges[data_hash] = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()

        return data_hash

    def provide_storage_space(self):
        """Return the storage space available"""
        return self.storage_space

    def retrieve_data(self, data_hash):
        """Retrieve the data that was stored with the given hash"""
        if data_hash in self.stored_data:
            return self.stored_data[data_hash]
        return None

    def provide_challenge(self, data_hash):
        """Return the encrypted challenge for the stored data"""
        if data_hash in self.challenges:
            return hashlib.sha256((data_hash + self.challenges[data_hash]).encode()).hexdigest()
        return None

    def solve_challenge(self, data_hash, solution):
        """Verify that the challenge has been properly solved"""
        if data_hash in self.challenges:
            expected_solution = hashlib.sha256((data_hash + self.challenges[data_hash]).encode()).hexdigest()
            if solution == expected_solution:
                return True
        return False


nodes = [FilecoinNode(_) for _ in range(5)]

# simulate a transaction that needs to be stored
data = "Hello World"

# randomly select a node to propose the storage
selected_node = random.choice(nodes)
storage_proof = selected_node.propose_storage(data)

if storage_proof:
    print("Storage proposed and proof provided:", storage_proof)
    # simulate broadcast of the storage proof
    challenge = selected_node.provide_challenge(storage_proof)
    for node in nodes:
        if node.solve_challenge(storage_proof, challenge):
            print(f"Data found on node with {node.provide_storage_space()} of storage space ({node.id})")
            break
else:
    print(f"Not enough storage space on the selected node with {selected_node.provide_storage_space()} space")
