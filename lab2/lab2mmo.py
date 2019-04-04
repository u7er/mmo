#запилить забор с двух концов в data =
import random
import math
import csv
distances = []


def get_distances_learn(learn_data):  # тут размер learn*k
    distances.clear()
    length = len(learn_data)
    point_distance = []
    for i in range(length):
        for j in range(length):
            if i == j:
                continue
            point_distance.append([dist(learn_data[i], learn_data[j]), learn_data[j][2]])
        distances.append(point_distance[:21])
        point_distance.clear()
        distances[i].sort(key=lambda e: e[0])


def get_distances_test(learn_data, test_data):  # тут размер learn*test
    distances.clear()
    point_distance = []
    test_length = len(test_data)
    learn_length = len(learn_data)
    for i in range(test_length):
        for j in range(learn_length):
            point_distance.append([dist(test_data[i], learn_data[j]), learn_data[j][2]])
        distances.append(point_distance[:21])
        point_distance.clear()
        distances[i].sort(key=lambda e: e[0])


def dist(a, b):  # просто расстояние в декартовых координатах между a и b
    return math.sqrt(((a[0]) - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


def get_k(learn_data):  # выбораем оптимальное k таким образом, что при попытке классифицировать уже известные объекты
    minimum = 100000  # из обучающей выборки получится минимальное количество ошибок
    answer = 0
    for k in range(3, 20, 2):
        neigh = LOO(learn_data, k)  # тут перебираем эти k
        if neigh < minimum:
            minimum = neigh
            answer = k
    return answer

def get_q(learn_data, k):  # выбораем оптимальное k таким образом, что при попытке классифицировать уже известные объекты
    minimum = 100000  # из обучающей выборки получится минимальное количество ошибок
    answer = 0
    for q in range(1, 99, 1):
        neigh = LOOq(learn_data, k, q/100)  # тут перебираем эти k
        if neigh < minimum:
            minimum = neigh
            answer = q
    return answer


def LOO(learn_data, k):
    summa = 0
    length = len(learn_data)
    for i in range(length):
        summa += int(parsen(i, k) != learn_data[i][2])  # parsen классифицирует объекты i`ые из learn, и тут же копим все ошибки
    return summa  # чем summa меньше тем лучше k


def LOOq(learn_data, k, q):
    summa = 0
    length = len(learn_data)
    for i in range(length):
        summa += int(parsen(i, k, q) != learn_data[i][2])  # parsen классифицирует объекты i`ые из learn, и тут же копим все ошибки
    return summa  # чем summa меньше тем лучше k


def parsen(index_u, k, q=0.62):  # parsen классифицирует объект под номером index_u.
    maximum = 0  # множество, откуда берём index_u`ый объект подразумевается с помощью заданных заранее distances
    answer = 0
    for y in range(2):  # пытаемся отнести проверяемый объект ко всем возможным объектам класса 0 и 1
        summa = 0
        for i in range(1, k + 1):  # рассматривается при этом k ближайших соседей
            neigh_i = distances[index_u][i]
            # считаем чего рядом больше объектов из 0 или 1. всё что не влезет в h-окно, обнулит ядро
            summa += int(neigh_i[1] == y) * pow(q, i)
        if summa > maximum:
            maximum = summa
            answer = y
    return answer

# разделение на learn и test выборки по принципу 50 на 50 нулей и единиц в learn, остальное в test
def split_on_test_and_learn(data, percent_test):
    percent_test = 1-percent_test
    learn_data = []
    test_data = []
    data.sort(key=lambda row: row[2])
    for i in range(len(data)):
        if data[i][2] == 0:
            where = i
    howmany = int(percent_test*len(data))
    for i in range(len(data)):
        if i % 2 > 0 and where > 0 and howmany != 0:
            random_number = random.randint(0, where)
            where = where - 1
            learn_data.append(data[random_number])
            data.remove(data[random_number])
            howmany -= 1
            continue
        if i % 2 != 0 and where > 0 and howmany != 0:
            random_number = random.randint(where, len(data) - 1)
            learn_data.append(data[random_number])
            data.remove(data[random_number])
            howmany -= 1
            continue

        if i % 2 > 0 and where > 0 and howmany == 0:
            random_number = random.randint(0, where)
            where = where - 1
            test_data.append(data[random_number])
            data.remove(data[random_number])
            continue
        if i % 2 != 0 and where > 0 and howmany == 0:
            random_number = random.randint(where, len(data) - 1)
            test_data.append(data[random_number])
            data.remove(data[random_number])
            continue

        if howmany > 0:
            random_number = random.randint(where, len(data) - 1)
            learn_data.append(data[random_number])
            data.remove(data[random_number])
            howmany -= 1
            continue
        else:
            random_number = random.randint(where, len(data) - 1)
            test_data.append(data[random_number])
            data.remove(data[random_number])
    return learn_data, test_data


def read_file():  # считываем из файла в список
    data = []
    csv_file = open('data.csv')
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:  # первую строчку с заголовками пропускаем
            line_count += 1
            continue
        else:
            line_count += 1
            data.append([int(row[0]), int(row[1]), int(row[2])])
    return data


def count_of_objects(list, object_class):  # подсчет объектов класса object_class
    count = 0
    for i in range(len(list)):
        if list[i][2] == object_class:
            count += 1
    return count


def main():
    data = read_file()  # в список data считываем наш csv`шник
    count = count_of_objects(data, 0)  # подсчитываем количество объектов класса 0 во всех data
    print('Количество объектов класса 0 в исходной выборке:', count, '(',
          (count * 100) / len(data), '% )')
    count = count_of_objects(data, 1)  # подсчитываем количество объектов класса 1 во всех data
    print('Количество объектов класса 1 в исходной выборке:', count, '(',
          (count * 100) / len(data), '% )\n')
    for i in range(3):  # будет 3 разбиения
        data = read_file()
        print('Разбиение', i + 1)

        learn, test = split_on_test_and_learn(data, 0.95)  # test составляет 66% от data. но это будет так долго,
        count = count_of_objects(learn, 0)  # что  если хотите посмотреть на результат советую использовать значение 0.95
        print('Количество объектов класса 0 в обучающей выборке:', count, '(',
              (count * 100) / len(learn), '% )')
        count = count_of_objects(learn, 1)  # подсчитываем количество объектов класса 1 в обучающей выборке
        print('Количество объектов класса 1 в обучающей выборке:', count, '(',
              (count * 100) / len(learn), '% )')
        count = count_of_objects(test, 0)
        print('Количество объектов класса 0 в тестовой выборке:', count, '(',
              (count * 100) / len(test), '% )')
        count = count_of_objects(test, 1)  # подсчитываем количество объектов класса 1 в тестовой выборке
        print('Количество объектов класса 1 в тестовой выборке:', count, '(',
              (count * 100) / len(test), '% )')
        # считаем расстояния между всеми объектами learn.
        # занимает больше всего времени
        get_distances_learn(learn)  # нужно для выбора k
        k = get_k(learn)  # выбираем количество соседей k
        q = get_q(learn, k)
        print('Количество соседей k =', k)
        # print('\nq =', q)
        # считаем расстояния между всеми объектами learn и test выборок. в test при этом подразумеваются любые объекты
        # занимает больше всего времени
        get_distances_test(learn, test)  # они нужны для осуществления классификации из test
        mistakes = 0
        for val in range(len(test)):
            answer = parsen(val, k, q)  # непосредственная классификация
            mistakes += int(answer != test[val][2])  # подсчет ошибок классификации
        print('Количество ошибок на тестовой выборке:', mistakes, '(', (mistakes * 100) / len(test), '% )\n')


if __name__ == "__main__":
    main()
