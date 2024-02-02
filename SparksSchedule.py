import random
from NextSchedule import *
import copy

from functools import reduce


def ilen(iterable):
    return reduce(lambda sum, element: sum + 1, iterable, 0)


class SparksSchedule:
    def __init__(self):
        # 35 вариантов
        self.vovan = []
        self.ghostOneTime = []
        self.ghostPair = []
        self.__setBase()
        self.ghostNames = {
            1: 'Даша',
            2: 'Маша',
            3: 'Саша',
            4: 'Лада',
            5: 'Артур'
        }
        self.eldersNames = {
            1: 'Вован',
            2: 'Люба'
        }
        self.ghostLimits = {
            1: 3.5,
            2: 3.5,
            3: 3,
            4: 3,
            5: 1
        }
        self.undesirableGhostDays = {
            1: [1, 2],
            2: [3, 5, 6],
            3: [],
            4: [1, 2, 3, 7],
            5: []
        }

    def __ghostTraversalGen(self):
        self.__setBase()

        while True:
            self.ghostPair = [(1, 2), (1, 2), (1, 2), (1, 2)]
            while True:
                yield
                if not self.nextGhostPair():
                    break
            if not self.nextGhostOneTime():
                break

    def findFirstGhost(self):
        differInTurnsCoef = 1.5
        turnRepeatCoef = 10
        undesirableDayCoef = 5

        minDebatov = 1e5
        bestCount = 2
        scheduleBest = {minDebatov + i * 1.0: SparksSchedule() for i in range(bestCount)}
        iterationId = 0
        for _ in self.__ghostTraversalGen():
            iterationId += 1
            currDebatov = 0.0

            """ Turn Count By Ghost """
            turnCountDict = [0 for i in self.ghostNames]

            """ The Longest Turn Repeats """
            turnRepeats = 0
            ghostRepeat = -1
            maxTurnRepeat = 0

            for ghostId in self.ghostOneTime:
                """ Turn Count By Ghost """
                turnCountDict[ghostId - 1] += 1

                """ The Longest Turn Repeats """
                if ghostRepeat == ghostId:
                    turnRepeats = turnRepeats + 1
                else:
                    maxTurnRepeat = max(maxTurnRepeat, turnRepeats)
                    turnRepeats = 1
                ghostRepeat = ghostId

            """ The Longest Turn Repeats """
            secondTurnRepeats = 0
            secondGhostRepeat = -1
            for p in self.ghostPair:
                """ Turn Count By Ghost """
                turnCountDict[p[0] - 1] += 1
                turnCountDict[p[1] - 1] += 1

                """ The Longest Turn Repeats """
                if secondGhostRepeat == p[0] or secondGhostRepeat == p[1]:
                    secondTurnRepeats += 1
                else:
                    maxTurnRepeat = max(maxTurnRepeat, secondTurnRepeats)
                    secondTurnRepeats = 1
                    secondGhostRepeat = p[0] if ghostRepeat != p[0] else p[1]

                if ghostRepeat == p[0] or ghostRepeat == p[1]:
                    turnRepeats = turnRepeats + 1
                else:
                    maxTurnRepeat = max(maxTurnRepeat, turnRepeats)
                    turnRepeats = 1
                    ghostRepeat = p[0] if secondGhostRepeat != p[0] else p[1]

            """ Turn Count By Ghost """
            # смотрим разницу между желаемым количеством смен для каждого духа
            # и текущим рассматриваемым расписанием
            for ghostId, limit in self.ghostLimits.items():
                currDebatov += differInTurnsCoef * abs(turnCountDict[ghostId - 1] - limit)

            """ The Longest Turn Repeats """
            maxTurnRepeat = max(maxTurnRepeat, ghostRepeat, secondTurnRepeats)
            if maxTurnRepeat >= 3:
                currDebatov += turnRepeatCoef + (maxTurnRepeat - 3) * turnRepeatCoef

            if currDebatov < minDebatov:
                scheduleBest.pop(max(scheduleBest.keys()))
                while currDebatov in scheduleBest:
                    currDebatov += 0.0001
                scheduleBest[currDebatov] = copy.deepcopy(self)
                minDebatov = float(max(scheduleBest.keys()))

        print(f"Количество итераций: {iterationId}")
        print()
        for s in scheduleBest.items():
            print(f"Минимум дебатов: {s[0]}")
            s[1].print()
            print()

    def calcTraverseLen(self):
        self.__setBase()

        traversalLen = 0
        while True:
            self.ghostPair = [(1, 2), (1, 2), (1, 2), (1, 2)]
            while True:
                traversalLen += 1
                if not self.nextGhostPair():
                    break
            if not self.nextGhostOneTime():
                break

        return traversalLen

    def nextGhostPair(self):
        return nextPairSchedule(self.ghostPair, 5, 4)

    def nextGhostOneTime(self):
        return nextOneTimeScheduleOfGhostman(self.ghostOneTime, 5, 3)

    def shuffle(self):
        self.__setBase()

        n = random.randint(1, 35)
        for i in range(1, n):
            nextScheduleOfElderman(self.vovan, 4, 7)

        n = random.randint(1, 125)
        for i in range(1, n):
            nextOneTimeScheduleOfGhostman(self.ghostOneTime, 5, 3)

        n = random.randint(1, int(1e4))
        for i in range(1, n):
            nextPairSchedule(self.ghostPair, 5, 4)

    def __setBase(self):
        # 35 вариантов
        self.vovan = [1, 2, 3, 4]
        # lubaSchedule === [5, 6, 7] соответственно

        # пн, вт, ср (125 variants)
        # хранит список духов по порядку дней когда у кого смена (Даша пн, Даша вт, Даша ср)
        self.ghostOneTime = [1, 1, 1]

        # чт, пт, сб, вс (10 000 variants)
        # хранит список пар духов по порядку дней у кого смена (Даша, Маша чт), (Даша, Маша пт)...
        # (1, 2) === (2, 1)
        self.ghostPair = [(1, 2), (1, 2), (1, 2), (1, 2)]

    def print(self):
        week = range(1, 7 + 1)
        nameMaxLen = 6
        print(''.rjust(nameMaxLen + 1), end='')
        for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
            print(day.rjust(4), end='')
        print()

        print(self.eldersNames[1].rjust(nameMaxLen) + ':', end='')
        for i in week:
            print(('C' if i in self.vovan else 'x').rjust(4), end='')
        print()
        print(self.eldersNames[2].rjust(nameMaxLen) + ':', end='')
        for i in week:
            print(('C' if i not in self.vovan else 'x').rjust(4), end='')
        print()

        print('---------------------'.rjust((nameMaxLen + 1 + 7 * 4) // 5 * 4))

        oneTimeWeek = [1, 2, 3]
        for [id, name] in self.ghostNames.items():
            print(name.rjust(nameMaxLen) + ':', end='')
            for i in week:
                if i in oneTimeWeek:
                    print(('C' if self.ghostOneTime[i - 1] == id else 'x').rjust(4), end='')
                else:
                    print(('C' if id in self.ghostPair[i - 4] else 'x').rjust(4), end='')
            print()
