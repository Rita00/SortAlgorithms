import math
import copy
import timeit


class Word:
    def __init__(self, word, user_id):
        self.word = word  # Guarda palavra
        self.users = set()  # Guarda "lista" com id de utilizadores, sem repeticao
        self.users.add(user_id)  # Contador para todos os acessos
        self.counter = 1

    def __repr__(self):
        string = str(tuple([self.word, self.users, self.counter]))
        return string

    def __str__(self):
        string = str(tuple([self.word, self.users, self.counter]))
        return string

    def calculate(self):
        self.users = len(self.users)  # Faz a contagem de quantas vezes uma determinada palavra foi pesquisada

    def insert_user(self, user_id):
        self.users.add(user_id)
        self.counter += 1


class WordList(list):
    def __init__(self):
        super().__init__()

    def bubble_sort(self, key=lambda x: x.counter):
        for i in range(len(self) - 1):
            for j in range(len(self) - 1):
                if key(self[j]) < key(self[j + 1]):
                    self[j], self[j + 1] = self[j + 1], self[j]

    def merge_sort(self, left=0, right=None, key=lambda x: x.counter):
        if right is None:
            right = len(self) - 1
        if right != left:
            self.merge_sort(left, int((left + right) / 2), key)
            self.merge_sort(int((left + right) / 2) + 1, right, key)
            self.merge(left, right, key)

    def merge(self, left, right, key):
        array_l = [self[i] for i in range(left, int((left + right) / 2) + 1)]  # dividir array em dois
        array_r = [self[i] for i in range(int((left + right) / 2) + 1, right + 1)]

        i = j = 0
        while i < len(array_l) and j < len(array_r):
            if key(array_l[i]) > key(array_r[j]):
                self[left] = array_l[i]
                i += 1
            else:
                self[left] = array_r[j]
                j += 1
            left += 1

        while i < len(array_l):
            self[left] = array_l[i]
            i += 1
            left += 1

        while j < len(array_r):
            self[left] = array_r[j]
            j += 1
            left += 1

    def quick_sort(self, low=0, high=None, key=lambda x: x.counter):
        if high is None:
            high = len(self)
        if low < high:
            pivot = self.division(low, high, key)
            self.quick_sort(low, pivot, key)
            self.quick_sort(pivot + 1, high, key)

    def division(self, low, high, key=lambda x: x.counter):
        pivot = self[low]
        left = low
        for i in range((low + 1), high):
            if key(self[i]) > key(pivot):
                self[i], self[left] = self[left], self[i]
                left += 1
        return left

    def insertion_sort(self, key=lambda x: x.counter):
        for i in range(1, len(self)):  # Numero de iteraçoes necessarias para percorrer o array
            indice = self[i]  # indice a ser colocado na ordem certa
            indice_sort = i - 1  # ultimo indice ordenado
            while indice_sort >= 0:
                if key(indice) > key(self[indice_sort]):  # verifica se o anterior é menor, se sim
                    self[indice_sort + 1] = self[indice_sort]  # troca as posiçoes
                    self[indice_sort] = indice
                    indice_sort -= 1  # repete-se ate nao ser ou encontrar o 1º indice do array
                else:  # se não, termina o while e avança para o próximo elemento a ordenar
                    break

    def shell_sort(self, key=lambda x: x.counter):
        gap_size = int(len(self) / 2)  # espaçamento entre indices a comparar
        while gap_size > 0:
            current = gap_size  # Indice de valor a ordenar
            while current < len(self):  # Ordenar todos os indices
                value_sort = self[current]  # valor a ordenar
                ind_values_comp = current - gap_size  # Valores com quem o value_sort vai ser comparado
                while ind_values_comp >= 0 and key(value_sort) > key(self[ind_values_comp]):  # Se value_sort for maior
                    self[ind_values_comp + gap_size] = self[ind_values_comp]  # Faz troca de indices
                    ind_values_comp -= gap_size  # decrementa indice, para comparar próximo valor
                self[ind_values_comp + gap_size] = value_sort
                current += 1  # Proximo valor a ordenar
            gap_size = int(gap_size / 2)  # Reduz gap_size

    # Algoritmo de Mudança de base
    def counting_sort(self, key=lambda x: x.counter, maior_elem=None):
        if maior_elem is None:
            maior_elem = max(self, key=key)
            new_array = [0] * (key(maior_elem) + 1)
        else:
            new_array = [0] * (maior_elem + 1)

        sorted_array = [0] * (len(self))

        for indice in range(len(self)):
            new_array[key(self[indice])] += 1

        for indice in range(len(new_array) - 2, -1, -1):
            new_array[indice] = new_array[indice] + new_array[indice + 1]

        for i in range(len(self) - 1, -1, -1):
            new_array[key(self[i])] = new_array[key(self[i])] - 1
            sorted_array[new_array[key(self[i])]] = self[i]

        for i in range(len(self)):
            self[i] = sorted_array[i]

    def radix_sort(self, key=lambda x: x.counter):
        tam_max = key(max(self, key=key))
        tam_max = math.floor(math.log10(tam_max)) + 1
        for algarismo in range(tam_max):
            self.counting_sort(key=lambda x: (key(x) // (10 ** algarismo)) % 10, maior_elem=9)

    def insert_word(self, word, user_id):
        exists = False
        for p in self:
            if p.word == word:
                exists = True
                break
        if not exists:
            self.append(Word(word, user_id))
        else:
            p.insert_user(user_id)

    def calculate(self):
        soma_users = 0
        total = 0
        for p in self:
            p.calculate()
            soma_users += p.users
            total += p.counter
        return soma_users, total

    def get_distinct_users(self):
        users = set()
        for p in self:
            users = users.union(p.users)
        return len(users)

    def get_maximums(self, key=lambda x: x.counter):
        maximo = key(self[0])
        return [p.word for p in self if key(p) == maximo]


if __name__ == "__main__":
    myList = WordList()
    # mysort = myList.radix_sort  # change to test
    input()
    start = timeit.default_timer()
    a = 0
    while True:
        a += 1
        command = input()
        command = command.split(" ")
        if len(command) == 1:
            break
        myList.insert_word(command[0].upper(), int(command[1]))
    print(a)

    print("Distinct users: %d" % (myList.get_distinct_users()))
    print("Distinct words: %d" % (len(myList)))
    pairs, total = myList.calculate()
    print("Distinct word, user pairs: %d" % pairs)
    print("Total searches: %d" % total)
    print("GUARDADAS")
    print("load took: %f" % ((timeit.default_timer() - start) * 1000))

    global_list = copy.copy(myList)
    users_list = copy.copy(myList)

    start = timeit.default_timer()
    global_list.radix_sort(key=lambda x: x.counter)
    print("global took: %f" % ((timeit.default_timer() - start) * 1000))

    start = timeit.default_timer()
    users_list.radix_sort(key=lambda x: x.users)
    print("users took: %f" % ((timeit.default_timer() - start) * 1000))

    while True:
        command = input()
        if command == "TCHAU":
            break
        elif command == "PESQ_GLOBAL":
            # mysort(key=lambda x: x.counter)
            # maximums = myList.get_maximums(key=lambda x: x.counter)
            maximums = global_list.get_maximums(key=lambda x: x.counter)
            maximums.sort()
            print(' '.join(maximums))
        elif command == "PESQ_UTILIZADORES":
            # mysort(key=lambda x: x.users)
            # maximums = myList.get_maximums(key=lambda x: x.users)
            maximums = users_list.get_maximums(key=lambda x: x.users)
            maximums.sort()
            print(' '.join(maximums))
