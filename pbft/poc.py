import hashlib
import random

"""
Dans cet exemple, j'ai créé une classe PBFTNode qui représente un nœud du réseau,

L'algorithme PBFT (Practical Byzantine Fault Tolerance), fonctionne sur la base de trois types de messages que les 
nœuds échangent afin de parvenir à un consensus sur une valeur:

-Requête : est un message envoyé par un client à une réplique PBFT pour initier une requête. Il comprend la commande 
du client et un numéro de séquence unique pour identifier la demande.
-Préparer : est un message envoyé par un réplica à tous les autres réplicas, indiquant qu'il a reçu la demande et 
qu'il se prépare à valider la demande. Ce message inclut l'ID du réplica, le numéro de séquence de la demande et la 
valeur que le réplica propose de valider.
-Commit: est un message envoyé par un réplica à tous les autres réplicas, indiquant qu'il a reçu suffisamment de 
messages de préparation et qu'il est prêt à valider la valeur proposée. Ce message inclut l'ID du réplica et le 
numéro de séquence de la demande.

Le message de demande est envoyé d'un client à un nœud, puis le nœud diffuse un message de préparation avec la valeur 
proposée, y compris son ID et un numéro de vue. Après cela, les autres nœuds enverront un message de validation avec 
leur ID au nœud d'origine.

L'algorithme PBFT garantit qu'un quorum de nœuds (au moins f + 1 où f est le nombre de nœuds défectueux) doit envoyer 
un message de préparation avec la même valeur et le même numéro de vue afin de s'engager sur cette valeur, 
garantissant que le consensus est atteint et le réseau est en mesure de parvenir à un accord sur une valeur proposée. 
De cette façon, le protocole PBFT garantit que même si certains nœuds sont défectueux, le réseau peut toujours 
parvenir à un consensus sur une valeur. Les messages de demande, de préparation et de validation fonctionnent 
ensemble pour garantir qu'un quorum de nœuds s'accorde sur la valeur proposée avant de s'y engager, ce qui contribue 
à garantir la cohérence et la fiabilité du système distribué.

Dans le code fourni, la méthode handle_request traite un message de requête, en mettant à jour la vue et la valeur du 
nœud qui a reçu la requête. La méthode handle_prepare traite un message de préparation et vérifie si un quorum de 
message de préparation avec la même vue et la même valeur a été reçu, si c'est le cas, elle affecte cette valeur 
comme celle qui sera validée. Et handle_commit traite le message de commit, si un quorum de messages de commit avec 
la même valeur a été reçu, le consensus est atteint et l'algorithme se termine.

Veuillez noter qu'il s'agit d'un simple algorithme PBFT pour démontrer son fonctionnement et qu'il n'est pas sécurisé 
pour une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou protection supplémentaire. De 
plus, c'est une version simplifiée pour la démonstration, dans une implémentation réelle, l'algorithme PBFT est plus 
complexe et comporte plus d'étapes"""


class Replica:
    def __init__(self, _id):
        self.id = f'node_id_{_id}'
        self.state = {}
        self.commits = {}
        self.view = 0
        self.network = None

    def receive_request(self, _request, seq_num):
        if self.id not in self.state:
            self.state[self.id] = {}
        self.broadcast_prepare(_request, seq_num, self.view)

    def broadcast_prepare(self, _request, seq_num, view):
        self.network.receive_prepare(self.id, _request, seq_num, view)

    def receive_prepare(self, sender_id, _request, seq_num, view):
        if sender_id not in self.state:
            self.state[sender_id] = {}
        if self.view != view:
            self.broadcast_view_change()
            return
        self.state[sender_id][seq_num] = {"request": _request, "view": view}
        self.check_prepare()

    def check_prepare(self):
        # check if a quorum of f + 1 nodes have sent the same request and view
        prepare_count = {}
        for sender in self.state.values():
            for seq_num, _replica in sender.items():
                if seq_num not in prepare_count:
                    prepare_count[seq_num] = {}
                _request = _replica["request"]
                view = _replica["view"]
                if (_request, view) not in prepare_count[seq_num]:
                    prepare_count[seq_num][(_request, view)] = 1
                else:
                    prepare_count[seq_num][(_request, view)] += 1

        for seq_num in prepare_count:
            for _request_view, _count in prepare_count[seq_num].items():
                if _count > self.network.f:
                    self.broadcast_commit(_request_view[0], seq_num, _request_view[1])
                    break

    def broadcast_commit(self, _request, seq_num, view):
        self.network.receive_commit(self.id, _request, seq_num, view)

    def receive_commit(self, sender_id, _request, seq_num, view):
        # only commit to request if from the same view
        if sender_id not in self.state:
            self.state[sender_id] = {}
        if seq_num not in self.state[sender_id]:
            self.state[sender_id][seq_num] = {}
            self.state[sender_id][seq_num]["view"] = self.view

        if seq_num in self.state[sender_id] and self.state[sender_id][seq_num]["view"] == view:
            self.execute_request(_request)
            del self.state[sender_id][seq_num]

    def broadcast_view_change(self):
        self.view += 1
        self.network.receive_view_change(self.id, self.view)

    def receive_view_change(self, sender_id, new_view):
        if self.view < new_view:
            self.view = new_view
            # reset the state and commits
            self.state = {}
            self.commits = {}

    def execute_request(self, _request):
        # simulate executing the request
        _result = hashlib.sha256(_request.encode()).hexdigest()
        self.commits[_request] = _result
        return _result


def finalize_request(_request, _hash, success):
    if success:
        print(f'Quorum reached for request: {_request} with hash: {_hash}')
    else:
        print(f'Quorum was not reached for request: {_request}')


class Network:
    def __init__(self, _f):
        self.replicas = []
        self.f = _f

    def add_replica(self, _replica):
        _replica.network = self
        self.replicas.append(_replica)

    def receive_request(self, _request, seq_num):
        replicas = random.sample(self.replicas, self.f + 1)
        for _replica in self.replicas:
            _replica.receive_request(_request, seq_num)

    def receive_prepare(self, sender_id, _request, seq_num, view):
        for _replica in self.replicas:
            _replica.receive_prepare(sender_id, _request, seq_num, view)

    def receive_commit(self, sender_id, _request, seq_num, view):
        for _replica in self.replicas:
            _replica.receive_commit(sender_id, _request, seq_num, view)

    def receive_view_change(self, sender_id, new_view):
        for _replica in self.replicas:
            _replica.receive_view_change(sender_id, new_view)

    def check_stalemate(self):
        """Check if there are no new messages for some time
        """
        """stalemate = False
        for _replica in self.replicas:
            if _replica.state:
                stalemate = False or stalemate
            else:
                stalemate = True or stalemate
        if stalemate:"""
        non_empty_replicas = list(filter(lambda r: r.state, self.replicas))
        if non_empty_replicas:
            random_replica = random.choice(non_empty_replicas)
            self.cast_view_change(random_replica)
        else:
            # Handle the case where all replicas have an empty state
            print("Network is broken.. sorry!")
            exit(127)

    def cast_view_change(self, sender):
        """Cast new view number to all replicas
        """
        sender.broadcast_view_change()

    def check_inactive_replicas(self):
        """
        Periodically check for replicas that have not received any requests
        """
        inactive_replicas = []
        for _replica in self.replicas:
            if not _replica.state:
                inactive_replicas.append(_replica)
        for _replica in inactive_replicas:
            self.replicas.remove(_replica)
            new_replica = Replica(len(self.replicas) + 1)
            self.add_replica(new_replica)
            print(f"Replacing inactive replica {_replica.id} with {new_replica.id}")

    def check_commit(self):
        # check if a quorum of f + 1 nodes have committed the same request
        commit_count = {}
        for _replica in self.replicas:
            for _request, _hash in _replica.commits.items():
                if _request not in commit_count:
                    commit_count[_request] = {}
                if _hash not in commit_count[_request]:
                    commit_count[_request][_hash] = 1
                else:
                    commit_count[_request][_hash] += 1

        request_quorum = {}
        for _request in commit_count:
            _requestQuorum = False
            for _hash, _count in commit_count[_request].items():
                if _count > (self.f + 1):
                    _requestQuorum = True
                    finalize_request(_request, _hash, True)
                    break
            if not _requestQuorum:
                finalize_request(_request, None, False)
            request_quorum[_request] = _requestQuorum

        return request_quorum


class Client:
    def __init__(self, _network):
        self.network = _network
        self.seq_num = 0

    def send_request(self, _request):
        self.seq_num += 1
        self.network.receive_request(_request, self.seq_num)


# create a network with 5 replicas and f = 2
f = 2
network = Network(f)

# add 4 replicas to the network
replica_ids = [1, 2, 3, 4, 5, 6]
for _id in replica_ids:
    replica = Replica(_id)
    network.add_replica(replica)

# create client
client = Client(network)


def print_states():
    global replica
    # Check the state of all replicas after the request has been executed
    result = {}
    for replica in network.replicas:
        result[replica.id] = (replica.state, replica.commits)
    print("State of replicas:")
    for replica_id, state_commit in result.items():
        print(f"Replica {replica_id}: {state_commit}")


for i in range(len(replica_ids)):
    request = f' request {i}'
    print("Client sends request:", request)
    client.send_request(request)

    # simulate faulty replicas
    faulty_replicas = random.sample(network.replicas, i)
    print("Faulty replicas:", [replica.id for replica in faulty_replicas])

    for replica in faulty_replicas:
        # if bool(random.getrandbits(1)):
        replica.state = {}  # Clear the state of the faulty replicas
        # else:
        replica.commits[request] = f'fake_hash'

    # Try to recover from the failure
    print_states()
    # Check if commit is reached
    network.check_commit()

    # network.check_stalemate()

    # Update the network replicas
    # network.check_inactive_replicas()

    print("###########################################################################################################")
