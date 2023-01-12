"""
Dans cet exemple, j'ai créé une classe PoA qui contient une liste d'autorités. Les autorités sont des personnes ou
des entités de confiance qui sont autorisées à valider les transactions et à créer de nouveaux blocs sur la blockchain.

Les autorités sont les nœuds qui peuvent diffuser la valeur et les validateurs sont les nœuds qui peuvent voter sur
la valeur. Cela nous permet de restreindre la capacité de diffuser et de voter à certains nœuds pré-approuvés,
comme c'est généralement le cas dans un algorithme PoA. De plus, nous avons ajouté une gestion des erreurs de base
pour garantir que seuls les autorités autorisées et les validateurs peuvent diffuser et voter, respectivement. La
méthode de diffusion envoie la valeur à toutes les autorités et la méthode de vote est utilisée pour mettre à jour
les valeurs reçues par une autorité. La méthode majority_agreement est utilisée pour s'assurer que la valeur convenue
par la majorité des autorités est utilisée, elle est calculée en comptant le nombre d'occurrences de chaque valeur.
Enfin, la méthode decide est utilisée pour renvoyer la valeur finale convenue par les autorités.

Veuillez noter qu'il s'agit d'un simple algorithme PoA pour démontrer son fonctionnement et qu'il n'est pas adapté à
une utilisation dans le monde réel, car il n'ajoute aucune mesure de sécurité ou protection supplémentaire. Il s'agit
également d'une version simplifiée pour la démonstration, dans le monde réel, l'algorithme PoA est plus complexe et
doit inclure des mécanismes de sécurité supplémentaires, tels que les signatures numériques, pour se protéger contre
les autorités byzantines et d'autres problèmes de réseau tels que la perte de messages, la réorganisation
et les retards.
"""


class PoA:
    def __init__(self, _authorities, _validators):
        self.values = None
        self.authorities = _authorities
        self.validators = _validators
        self.agreed_value = None

    def broadcast(self, authority, value):
        if authority in self.authorities:
            self.values = {node: value for node in self.validators}
        else:
            raise ValueError("Only authorized authorities can broadcast values.")

    def vote(self, validator, value):
        if validator in self.validators:
            self.values[validator] = value
        else:
            raise ValueError("Only authorized validators can vote.")

    def majority_agreement(self):
        """Check if a value has been agreed upon by a majority of validators"""
        value_count = {}
        for value in self.values.values():
            if value not in value_count:
                value_count[value] = 0
            value_count[value] += 1

        for value, count in value_count.items():
            if count > len(self.validators) / 2:
                self.agreed_value = value
                return True
        return False

    def decide(self):
        return self.agreed_value


# Example usage:
authorities = ["A", "B"]
validators = ["C", "D", "E"]
poa = PoA(authorities, validators)
poa.broadcast("A", "example value")
poa.vote("E", "wrong value")
poa.majority_agreement()
print(poa.decide())  # prints "example value"
